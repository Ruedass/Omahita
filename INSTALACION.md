# 🚀 Guía Rápida de Instalación

## ⚡ Opción 1: Cloud (MÁS RÁPIDO - Sin instalar nada)

### Streamlit Cloud (100% Gratis)

1. **Sube el código a GitHub**
   - Crea un repositorio en GitHub
   - Sube todos estos archivos

2. **Deploy en Streamlit**
   - Ve a https://streamlit.io/cloud
   - Conecta tu cuenta GitHub
   - Selecciona tu repositorio
   - Main file: `app_screener.py`
   - ¡Click Deploy!

3. **¡Listo!**
   - Obtendrás una URL tipo: `https://tu-screener.streamlit.app`
   - Accesible desde cualquier dispositivo
   - Actualización automática cada que hagas cambios

**Tiempo estimado: 5 minutos**

---

## 💻 Opción 2: Local (En tu computadora)

### Windows

1. **Instalar Python**
   ```
   Descarga Python 3.11 de https://www.python.org/downloads/
   ⚠️ Marca "Add Python to PATH" durante instalación
   ```

2. **Abrir PowerShell o CMD**
   ```
   Presiona Win + R
   Escribe: cmd
   Enter
   ```

3. **Navegar a la carpeta del proyecto**
   ```bash
   cd ruta\donde\descargaste\el\proyecto
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar**
   ```bash
   # Interfaz web
   streamlit run app_screener.py
   
   # O modo consola
   python ejemplo_uso.py
   ```

**Tiempo estimado: 10 minutos**

### Mac / Linux

1. **Abrir Terminal**

2. **Navegar al proyecto**
   ```bash
   cd /ruta/al/proyecto
   ```

3. **Instalar dependencias**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Ejecutar**
   ```bash
   # Interfaz web
   streamlit run app_screener.py
   
   # O ejemplo simple
   python3 ejemplo_uso.py
   ```

**Tiempo estimado: 5 minutos**

---

## 📧 Configurar Alertas por Email (Opcional)

### Gmail (Recomendado)

1. **Activar verificación en 2 pasos**
   - Ve a: https://myaccount.google.com/security
   - Activa "Verificación en 2 pasos"

2. **Generar contraseña de aplicación**
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Windows/Mac/Linux"
   - Copia la contraseña de 16 caracteres

3. **Configurar en el screener**
   
   **Opción A - Interfaz web**:
   - Sidebar → Email Settings
   - Pega email y contraseña
   
   **Opción B - Consola**:
   ```bash
   python scheduler_screener.py
   # Opción 5: Configurar alertas
   ```
   
   **Opción C - Editar archivo**:
   Crea `config_alertas.json`:
   ```json
   {
     "email_destino": "tu_email@gmail.com",
     "email_origen": "origen@gmail.com",
     "password": "xxxx xxxx xxxx xxxx",
     "alertas_activas": true
   }
   ```

**Tiempo estimado: 5 minutos**

---

## ✅ Verificar Instalación

```bash
# Test básico
python ejemplo_uso.py

# Si funciona, deberías ver:
# - Lista de mega caps analizadas
# - IVR scores
# - Señales de compra/venta
```

---

## 🎯 Primeros Pasos

### 1. Ejecutar Ejemplo
```bash
python ejemplo_uso.py
```

### 2. Interfaz Web
```bash
streamlit run app_screener.py
```

### 3. Modo Automático
```bash
python scheduler_screener.py
```

---

## ❓ Problemas Comunes

### Error: "Python no reconocido"
**Windows**: Reinstala Python y marca "Add to PATH"
**Mac/Linux**: Usa `python3` en vez de `python`

### Error: "pip no reconocido"
```bash
python -m pip install -r requirements.txt
```

### Error: "No module named X"
```bash
pip install yfinance pandas streamlit plotly schedule
```

### Streamlit no abre navegador
```bash
streamlit run app_screener.py --server.headless false
```

### Yahoo Finance muy lento
- Reduce cantidad de tickers
- Aumenta intervalo entre ejecuciones
- Usa horario fuera de market hours

---

## 📞 Soporte

¿Problemas? Abre un issue en GitHub o contacta al desarrollador.

---

## 🎉 ¡Listo para Invertir!

Ya tienes tu screener funcionando. Ahora:

1. ✅ Personaliza los pesos según tu estrategia
2. ✅ Agrega tus tickers favoritos
3. ✅ Configura alertas automáticas
4. ✅ ¡Encuentra oportunidades de valor!

**"El precio es lo que pagas, el valor es lo que obtienes"** - Warren Buffett
