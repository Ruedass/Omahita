# 💡 Mejores Prácticas y Optimización del Screener IVR

## 🎯 Estrategias de Uso

### 1. Value Investing Clásico
**Pesos recomendados**:
- Valoración: 80%
- Calidad: 15%
- Timing: 5%

**Umbrales**:
- Compra: IVR ≥ 0.70
- Venta: IVR ≤ 0.30

**Mejor para**: Inversores de largo plazo, estilo Warren Buffett

### 2. GARP (Growth at Reasonable Price)
**Pesos recomendados**:
- Valoración: 50%
- Calidad: 40%
- Timing: 10%

**Umbrales**:
- Compra: IVR ≥ 0.60
- Venta: IVR ≤ 0.35

**Mejor para**: Balance entre valor y crecimiento

### 3. Oportunidades de Swing Trading
**Pesos recomendados**:
- Valoración: 40%
- Calidad: 30%
- Timing: 30%

**Umbrales**:
- Compra: IVR ≥ 0.55
- Venta: IVR ≤ 0.40

**Mejor para**: Operaciones de 1-3 meses

---

## 📊 Selección de Tickers

### Estrategia 1: Por Sectores
Diversifica analizando todos los sectores:

```python
from listas_tickers import *

mi_portafolio = (
    TECH[:5] +           # 5 tech
    FINANCIALS[:3] +     # 3 financieras
    HEALTHCARE[:3] +     # 3 healthcare
    ENERGY[:2] +         # 2 energía
    CONSUMER_STAPLES[:2] # 2 consumer
)
# Total: 15 tickers bien diversificados
```

### Estrategia 2: Small Caps (Mayor potencial)
```python
mi_portafolio = SMALL_CAPS[:20]
# Más volatilidad, más oportunidades
```

### Estrategia 3: Dividend Aristocrats (Estabilidad)
```python
mi_portafolio = DIVIDEND_ARISTOCRATS[:30]
# Empresas con 25+ años aumentando dividendos
```

### Estrategia 4: Mix Personalizado
```python
# 30% mega caps (estabilidad)
# 40% mid caps (balance)
# 30% small caps (crecimiento)

mi_portafolio = (
    MEGA_CAPS[:6] +    # 30%
    MID_CAPS[:8] +     # 40%
    SMALL_CAPS[:6]     # 30%
)
```

---

## ⏰ Frecuencia de Actualización

### Mercado en Tiempo Real
- **Intervalo**: 15 minutos
- **Cuándo**: Durante market hours (9:30 AM - 4:00 PM EST)
- **Para**: Day trading, swing trading

### Inversión Activa
- **Intervalo**: 30 minutos (default)
- **Cuándo**: Todo el día
- **Para**: Capturar oportunidades del día

### Buy & Hold
- **Intervalo**: 1-2 veces al día
- **Cuándo**: Apertura (9:30 AM) y cierre (4:00 PM)
- **Para**: Inversión de largo plazo

### Weekend Warrior
- **Intervalo**: Una vez al fin de semana
- **Cuándo**: Domingos por la tarde
- **Para**: Planificación semanal

---

## 🔍 Interpretación Avanzada de Resultados

### IVR Alto + Pasa Filtros ✅
**Señal**: 🟢 **COMPRA FUERTE**
- Empresa barata fundamentalmente
- Salud financiera sólida
- Margen de seguridad adecuado

**Acción**: Analizar manualmente y considerar compra

### IVR Alto + NO Pasa Filtros ❌
**Señal**: ⚠️ **TRAMPA DE VALOR**
- Parece barata pero hay problemas
- FCF negativo o deuda alta
- Evitar hasta que mejore fundamentales

**Acción**: Esperar mejora en filtros o descartar

### IVR Medio + Buena Tendencia
**Señal**: 🟡 **OBSERVAR**
- No es ganga pero tampoco cara
- Momentum positivo

**Acción**: Monitorear, comprar si baja a umbral

### IVR Bajo + Buen Sector
**Señal**: 🔴 **SOBREVALORADA**
- Precio por encima de valor intrínseco
- Posible corrección

**Acción**: Si la tienes, considerar venta parcial

---

## 💰 Gestión de Alertas

### Configuración Conservadora
```json
{
  "umbral_compra": 0.70,
  "umbral_venta": 0.25
}
```
**Resultado**: Pocas alertas, muy alta calidad

### Configuración Balanceada (Recomendada)
```json
{
  "umbral_compra": 0.60,
  "umbral_venta": 0.30
}
```
**Resultado**: Balance entre cantidad y calidad

### Configuración Agresiva
```json
{
  "umbral_compra": 0.50,
  "umbral_venta": 0.35
}
```
**Resultado**: Muchas alertas, filtrar manualmente

---

## 🚀 Optimización de Rendimiento

### Si el Screener es Lento

1. **Reduce tickers por ejecución**
   ```python
   # Mal: 100 tickers cada 15 min
   # Bien: 20 tickers cada 30 min
   ```

2. **Usa caché inteligente**
   ```python
   # Actualiza mega caps cada 15 min
   # Small caps cada 1 hora
   # ETFs cada 4 horas
   ```

3. **Horarios óptimos**
   - Evita 9:30-10:00 AM (apertura caótica)
   - Evita 3:45-4:00 PM (cierre volátil)
   - Mejor: 10:30 AM, 12:00 PM, 2:00 PM

### Límites de Yahoo Finance
- Máximo: ~2000 requests/hora
- Si te bloquean: Espera 1 hora
- Solución: Distribuir requests en el tiempo

