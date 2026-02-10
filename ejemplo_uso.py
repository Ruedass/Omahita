"""
Script de Ejemplo Rápido - Test del Screener IVR
Analiza algunos tickers populares y muestra resultados
"""

from screener_ivr import ScreenerIVR
from listas_tickers import MEGA_CAPS, TECH, VALUE_STOCKS
import pandas as pd

def ejemplo_basico():
    """Ejemplo básico: Analizar mega caps"""
    print("="*80)
    print("🚀 EJEMPLO BÁSICO - MEGA CAPS")
    print("="*80)
    
    # Crear screener
    screener = ScreenerIVR()
    
    # Analizar
    tickers = MEGA_CAPS[:5]  # Primeras 5
    print(f"\nAnalizando: {', '.join(tickers)}")
    
    df = screener.escanear_lista(tickers)
    
    # Mostrar resultados
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80)
    
    for idx, row in df.iterrows():
        print(f"\n{idx+1}. {row['ticker']} - {row['nombre'][:40]}")
        print(f"   IVR: {row['ivr']:.2%}")
        print(f"   Precio: ${row['precio']:.2f}")
        print(f"   Valor Intrínseco: ${row['valor_intrinseco']:.2f}")
        print(f"   Margen Seguridad: {row['margen_seguridad']:.2%}")
        print(f"   Pasa filtros: {'✅ Sí' if row['pasa_filtros'] else '❌ No'}")
        
        if row['ivr'] >= 0.60:
            print(f"   🟢 SEÑAL: COMPRA")
        elif row['ivr'] <= 0.30:
            print(f"   🔴 SEÑAL: VENTA")
        else:
            print(f"   🟡 SEÑAL: NEUTRAL")
    
    return df


def ejemplo_comparacion_sectores():
    """Comparar diferentes sectores"""
    print("\n" + "="*80)
    print("📊 COMPARACIÓN TECH vs VALUE")
    print("="*80)
    
    screener = ScreenerIVR()
    
    # Tech
    print("\n🔵 Analizando TECH...")
    tech_tickers = TECH[:3]
    df_tech = screener.escanear_lista(tech_tickers)
    df_tech['sector_grupo'] = 'Tech'
    
    # Value
    print("🟢 Analizando VALUE...")
    value_tickers = VALUE_STOCKS[:3]
    df_value = screener.escanear_lista(value_tickers)
    df_value['sector_grupo'] = 'Value'
    
    # Combinar
    df_combined = pd.concat([df_tech, df_value])
    
    # Comparar promedios
    print("\n" + "="*80)
    print("PROMEDIOS POR SECTOR")
    print("="*80)
    
    for sector in ['Tech', 'Value']:
        df_sector = df_combined[df_combined['sector_grupo'] == sector]
        print(f"\n{sector}:")
        print(f"  IVR Promedio: {df_sector['ivr'].mean():.2%}")
        print(f"  Margen Seguridad Promedio: {df_sector['margen_seguridad'].mean():.2%}")
        print(f"  % Pasan filtros: {df_sector['pasa_filtros'].sum() / len(df_sector) * 100:.0f}%")
    
    return df_combined


def ejemplo_pesos_personalizados():
    """Ejemplo con diferentes pesos"""
    print("\n" + "="*80)
    print("⚖️ COMPARACIÓN CON DIFERENTES PESOS")
    print("="*80)
    
    ticker_test = 'AAPL'
    
    # Configuración 1: Value puro
    print(f"\n1️⃣ VALUE PURO (90% Valoración)")
    screener1 = ScreenerIVR({
        'valoracion': 0.90,
        'calidad': 0.05,
        'timing': 0.05
    })
    result1 = screener1.calcular_ivr(ticker_test)
    print(f"   {ticker_test} IVR: {result1['ivr']:.2%}")
    
    # Configuración 2: Balanceado
    print(f"\n2️⃣ BALANCEADO (60/30/10)")
    screener2 = ScreenerIVR({
        'valoracion': 0.60,
        'calidad': 0.30,
        'timing': 0.10
    })
    result2 = screener2.calcular_ivr(ticker_test)
    print(f"   {ticker_test} IVR: {result2['ivr']:.2%}")
    
    # Configuración 3: Growth focus
    print(f"\n3️⃣ GROWTH FOCUS (30% Valoración, 50% Calidad)")
    screener3 = ScreenerIVR({
        'valoracion': 0.30,
        'calidad': 0.50,
        'timing': 0.20
    })
    result3 = screener3.calcular_ivr(ticker_test)
    print(f"   {ticker_test} IVR: {result3['ivr']:.2%}")
    
    print("\n💡 Conclusión: Los pesos afectan significativamente el ranking!")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "SCREENER IVR - EJEMPLOS" + " "*35 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Ejemplo 1
        df1 = ejemplo_basico()
        
        # Ejemplo 2
        df2 = ejemplo_comparacion_sectores()
        
        # Ejemplo 3
        ejemplo_pesos_personalizados()
        
        print("\n" + "="*80)
        print("✅ EJEMPLOS COMPLETADOS")
        print("="*80)
        print("\n💡 Próximos pasos:")
        print("   1. Ejecuta 'streamlit run app_screener.py' para la interfaz web")
        print("   2. Ejecuta 'python scheduler_screener.py' para modo automático")
        print("   3. Personaliza los pesos y tickers según tu estrategia")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
