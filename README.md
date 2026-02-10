# 📊 Screener Financiero IVR (Índice de Valoración Relativo)

Sistema automático de análisis financiero basado en tu algoritmo personalizado de valoración relativa.

## 🎯 Características

- ✅ **100% Gratuito** - Sin costos de APIs ni servicios
- ✅ **Actualización automática** - Cada 30 minutos (configurable)
- ✅ **Alertas por email** - Notificaciones de señales de compra/venta
- ✅ **Interfaz web** - Dashboard interactivo con gráficos
- ✅ **Cloud o Local** - Funciona en ambos modos
- ✅ **Algoritmo personalizado** - Tu fórmula IVR exacta

## 🧮 Algoritmo IVR

El sistema calcula el **Índice de Valoración Relativo** basado en:

### A. Valoración (60%)
- **Múltiplos vs sector**: P/E, P/B, P/S, EV/EBITDA
- **DCF simplificado**: Margen de seguridad usando Free Cash Flow

### B. Salud y Crecimiento (30%)
- **Salud financiera**: Deuda/Equity, Current Ratio
- **Crecimiento**: CAGR de ingresos y earnings

### C. Timing/Momentum (10%)
- **RSI**: Indicador de sobrecompra/sobreventa
- **Tendencia**: SMA 50 vs SMA 200

### Filtros de Seguridad
❌ Rechaza automáticamente si:
- EPS TTM ≤ 0
- Free Cash Flow ≤ 0
- Cobertura de intereses < 2
- Margen de seguridad < 20%

## 🚀 Instalación

### Opción 1: Cloud (Streamlit Cloud) - RECOMENDADO

1. **Fork este repositorio** en GitHub