```python
# Configuración segura
intervalo = 30  # minutos
tickers_por_ejecución = 20
# = 40 tickers/hora (muy por debajo del límite)
```

---

## 📈 Backtesting Manual

### Validar tu Estrategia

1. **Descarga historial**
   ```bash
   # Ejecuta screener durante 1 mes
   # Guarda resultados diarios
   ```

2. **Analiza señales pasadas**
   ```python
   # ¿Cuántas señales de compra tuviste?
   # ¿Qué % subieron después de 30 días?
   # ¿Cuál fue el retorno promedio?
   ```

3. **Ajusta parámetros**
   ```python
   # Si muchas falsas alarmas: Sube umbral_compra
   # Si pocas señales: Baja umbral_compra
   # Si muchos errores: Ajusta pesos
   ```

### Ejemplo de Tracking
```python
# Cada vez que compras según el screener
registro = {
    'fecha': '2025-02-10',
    'ticker': 'AAPL',
    'ivr': 0.72,
    'precio_compra': 185.50,
    'precio_30d': 195.20,  # Llenar después
    'retorno': 5.2%         # Llenar después
}
```

---

## 🎓 Casos de Uso Avanzados

### 1. Rotación Sectorial
```python
# Lunes: Analizar TECH
# Martes: Analizar HEALTHCARE  
# Miércoles: Analizar FINANCIALS
# Jueves: Analizar ENERGY
# Viernes: Analizar CONSUMER

# Siempre tienes el sector más actualizado
```

### 2. Pairs Trading
```python
# Busca pares en mismo sector
# Compra el IVR alto
# Vende corto el IVR bajo
# Espera convergencia
```

### 3. Portfolio Rebalancing
```python
# Analiza tu portafolio actual
# Vende las con IVR < 0.30
# Compra las con IVR > 0.70
# Rebalancea cada trimestre
```

---

## 🛡️ Gestión de Riesgo

### Regla 1: Diversificación
- Nunca más del 20% en un solo ticker
- Mínimo 5 sectores diferentes
- Máximo 30% en un sector

### Regla 2: Stop Loss
```python
# Aunque IVR sea alto, vende si:
- Baja más del 15% desde compra
- IVR cae por debajo de 0.40
- Aparecen noticias negativas fundamentales
```

### Regla 3: Position Sizing
```python
if ivr >= 0.80:
    position = 5% del portafolio  # Alta convicción
elif ivr >= 0.70:
    position = 3% del portafolio  # Convicción media
elif ivr >= 0.60:
    position = 2% del portafolio  # Convicción baja
```

---

## 📊 Combinar con Análisis Manual

**El screener NO sustituye tu análisis**, lo complementa:

### Checklist Post-Señal
Cuando el screener da señal de compra:

1. ✅ **Lee el 10-K** (reporte anual)
2. ✅ **Escucha earnings call** más reciente
3. ✅ **Revisa noticias** últimos 30 días
4. ✅ **Analiza competencia** del sector
5. ✅ **Valida supuestos** del DCF
6. ✅ **Verifica insider trading** (compras de directivos)

**Solo entonces**: Decide si comprar

---

## 🔄 Mantenimiento del Sistema

### Semanal
- Revisa historial de alertas
- Verifica que emails lleguen
- Actualiza lista de tickers

### Mensual
- Analiza performance de señales
- Ajusta pesos si es necesario
- Limpia archivos antiguos

### Trimestral
- Revisa resultados vs benchmarks (S&P 500)
- Considera cambios estratégicos
- Actualiza documentación

---

## 🎯 Metas Realistas

### Primer Mes
- Familiarizarte con el sistema
- Generar primeras señales
- NO invertir dinero real aún

### Primeros 3 Meses
- Validar señales con paper trading
- Ajustar parámetros según resultados
- Empezar con capital pequeño

### Primeros 6 Meses
- Tener estrategia validada
- Aumentar capital gradualmente
- Documentar aprendizajes

**Expectativas**: 
- No te harás millonario en 1 mes
- El screener mejora tus probabilidades
- La disciplina es más importante que el algoritmo

---

## 💎 Tips Avanzados

1. **Combina con opciones**
   - IVR > 0.70: Vende puts (genera ingreso esperando comprar barato)
   - IVR < 0.30: Vende calls cubiertas

2. **Usa en bear markets**
   - En caídas, aumenta umbral_compra a 0.80
   - Espera liquidaciones extremas

3. **Aprovecha earnings season**
   - Post-earnings, volatilidad genera oportunidades
   - Ejecuta screener el día después de earnings

4. **Sectores cíclicos**
   - Energy: Mejor en ciclos alcistas
   - Utilities: Mejor en recesiones
   - Ajusta pesos según ciclo económico

---

## 📚 Recursos Adicionales

### Libros Recomendados
- "The Intelligent Investor" - Benjamin Graham
- "Common Stocks and Uncommon Profits" - Philip Fisher
- "One Up On Wall Street" - Peter Lynch

### Sitios Web Útiles
- SEC.gov (reportes oficiales)
- FINVIZ.com (screeners adicionales)
- GuruFocus.com (métricas de valuación)

### Comunidades
- r/ValueInvesting (Reddit)
- r/SecurityAnalysis (Reddit)
- Bogleheads Forum

---

**¡Buena suerte con tus inversiones! 🚀📈**

*Remember: "Time in the market beats timing the market"*
