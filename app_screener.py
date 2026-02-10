"""
Interfaz Web para Screener IVR
Streamlit App con actualización automática y alertas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from screener_ivr import ScreenerIVR
import json
import os

# Configuración de página
st.set_page_config(
    page_title="Screener IVR - Valoración Relativa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .signal-buy {
        color: #00cc00;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .signal-sell {
        color: #ff3333;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


def cargar_configuracion():
    """Cargar configuración guardada"""
    config_file = 'config_screener.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {
        'tickers': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
        'pesos': {'valoracion': 0.60, 'calidad': 0.30, 'timing': 0.10},
        'umbral_compra': 0.60,
        'umbral_venta': 0.30,
        'actualizacion_minutos': 30
    }


def guardar_configuracion(config):
    """Guardar configuración"""
    with open('config_screener.json', 'w') as f:
        json.dump(config, f, indent=2)


def crear_gauge_ivr(ivr_value, nombre):
    """Crear gauge visual para IVR"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ivr_value * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': nombre, 'font': {'size': 14}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "#ff4444"},
                {'range': [30, 60], 'color': "#ffaa00"},
                {'range': [60, 100], 'color': "#44ff44"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def mostrar_señal(ivr, umbral_compra, umbral_venta):
    """Determinar y mostrar señal de trading"""
    if ivr >= umbral_compra:
        return "🟢 COMPRA FUERTE", "signal-buy"
    elif ivr >= (umbral_compra + umbral_venta) / 2:
        return "🟡 COMPRA MODERADA", "signal-buy"
    elif ivr <= umbral_venta:
        return "🔴 VENTA", "signal-sell"
    else:
        return "⚪ NEUTRAL", ""


def main():
    # Header
    st.markdown('<p class="main-header">📊 Screener de Valoración Relativa (IVR)</p>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar configuración
    if 'config' not in st.session_state:
        st.session_state.config = cargar_configuracion()
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Pesos personalizados
        st.subheader("Pesos del Algoritmo")
        peso_val = st.slider("Valoración", 0.0, 1.0, 
                             st.session_state.config['pesos']['valoracion'], 0.05)
        peso_cal = st.slider("Calidad", 0.0, 1.0, 
                             st.session_state.config['pesos']['calidad'], 0.05)
        peso_tim = st.slider("Timing", 0.0, 1.0, 
                             st.session_state.config['pesos']['timing'], 0.05)
        
        # Normalizar pesos
        total_peso = peso_val + peso_cal + peso_tim
        if total_peso > 0:
            pesos_normalizados = {
                'valoracion': peso_val / total_peso,
                'calidad': peso_cal / total_peso,
                'timing': peso_tim / total_peso
            }
        else:
            pesos_normalizados = st.session_state.config['pesos']
        
        st.info(f"Normalizado: Val={pesos_normalizados['valoracion']:.0%}, "
                f"Cal={pesos_normalizados['calidad']:.0%}, "
                f"Tim={pesos_normalizados['timing']:.0%}")
        
        st.markdown("---")
        
        # Umbrales de señal
        st.subheader("Umbrales de Señal")
        umbral_compra = st.slider("Umbral COMPRA", 0.0, 1.0, 
                                   st.session_state.config['umbral_compra'], 0.05)
        umbral_venta = st.slider("Umbral VENTA", 0.0, 1.0, 
                                  st.session_state.config['umbral_venta'], 0.05)
        
        st.markdown("---")
        
        # Tickers
        st.subheader("Tickers a Analizar")
        tickers_input = st.text_area(
            "Símbolos (separados por coma)",
            value=", ".join(st.session_state.config['tickers']),
            height=100
        )
        tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
        
        st.markdown("---")
        
        # Auto-actualización
        st.subheader("Auto-actualización")
        auto_refresh = st.checkbox("Activar auto-refresh", value=False)
        intervalo = st.selectbox(
            "Intervalo (minutos)",
            [5, 15, 30, 60],
            index=2
        )
        
        st.markdown("---")
        
        # Botones de acción
        if st.button("💾 Guardar Configuración", use_container_width=True):
            st.session_state.config = {
                'tickers': tickers_list,
                'pesos': pesos_normalizados,
                'umbral_compra': umbral_compra,
                'umbral_venta': umbral_venta,
                'actualizacion_minutos': intervalo
            }
            guardar_configuracion(st.session_state.config)
            st.success("✅ Configuración guardada!")
        
        if st.button("🔄 Escanear Ahora", type="primary", use_container_width=True):
            st.session_state.trigger_scan = True
    
    # Main content
    if st.button("▶️ Ejecutar Screener") or st.session_state.get('trigger_scan', False):
        st.session_state.trigger_scan = False
        
        # Crear screener con pesos personalizados
        screener = ScreenerIVR(pesos_personalizados=pesos_normalizados)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Escanear tickers
        resultados = []
        for i, ticker in enumerate(tickers_list):
            status_text.text(f"Analizando {ticker}... ({i+1}/{len(tickers_list)})")
            progress_bar.progress((i + 1) / len(tickers_list))
            
            resultado = screener.calcular_ivr(ticker)
            if resultado:
                resultados.append(resultado)
        
        status_text.text("✅ Análisis completado!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        if resultados:
            df = pd.DataFrame(resultados)
            df = df.sort_values('ivr', ascending=False).reset_index(drop=True)
            
            # Guardar en session state
            st.session_state.df_resultados = df
            st.session_state.ultima_actualizacion = datetime.now()
    
    # Mostrar resultados si existen
    if 'df_resultados' in st.session_state:
        df = st.session_state.df_resultados
        ultima_act = st.session_state.ultima_actualizacion
        
        # Timestamp
        st.info(f"📅 Última actualización: {ultima_act.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analizados", len(df))
        with col2:
            pasan_filtros = df['pasa_filtros'].sum()
            st.metric("Pasan Filtros", pasan_filtros)
        with col3:
            señales_compra = (df['ivr'] >= umbral_compra).sum()
            st.metric("🟢 Señales COMPRA", señales_compra)
        with col4:
            ivr_promedio = df[df['pasa_filtros']]['ivr'].mean()
            st.metric("IVR Promedio", f"{ivr_promedio:.2%}")
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Ranking", "📊 Detalles", "📈 Gráficos", "🔔 Alertas"])
        
        with tab1:
            st.subheader("🏆 Ranking por IVR")
            
            # Preparar tabla de visualización
            df_display = df.copy()
            df_display['ivr_pct'] = (df_display['ivr'] * 100).round(2)
            df_display['ms_pct'] = (df_display['margen_seguridad'] * 100).round(2)
            df_display['señal'] = df_display['ivr'].apply(
                lambda x: mostrar_señal(x, umbral_compra, umbral_venta)[0]
            )
            
            cols_mostrar = ['ticker', 'nombre', 'precio', 'ivr_pct', 'ms_pct', 
                           'score_valoracion', 'score_calidad', 'score_timing', 
                           'pasa_filtros', 'señal']
            
            # Colorear filas según señal
            def highlight_rows(row):
                if row['ivr_pct'] >= umbral_compra * 100:
                    return ['background-color: #d4edda'] * len(row)
                elif row['ivr_pct'] <= umbral_venta * 100:
                    return ['background-color: #f8d7da'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_display[cols_mostrar].style.apply(highlight_rows, axis=1),
                use_container_width=True,
                height=400
            )
        
        with tab2:
            st.subheader("🔍 Análisis Detallado")
            
            # Selector de ticker
            ticker_seleccionado = st.selectbox(
                "Selecciona un ticker para ver detalles",
                df['ticker'].tolist()
            )
            
            data_ticker = df[df['ticker'] == ticker_seleccionado].iloc[0]
            
            # Layout en columnas
            col_izq, col_der = st.columns([2, 1])
            
            with col_izq:
                # Información general
                st.markdown(f"### {data_ticker['nombre']} ({data_ticker['ticker']})")
                st.write(f"**Sector:** {data_ticker['sector']}")
                st.write(f"**Precio actual:** ${data_ticker['precio']:.2f}")
                st.write(f"**Valor intrínseco:** ${data_ticker['valor_intrinseco']:.2f}")
                
                # Señal
                señal, clase = mostrar_señal(data_ticker['ivr'], umbral_compra, umbral_venta)
                st.markdown(f'<p class="{clase}">{señal}</p>', unsafe_allow_html=True)
                
                # Desglose de scores
                st.markdown("#### Desglose de Puntuaciones")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Valoración", f"{data_ticker['score_valoracion']:.2%}")
                with col2:
                    st.metric("Calidad", f"{data_ticker['score_calidad']:.2%}")
                with col3:
                    st.metric("Timing", f"{data_ticker['score_timing']:.2%}")
                
                # Margen de seguridad
                st.markdown("#### Margen de Seguridad")
                st.metric(
                    "Diferencia vs Valor Intrínseco",
                    f"{data_ticker['margen_seguridad']:.2%}",
                    delta=f"${data_ticker['valor_intrinseco'] - data_ticker['precio']:.2f}"
                )
                
                # Filtros de seguridad
                st.markdown("#### Filtros de Seguridad")
                if data_ticker['pasa_filtros']:
                    st.success("✅ Pasa todos los filtros de seguridad")
                else:
                    st.error(f"❌ {data_ticker['razon_filtro']}")
            
            with col_der:
                # Gauge de IVR
                fig_gauge = crear_gauge_ivr(data_ticker['ivr'], "IVR Total")
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # RSI
                st.metric("RSI (14)", f"{data_ticker['rsi']:.2f}")
        
        with tab3:
            st.subheader("📊 Visualizaciones")
            
            # Gráfico de dispersión IVR vs Margen Seguridad
            fig_scatter = px.scatter(
                df,
                x='margen_seguridad',
                y='ivr',
                size='precio',
                color='pasa_filtros',
                hover_data=['ticker', 'nombre'],
                labels={
                    'margen_seguridad': 'Margen de Seguridad',
                    'ivr': 'IVR',
                    'pasa_filtros': 'Pasa Filtros'
                },
                title='IVR vs Margen de Seguridad'
            )
            
            # Añadir líneas de umbral
            fig_scatter.add_hline(y=umbral_compra, line_dash="dash", 
                                 line_color="green", annotation_text="Umbral Compra")
            fig_scatter.add_hline(y=umbral_venta, line_dash="dash", 
                                 line_color="red", annotation_text="Umbral Venta")
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Gráfico de barras por componente
            df_top5 = df.head(5)
            
            fig_components = go.Figure()
            fig_components.add_trace(go.Bar(
                name='Valoración',
                x=df_top5['ticker'],
                y=df_top5['score_valoracion'] * pesos_normalizados['valoracion']
            ))
            fig_components.add_trace(go.Bar(
                name='Calidad',
                x=df_top5['ticker'],
                y=df_top5['score_calidad'] * pesos_normalizados['calidad']
            ))
            fig_components.add_trace(go.Bar(
                name='Timing',
                x=df_top5['ticker'],
                y=df_top5['score_timing'] * pesos_normalizados['timing']
            ))
            
            fig_components.update_layout(
                barmode='stack',
                title='Contribución de Componentes al IVR (Top 5)',
                yaxis_title='Puntuación'
            )
            
            st.plotly_chart(fig_components, use_container_width=True)
        
        with tab4:
            st.subheader("🔔 Sistema de Alertas")
            
            # Generar alertas
            alertas_compra = df[df['ivr'] >= umbral_compra]
            alertas_venta = df[df['ivr'] <= umbral_venta]
            
            if len(alertas_compra) > 0:
                st.success(f"### 🟢 {len(alertas_compra)} SEÑALES DE COMPRA")
                for _, row in alertas_compra.iterrows():
                    with st.expander(f"{row['ticker']} - {row['nombre']} (IVR: {row['ivr']:.2%})"):
                        st.write(f"**Precio:** ${row['precio']:.2f}")
                        st.write(f"**Valor Intrínseco:** ${row['valor_intrinseco']:.2f}")
                        st.write(f"**Margen de Seguridad:** {row['margen_seguridad']:.2%}")
                        st.write(f"**Pasa filtros:** {'✅ Sí' if row['pasa_filtros'] else '❌ No'}")
            
            if len(alertas_venta) > 0:
                st.warning(f"### 🔴 {len(alertas_venta)} SEÑALES DE VENTA")
                for _, row in alertas_venta.iterrows():
                    with st.expander(f"{row['ticker']} - {row['nombre']} (IVR: {row['ivr']:.2%})"):
                        st.write(f"**Precio:** ${row['precio']:.2f}")
                        st.write(f"**Razón:** IVR por debajo del umbral de venta")
            
            # Opción de exportar alertas
            st.markdown("---")
            st.markdown("#### Exportar Alertas")
            
            col1, col2 = st.columns(2)
            with col1:
                csv_compra = alertas_compra.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar señales de COMPRA (CSV)",
                    data=csv_compra,
                    file_name=f"alertas_compra_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                csv_todas = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar análisis completo (CSV)",
                    data=csv_todas,
                    file_name=f"screener_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    else:
        st.info("👆 Presiona '▶️ Ejecutar Screener' para comenzar el análisis")
    
    # Auto-refresh
    if auto_refresh and 'ultima_actualizacion' in st.session_state:
        tiempo_desde_ultimo = (datetime.now() - st.session_state.ultima_actualizacion).seconds / 60
        if tiempo_desde_ultimo >= intervalo:
            st.rerun()


if __name__ == "__main__":
    main()