2. **Ve a [streamlit.io/cloud](https://streamlit.io/cloud)**

3. **Conecta tu GitHub** y selecciona tu repositorio

4. **Configura el deploy**:
   - Main file: `app_screener.py`
   - Python version: 3.11

5. **¡Listo!** Tendrás una URL pública tipo: `https://tu-app.streamlit.app`

**Ventajas**:
- ✅ Gratis para siempre
- ✅ Accesible desde cualquier dispositivo
- ✅ Auto-actualización cada que hagas push
- ✅ No consume recursos de tu PC

### Opción 2: Local (tu computadora)

1. **Clona o descarga** este proyecto

2. **Instala Python 3.8+** si no lo tienes

3. **Instala dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecuta la interfaz web**:
```bash
streamlit run app_screener.py
```

Se abrirá en `http://localhost:8501`

## 📖 Uso

### Interfaz Web (Streamlit)

1. **Configurar en el Sidebar**:
   - Ajusta los **pesos** del algoritmo (Valoración, Calidad, Timing)
   - Define **umbrales** de compra y venta
   - Ingresa los **tickers** a analizar
   - Activa **auto-refresh** si quieres

2. **Ejecutar Screener**:
   - Click en "🔄 Escanear Ahora"
   - Espera el análisis (30 seg - 2 min según cantidad de tickers)

3. **Ver Resultados**:
   - **Tab Ranking**: Lista ordenada por IVR
   - **Tab Detalles**: Análisis profundo de cada ticker
   - **Tab Gráficos**: Visualizaciones interactivas
   - **Tab Alertas**: Señales de compra/venta activas

4. **Exportar**:
   - Descarga CSV con todos los datos
   - Guarda configuración para próximas sesiones

### Modo Automático (Scheduler)

Para ejecutar análisis automáticos cada 30 minutos:

```bash
python scheduler_screener.py
```

**Menú interactivo**:
1. Ejecutar una vez (testing)
2. Modo automático (loop infinito)
3. Configurar tickers
4. Configurar pesos
5. Configurar alertas email
6. Ver último resultado
7. Ver historial

El scheduler:
- 🔄 Ejecuta cada 30 min (configurable)
- 💾 Guarda historial en CSV
- 📧 Envía emails automáticos con alertas
- 📊 Muestra resumen en consola

## 📧 Configurar Alertas por Email

Para recibir alertas automáticas por Gmail:

### 1. Preparar Gmail

1. Ve a tu cuenta Google → Seguridad
2. Activa **Verificación en 2 pasos**
3. En "Contraseñas de aplicaciones", genera una nueva
4. Copia la contraseña de 16 caracteres

### 2. Configurar en el Sistema

**Opción A - Desde la interfaz web**:
- Sidebar → Email Settings
- Ingresa email destino y credenciales

**Opción B - Desde el scheduler**:
```bash
python scheduler_screener.py
# Opción 5: Configurar alertas
```

**Opción C - Manual**:
Edita `config_alertas.json`:
```json
{
  "email_destino": "tu_email@gmail.com",
  "email_origen": "email_origen@gmail.com",
  "password": "abcd efgh ijkl mnop",
  "alertas_activas": true,
  "umbral_compra": 0.60,
  "umbral_venta": 0.30
}
```

### 3. Test
```python
from sistema_alertas import SistemaAlertas
sistema = SistemaAlertas()
sistema.test_email()  # Envía email de prueba
```

## 🎨 Personalización

### Modificar Pesos del Algoritmo

Edita directamente en la interfaz o en `config_screener.json`:

```json
{
  "pesos": {
    "valoracion": 0.70,  // Aumenta si quieres más énfasis en valuación
    "calidad": 0.20,     // Reduce si prefieres pure value
    "timing": 0.10       // Mantén bajo para buy & hold
  }
}
```

### Agregar Tickers

**Método 1 - Interfaz**: Sidebar → Tickers a analizar

**Método 2 - Código**: Edita `tickers_list` en `scheduler_screener.py`

**Método 3 - Por sector**:
```python
# Ejemplo: Tech sector
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'AMD', 'INTC']

# Ejemplo: ETFs
tickers = ['SPY', 'QQQ', 'IWM', 'DIA', 'VTI']

# Ejemplo: Crypto proxies
tickers = ['COIN', 'MSTR', 'RIOT', 'MARA']
```

### Ajustar Parámetros de Referencia

En `screener_ivr.py`, clase `ScreenerIVR.__init__()`:

```python
self.params = {
    'de_max_bueno': 1.5,    // Deuda/Equity máximo
    'cr_optimo': 2.0,        // Current Ratio ideal
    'cagr_optimo': 0.15,     // 15% crecimiento anual
    'rsi_centro': 40,        // RSI ideal
    'rsi_rango': 40,         // Tolerancia RSI
}
```

## 📊 Interpretación de Resultados

### IVR Score
- **0.70 - 1.00**: 🟢 COMPRA FUERTE - Excelente oportunidad
- **0.60 - 0.70**: 🟢 COMPRA - Buena valuación
- **0.40 - 0.60**: 🟡 NEUTRAL - Observar
- **0.30 - 0.40**: 🟠 PRECAUCIÓN - Posible sobrevaloración
- **0.00 - 0.30**: 🔴 VENTA - Caro o problemas fundamentales

### Señales
- ✅ **Pasa filtros** = Cumple todos los requisitos de seguridad
- ❌ **No pasa filtros** = Falla algún criterio fundamental
- 📊 **Margen seguridad** = % diferencia entre precio y valor intrínseco

## 🗂️ Estructura de Archivos

```
screener-ivr/
│
├── screener_ivr.py           # Motor del algoritmo IVR
├── app_screener.py            # Interfaz web Streamlit
├── scheduler_screener.py      # Ejecución automática
├── sistema_alertas.py         # Alertas por email
├── requirements.txt           # Dependencias
├── README.md                  # Este archivo
│
├── config_screener.json       # Configuración interfaz (auto-generado)
├── config_scheduler.json      # Configuración scheduler (auto-generado)
├── config_alertas.json        # Configuración emails (auto-generado)
│
└── historial_screener/        # Históricos CSV (auto-generado)
    ├── screener_20250210.csv
    └── ...
```

## 🔧 Solución de Problemas

### Error: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Error: Rate limit de Yahoo Finance
- Reduce cantidad de tickers
- Aumenta intervalo entre ejecuciones
- Yahoo limita ~2000 requests/hora

### Email no se envía
1. Verifica que uses **contraseña de aplicación**, no tu password normal
2. Chequea que tengas verificación en 2 pasos activa
3. Prueba con `sistema.test_email()`

### Streamlit Cloud: App inactiva
- Apps gratis duermen después de inactividad
- Primer acceso puede tardar 30 seg en despertar
- Considera usar cron job para mantenerla activa

### Datos inconsistentes
- Yahoo Finance puede tener delays de 15 min
- Algunos tickers tienen datos incompletos
- Verifica que el ticker sea correcto

## 📈 Próximas Mejoras

Ideas para expandir el sistema:

- [ ] Integración con otras APIs (Alpha Vantage, IEX Cloud)
- [ ] Backtesting histórico del algoritmo
- [ ] Machine Learning para ajuste dinámico de pesos
- [ ] Telegram bot para alertas
- [ ] Base de datos para historial más robusto
- [ ] Análisis de opciones (Greeks, IV)
- [ ] Portfolio tracker integrado

## 🤝 Contribuir

¡Contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -am 'Agrega nueva feature'`)
4. Push (`git push origin feature/mejora`)
5. Abre un Pull Request

## ⚠️ Disclaimer

**ESTE SOFTWARE ES SOLO PARA FINES EDUCATIVOS**

- No es asesoramiento financiero
- No garantiza rentabilidad
- Invierte bajo tu propio riesgo
- Siempre haz tu propia investigación (DYOR)
- Consulta con un asesor financiero certificado

El autor no se responsabiliza por pérdidas financieras derivadas del uso de este software.

## 📜 Licencia

MIT License - Uso libre para proyectos personales y comerciales

## 📞 Soporte

¿Preguntas? Abre un issue en GitHub o contacta al desarrollador.

---

**Desarrollado con ❤️ para inversores value**

*"El precio es lo que pagas, el valor es lo que obtienes" - Warren Buffett*
