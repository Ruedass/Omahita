"""
Scheduler Automático para Screener IVR
Ejecuta el screener cada X minutos y envía alertas
"""

import schedule
import time
from datetime import datetime
import pandas as pd
from screener_ivr import ScreenerIVR
from sistema_alertas import SistemaAlertas
import json
import os


class SchedulerScreener:
    """Ejecuta screener automáticamente en intervalos definidos"""
    
    def __init__(self, config_file='config_scheduler.json'):
        self.config_file = config_file
        self.config = self.cargar_config()
        self.screener = ScreenerIVR(pesos_personalizados=self.config['pesos'])
        self.sistema_alertas = SistemaAlertas()
        self.ultimo_resultado = None
    
    def cargar_config(self):
        """Cargar configuración del scheduler"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        return {
            'intervalo_minutos': 30,
            'tickers': [
                # Mega caps tech
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
                # Finance
                'JPM', 'BAC', 'WFC', 'GS', 'MS',
                # Consumer
                'WMT', 'HD', 'NKE', 'SBUX', 'MCD',
                # Healthcare
                'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO',
                # Industrials
                'CAT', 'BA', 'HON', 'UPS', 'GE'
            ],
            'pesos': {
                'valoracion': 0.60,
                'calidad': 0.30,
                'timing': 0.10
            },
            'guardar_historial': True,
            'enviar_alertas': True,
            'umbral_compra': 0.60,
            'umbral_venta': 0.30
        }
    
    def guardar_config(self):
        """Guardar configuración"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def ejecutar_screener(self):
        """Ejecutar el screener completo"""
        timestamp = datetime.now()
        print(f"\n{'='*80}")
        print(f"🔄 Ejecutando screener - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        try:
            # Escanear tickers
            df_resultados = self.screener.escanear_lista(self.config['tickers'])
            
            if df_resultados.empty:
                print("❌ No se obtuvieron resultados")
                return
            
            # Guardar resultado
            self.ultimo_resultado = df_resultados
            
            # Estadísticas
            total = len(df_resultados)
            pasan_filtros = df_resultados['pasa_filtros'].sum()
            señales_compra = (df_resultados['ivr'] >= self.config['umbral_compra']).sum()
            señales_venta = (df_resultados['ivr'] <= self.config['umbral_venta']).sum()
            
            print(f"\n📊 Resumen:")
            print(f"   Total analizados: {total}")
            print(f"   Pasan filtros: {pasan_filtros}")
            print(f"   🟢 Señales COMPRA: {señales_compra}")
            print(f"   🔴 Señales VENTA: {señales_venta}")
            
            # Top 3 oportunidades
            print(f"\n🏆 Top 3 por IVR:")
            for idx, row in df_resultados.head(3).iterrows():
                print(f"   {idx+1}. {row['ticker']} - IVR: {row['ivr']:.2%} - "
                      f"{'✅' if row['pasa_filtros'] else '❌'} - {row['nombre'][:30]}")
            
            # Guardar historial
            if self.config['guardar_historial']:
                self.guardar_historial(df_resultados, timestamp)
            
            # Enviar alertas si hay señales
            if self.config['enviar_alertas'] and (señales_compra > 0 or señales_venta > 0):
                print("\n📧 Enviando alertas por email...")
                self.sistema_alertas.enviar_alerta(df_resultados)
            
            print(f"\n✅ Screener completado exitosamente")
            
        except Exception as e:
            print(f"\n❌ Error ejecutando screener: {e}")
            import traceback
            traceback.print_exc()
    
    def guardar_historial(self, df, timestamp):
        """Guardar resultados en historial CSV"""
        historial_dir = 'historial_screener'
        os.makedirs(historial_dir, exist_ok=True)
        
        # Agregar timestamp
        df_con_timestamp = df.copy()
        df_con_timestamp['timestamp'] = timestamp
        
        # Guardar archivo diario
        fecha_str = timestamp.strftime('%Y%m%d')
        archivo_diario = os.path.join(historial_dir, f'screener_{fecha_str}.csv')
        
        if os.path.exists(archivo_diario):
            # Agregar al archivo existente
            df_existente = pd.read_csv(archivo_diario)
            df_combinado = pd.concat([df_existente, df_con_timestamp], ignore_index=True)
            df_combinado.to_csv(archivo_diario, index=False)
        else:
            # Crear nuevo archivo
            df_con_timestamp.to_csv(archivo_diario, index=False)
        
        print(f"   💾 Historial guardado en: {archivo_diario}")
    
    def iniciar_modo_automatico(self):
        """Iniciar ejecución automática según intervalo configurado"""
        intervalo = self.config['intervalo_minutos']
        
        print(f"\n🤖 Iniciando modo automático")
        print(f"⏱️  Intervalo: {intervalo} minutos")
        print(f"📋 Tickers a monitorear: {len(self.config['tickers'])}")
        print(f"📧 Alertas por email: {'✅ Activadas' if self.config['enviar_alertas'] else '❌ Desactivadas'}")
        print(f"\nPresiona Ctrl+C para detener\n")
        
        # Programar tarea
        schedule.every(intervalo).minutes.do(self.ejecutar_screener)
        
        # Ejecutar una vez inmediatamente
        self.ejecutar_screener()
        
        # Loop infinito
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Revisar cada 30 segundos
        except KeyboardInterrupt:
            print("\n\n🛑 Scheduler detenido por el usuario")
    
    def ejecutar_una_vez(self):
        """Ejecutar screener una sola vez (útil para testing)"""
        self.ejecutar_screener()
        return self.ultimo_resultado


def menu_interactivo():
    """Menú interactivo para configurar y ejecutar"""
    scheduler = SchedulerScreener()
    
    while True:
        print("\n" + "="*80)
        print("📊 SCREENER IVR - SCHEDULER AUTOMÁTICO")
        print("="*80)
        print("\n1. 🚀 Ejecutar screener UNA VEZ")
        print("2. 🤖 Iniciar modo AUTOMÁTICO (cada 30 min)")
        print("3. ⚙️  Configurar tickers")
        print("4. ⚙️  Configurar pesos del algoritmo")
        print("5. 📧 Configurar alertas por email")
        print("6. 📊 Ver último resultado")
        print("7. 📈 Ver historial")
        print("8. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            scheduler.ejecutar_una_vez()
        
        elif opcion == '2':
            scheduler.iniciar_modo_automatico()
        
        elif opcion == '3':
            print("\nTickers actuales:")
            print(", ".join(scheduler.config['tickers']))
            nuevo = input("\nIngresa nuevos tickers (separados por coma) o Enter para mantener: ").strip()
            if nuevo:
                scheduler.config['tickers'] = [t.strip().upper() for t in nuevo.split(',')]
                scheduler.guardar_config()
                print("✅ Tickers actualizados")
        
        elif opcion == '4':
            print("\nPesos actuales:")
            print(f"  Valoración: {scheduler.config['pesos']['valoracion']:.0%}")
            print(f"  Calidad: {scheduler.config['pesos']['calidad']:.0%}")
            print(f"  Timing: {scheduler.config['pesos']['timing']:.0%}")
            
            try:
                val = float(input("\nNuevo peso Valoración (0-1): "))
                cal = float(input("Nuevo peso Calidad (0-1): "))
                tim = float(input("Nuevo peso Timing (0-1): "))
                
                total = val + cal + tim
                scheduler.config['pesos'] = {
                    'valoracion': val / total,
                    'calidad': cal / total,
                    'timing': tim / total
                }
                scheduler.screener = ScreenerIVR(scheduler.config['pesos'])
                scheduler.guardar_config()
                print("✅ Pesos actualizados y normalizados")
            except:
                print("❌ Error en los valores ingresados")
        
        elif opcion == '5':
            print("\n📧 Configuración de Alertas por Email")
            print("\nPara Gmail necesitas:")
            print("1. Activar verificación en 2 pasos")
            print("2. Generar 'Contraseña de aplicación'")
            print("3. Usar esa contraseña (NO tu contraseña normal)")
            
            destino = input("\nEmail destino: ").strip()
            origen = input("Email origen (Gmail): ").strip()
            password = input("Contraseña de aplicación: ").strip()
            
            if destino and origen and password:
                scheduler.sistema_alertas.configurar_email(destino, origen, password)
                scheduler.config['enviar_alertas'] = True
                scheduler.guardar_config()
                
                test = input("\n¿Enviar email de prueba? (s/n): ").strip().lower()
                if test == 's':
                    scheduler.sistema_alertas.test_email()
            else:
                print("❌ Configuración incompleta")
        
        elif opcion == '6':
            if scheduler.ultimo_resultado is not None:
                print("\n" + "="*80)
                print("📊 ÚLTIMO RESULTADO")
                print("="*80)
                df = scheduler.ultimo_resultado
                print(df[['ticker', 'nombre', 'ivr', 'pasa_filtros']].head(10))
            else:
                print("\n⚠️  No hay resultados aún. Ejecuta el screener primero.")
        
        elif opcion == '7':
            historial_dir = 'historial_screener'
            if os.path.exists(historial_dir):
                archivos = sorted(os.listdir(historial_dir))
                if archivos:
                    print("\n📈 Archivos de historial:")
                    for i, archivo in enumerate(archivos[-5:], 1):  # Últimos 5
                        print(f"  {i}. {archivo}")
                else:
                    print("\n⚠️  No hay historial guardado")
            else:
                print("\n⚠️  No hay historial guardado")
        
        elif opcion == '8':
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida")


if __name__ == "__main__":
    menu_interactivo()
