"""
Screener Financiero con Índice de Valoración Relativo (IVR)
Sistema de valoración basado en múltiplos, DCF y timing
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ScreenerIVR:
    """Motor de cálculo del Índice de Valoración Relativo"""
    
    def __init__(self, pesos_personalizados=None):
        """
        Inicializar con pesos configurables
        
        Args:
            pesos_personalizados: dict con keys 'valoracion', 'calidad', 'timing'
        """
        self.pesos = pesos_personalizados or {
            'valoracion': 0.60,
            'calidad': 0.30,
            'timing': 0.10
        }
        
        # Parámetros de referencia
        self.params = {
            'de_max_bueno': 1.5,  # Deuda/Equity máximo aceptable
            'cr_optimo': 2.0,      # Current Ratio óptimo
            'cagr_optimo': 0.15,   # 15% crecimiento anual óptimo
            'rsi_centro': 40,      # Centro del RSI ideal
            'rsi_rango': 40,       # Rango de normalización RSI
        }
        
    def obtener_datos_ticker(self, ticker_symbol):
        """Obtener todos los datos necesarios de un ticker"""
        try:
            ticker = yf.Ticker(ticker_symbol)
            
            # Datos básicos
            info = ticker.info
            hist = ticker.history(period="1y")
            
            if hist.empty:
                return None
            
            # Precio actual
            precio_actual = hist['Close'].iloc[-1]
            
            # Preparar estructura de datos
            datos = {
                'ticker': ticker_symbol,
                'precio': precio_actual,
                'info': info,
                'hist': hist,
                'fecha': datetime.now()
            }
            
            return datos
            
        except Exception as e:
            print(f"Error obteniendo {ticker_symbol}: {e}")
            return None
    
    def calcular_dcf_simple(self, info, precio_actual):
        """
        DCF simplificado usando FCF y crecimiento estimado
        """
        try:
            # Obtener Free Cash Flow
            fcf = info.get('freeCashflow', 0)
            if fcf <= 0:
                return 0
            
            # Parámetros DCF
            tasa_crecimiento = info.get('earningsGrowth', 0.05) or 0.05
            tasa_crecimiento = min(max(tasa_crecimiento, 0), 0.25)  # Limitar 0-25%
            
            wacc = 0.10  # Costo capital promedio
            años_proyeccion = 5
            tasa_perpetua = 0.03
            
            # Proyección de FCF
            fcf_proyectado = []
            for año in range(1, años_proyeccion + 1):
                fcf_futuro = fcf * ((1 + tasa_crecimiento) ** año)
                valor_presente = fcf_futuro / ((1 + wacc) ** año)
                fcf_proyectado.append(valor_presente)
            
            # Valor terminal
            fcf_terminal = fcf * ((1 + tasa_crecimiento) ** años_proyeccion) * (1 + tasa_perpetua)
            valor_terminal = fcf_terminal / (wacc - tasa_perpetua)
            valor_terminal_presente = valor_terminal / ((1 + wacc) ** años_proyeccion)
            
            # Valor empresa
            valor_empresa = sum(fcf_proyectado) + valor_terminal_presente
            
            # Ajustar por deuda y efectivo
            deuda = info.get('totalDebt', 0)
            efectivo = info.get('totalCash', 0)
            valor_equity = valor_empresa - deuda + efectivo
            
            # Valor por acción
            shares = info.get('sharesOutstanding', 1)
            valor_intrinseco = valor_equity / shares if shares > 0 else 0
            
            return max(valor_intrinseco, 0)
            
        except Exception as e:
            print(f"Error en DCF: {e}")
            return 0
    
    def calcular_multiplos(self, info, precio_actual):
        """Calcular scores de múltiplos vs sector"""
        scores = []
        
        # P/E Ratio
        pe = info.get('trailingPE', None)
        pe_sector = info.get('industryPE', None) or info.get('forwardPE', None)
        
        if pe and pe_sector and pe > 0 and pe_sector > 0:
            r_pe = pe / pe_sector
            s_pe = max(0, min(1, 1 - r_pe))  # Invertir: menor es mejor
            scores.append(s_pe)
        
        # P/B Ratio
        pb = info.get('priceToBook', None)
        pb_sector = info.get('industryPB', 2.5)  # Default conservador
        
        if pb and pb > 0:
            r_pb = pb / pb_sector
            s_pb = max(0, min(1, 1 - r_pb))
            scores.append(s_pb)
        
        # P/S Ratio
        ps = info.get('priceToSalesTrailing12Months', None)
        ps_sector = info.get('industryPS', 2.0)
        
        if ps and ps > 0:
            r_ps = ps / ps_sector
            s_ps = max(0, min(1, 1 - r_ps))
            scores.append(s_ps)
        
        # EV/EBITDA
        ev_ebitda = info.get('enterpriseToEbitda', None)
        ev_sector = 12  # Promedio de mercado
        
        if ev_ebitda and ev_ebitda > 0:
            r_ev = ev_ebitda / ev_sector
            s_ev = max(0, min(1, 1 - r_ev))
            scores.append(s_ev)
        
        # Promedio de múltiplos
        if scores:
            return np.mean(scores)
        return 0.5  # Neutral si no hay datos
    
    def calcular_score_valoracion(self, info, precio_actual):
        """
        A. Valoración (60% del IVR)
        Combina múltiplos y margen de seguridad DCF
        """
        # 1. Score de múltiplos
        s_mult = self.calcular_multiplos(info, precio_actual)
        
        # 2. Margen de seguridad DCF
        valor_intrinseco = self.calcular_dcf_simple(info, precio_actual)
        
        if valor_intrinseco > 0:
            ms = (valor_intrinseco - precio_actual) / precio_actual
            s_ms = max(0, min(1, ms))  # Limitar a 0-1
        else:
            s_ms = 0
        
        # 3. Score final de valoración
        s_valoracion = 0.5 * s_mult + 0.5 * s_ms
        
        return s_valoracion, valor_intrinseco, ms if valor_intrinseco > 0 else 0
    
    def calcular_score_calidad(self, info):
        """
        B. Salud y Crecimiento (30% del IVR)
        """
        # 1. Salud financiera
        de_ratio = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
        current_ratio = info.get('currentRatio', 1.0)
        
        s_deuda = max(0, 1 - (de_ratio / self.params['de_max_bueno']))
        s_liquidez = min(1, current_ratio / self.params['cr_optimo'])
        
        s_salud = 0.5 * s_deuda + 0.5 * s_liquidez
        
        # 2. Crecimiento
        revenue_growth = info.get('revenueGrowth', 0) or 0
        earnings_growth = info.get('earningsGrowth', 0) or 0
        
        # Promedio de crecimientos
        cagr_estimado = (revenue_growth + earnings_growth) / 2
        
        if cagr_estimado > 0:
            s_crec = min(1, cagr_estimado / self.params['cagr_optimo'])
        else:
            s_crec = 0
        
        # 3. Score calidad
        s_calidad = 0.5 * s_salud + 0.5 * s_crec
        
        return s_calidad
    
    def calcular_rsi(self, precios, periodo=14):
        """Calcular RSI (Relative Strength Index)"""
        if len(precios) < periodo + 1:
            return 50  # Neutral por defecto
        
        deltas = precios.diff()
        gain = deltas.where(deltas > 0, 0)
        loss = -deltas.where(deltas < 0, 0)
        
        avg_gain = gain.rolling(window=periodo).mean()
        avg_loss = loss.rolling(window=periodo).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
    
    def calcular_score_timing(self, hist):
        """
        C. Timing / Momentum (10% del IVR)
        """
        precios = hist['Close']
        
        # 1. RSI
        rsi = self.calcular_rsi(precios)
        s_rsi = max(0, 1 - (abs(rsi - self.params['rsi_centro']) / self.params['rsi_rango']))
        
        # 2. Tendencia (SMA)
        if len(precios) >= 200:
            sma_50 = precios.rolling(window=50).mean().iloc[-1]
            sma_200 = precios.rolling(window=200).mean().iloc[-1]
            s_tendencia = 1 if sma_50 >= sma_200 else 0
        else:
            s_tendencia = 0.5  # Neutral
        
        # 3. Score timing
        s_timing = 0.7 * s_rsi + 0.3 * s_tendencia
        
        return s_timing, rsi
    
    def aplicar_reglas_seguridad(self, info, margen_seguridad):
        """
        Reglas duras de seguridad (filtros binarios)
        """
        # EPS TTM > 0
        eps = info.get('trailingEps', 0)
        if eps <= 0:
            return False, "EPS negativo o cero"
        
        # FCF > 0
        fcf = info.get('freeCashflow', 0)
        if fcf <= 0:
            return False, "Free Cash Flow negativo o cero"
        
        # Cobertura de intereses >= 2
        ebit = info.get('ebitda', 0)
        interest = info.get('interestExpense', 1)
        if interest and interest != 0:
            cobertura = abs(ebit / interest)
            if cobertura < 2:
                return False, f"Cobertura intereses baja: {cobertura:.2f}"
        
        # Margen de seguridad >= 20%
        if margen_seguridad < 0.20:
            return False, f"Margen seguridad bajo: {margen_seguridad*100:.1f}%"
        
        return True, "Aprobado"
    
    def calcular_ivr(self, ticker_symbol):
        """
        Calcular el IVR completo para un ticker
        
        Returns:
            dict con IVR y todos los componentes
        """
        # Obtener datos
        datos = self.obtener_datos_ticker(ticker_symbol)
        if not datos:
            return None
        
        info = datos['info']
        hist = datos['hist']
        precio = datos['precio']
        
        # A. Valoración
        s_val, valor_int, ms = self.calcular_score_valoracion(info, precio)
        
        # B. Calidad
        s_cal = self.calcular_score_calidad(info)
        
        # C. Timing
        s_tim, rsi = self.calcular_score_timing(hist)
        
        # Aplicar reglas de seguridad
        pasa_filtros, razon_filtro = self.aplicar_reglas_seguridad(info, ms)
        
        # Calcular IVR final
        if pasa_filtros:
            ivr = (self.pesos['valoracion'] * s_val + 
                   self.pesos['calidad'] * s_cal + 
                   self.pesos['timing'] * s_tim)
        else:
            ivr = 0
        
        # Resultado completo
        resultado = {
            'ticker': ticker_symbol,
            'fecha': datos['fecha'],
            'precio': precio,
            'valor_intrinseco': valor_int,
            'margen_seguridad': ms,
            'ivr': ivr,
            'score_valoracion': s_val,
            'score_calidad': s_cal,
            'score_timing': s_tim,
            'rsi': rsi,
            'pasa_filtros': pasa_filtros,
            'razon_filtro': razon_filtro,
            'nombre': info.get('longName', ticker_symbol),
            'sector': info.get('sector', 'N/A'),
        }
        
        return resultado
    
    def escanear_lista(self, tickers_list):
        """
        Escanear una lista de tickers y retornar DataFrame ordenado por IVR
        """
        resultados = []
        
        for ticker in tickers_list:
            print(f"Procesando {ticker}...")
            resultado = self.calcular_ivr(ticker)
            if resultado:
                resultados.append(resultado)
        
        # Convertir a DataFrame
        df = pd.DataFrame(resultados)
        
        # Ordenar por IVR descendente
        df = df.sort_values('ivr', ascending=False).reset_index(drop=True)
        
        return df


def ejemplo_uso():
    """Ejemplo de uso del screener"""
    
    # Crear screener con pesos por defecto
    screener = ScreenerIVR()
    
    # Lista de tickers a analizar (ejemplo S&P 500)
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT']
    
    # Escanear
    df_resultados = screener.escanear_lista(tickers)
    
    # Mostrar top 5
    print("\n" + "="*80)
    print("TOP 5 OPORTUNIDADES (Mayor IVR)")
    print("="*80)
    
    columnas_mostrar = ['ticker', 'nombre', 'precio', 'ivr', 'margen_seguridad', 
                        'score_valoracion', 'pasa_filtros']
    
    print(df_resultados[columnas_mostrar].head())
    
    return df_resultados


if __name__ == "__main__":
    df = ejemplo_uso()
