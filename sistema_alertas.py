"""
Sistema de Alertas Automáticas
Envía emails cuando se detectan señales de compra/venta
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os


class SistemaAlertas:
    """Gestiona alertas por email"""
    
    def __init__(self, config_file='config_alertas.json'):
        self.config_file = config_file
        self.config = self.cargar_config()
    
    def cargar_config(self):
        """Cargar configuración de alertas"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        # Configuración por defecto
        return {
            'email_destino': '',  # Usuario debe configurar
            'email_origen': '',   # Gmail para envío
            'password': '',       # App password de Gmail
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'alertas_activas': True,
            'umbral_compra': 0.60,
            'umbral_venta': 0.30,
            'ultima_alerta': None
        }
    
    def guardar_config(self):
        """Guardar configuración"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configurar_email(self, email_destino, email_origen, password):
        """Configurar credenciales de email"""
        self.config['email_destino'] = email_destino
        self.config['email_origen'] = email_origen
        self.config['password'] = password
        self.guardar_config()
    
    def generar_html_alerta(self, alertas_compra, alertas_venta, timestamp):
        """Generar HTML para email de alerta"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px; }}
                .buy {{ background-color: #d4edda; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .sell {{ background-color: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .ticker {{ font-weight: bold; font-size: 1.2em; }}
                .metric {{ margin: 5px 0; }}
                .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Screener IVR - Alertas Automáticas</h1>
                <p>Actualización: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Alertas de COMPRA
        if alertas_compra:
            html += f"""
            <div class="section">
                <h2>🟢 SEÑALES DE COMPRA ({len(alertas_compra)})</h2>
            """
            for alerta in alertas_compra:
                html += f"""
                <div class="buy">
                    <div class="ticker">{alerta['ticker']} - {alerta['nombre']}</div>
                    <div class="metric">IVR: <strong>{alerta['ivr']:.2%}</strong></div>
                    <div class="metric">Precio: ${alerta['precio']:.2f}</div>
                    <div class="metric">Valor Intrínseco: ${alerta['valor_intrinseco']:.2f}</div>
                    <div class="metric">Margen Seguridad: {alerta['margen_seguridad']:.2%}</div>
                    <div class="metric">Sector: {alerta['sector']}</div>
                </div>
                """
            html += "</div>"
        
        # Alertas de VENTA
        if alertas_venta:
            html += f"""
            <div class="section">
                <h2>🔴 SEÑALES DE VENTA ({len(alertas_venta)})</h2>
            """
            for alerta in alertas_venta:
                html += f"""
                <div class="sell">
                    <div class="ticker">{alerta['ticker']} - {alerta['nombre']}</div>
                    <div class="metric">IVR: <strong>{alerta['ivr']:.2%}</strong></div>
                    <div class="metric">Precio: ${alerta['precio']:.2f}</div>
                </div>
                """
            html += "</div>"
        
        html += """
            <div class="footer">
                <p>Este es un mensaje automático del Screener IVR</p>
                <p>No responder a este email</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def enviar_alerta(self, df_resultados):
        """
        Enviar email con alertas si se detectan señales
        
        Args:
            df_resultados: DataFrame con resultados del screener
        """
        if not self.config['alertas_activas']:
            print("Alertas desactivadas")
            return False
        
        if not self.config['email_destino'] or not self.config['email_origen']:
            print("Email no configurado")
            return False
        
        # Filtrar alertas
        alertas_compra = df_resultados[
            df_resultados['ivr'] >= self.config['umbral_compra']
        ].to_dict('records')
        
        alertas_venta = df_resultados[
            df_resultados['ivr'] <= self.config['umbral_venta']
        ].to_dict('records')
        
        # Si no hay alertas, no enviar
        if not alertas_compra and not alertas_venta:
            print("No hay alertas para enviar")
            return False
        
        try:
            # Crear mensaje
            timestamp = datetime.now()
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 Screener IVR - {len(alertas_compra)} compras, {len(alertas_venta)} ventas"
            msg['From'] = self.config['email_origen']
            msg['To'] = self.config['email_destino']
            
            # HTML body
            html_content = self.generar_html_alerta(alertas_compra, alertas_venta, timestamp)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Enviar email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email_origen'], self.config['password'])
            server.send_message(msg)
            server.quit()
            
            # Actualizar última alerta
            self.config['ultima_alerta'] = timestamp.isoformat()
            self.guardar_config()
            
            print(f"✅ Alerta enviada exitosamente a {self.config['email_destino']}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando alerta: {e}")
            return False
    
    def test_email(self):
        """Enviar email de prueba"""
        try:
            msg = MIMEText("Este es un email de prueba del Screener IVR")
            msg['Subject'] = "🧪 Test - Screener IVR"
            msg['From'] = self.config['email_origen']
            msg['To'] = self.config['email_destino']
            
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email_origen'], self.config['password'])
            server.send_message(msg)
            server.quit()
            
            print("✅ Email de prueba enviado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error en email de prueba: {e}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    """
    IMPORTANTE: Para usar Gmail necesitas:
    1. Activar verificación en 2 pasos en tu cuenta Google
    2. Generar una "Contraseña de aplicación" específica
    3. Usar esa contraseña aquí (NO tu contraseña normal de Gmail)
    
    Guía: https://support.google.com/accounts/answer/185833
    """
    
    sistema = SistemaAlertas()
    
    # Configurar (solo primera vez)
    # sistema.configurar_email(
    #     email_destino='tu_email@gmail.com',
    #     email_origen='email_origen@gmail.com', 
    #     password='tu_app_password_aqui'
    # )
    
    # Test
    # sistema.test_email()
    
    print("Sistema de alertas listo")
    print(f"Configuración actual: {sistema.config}")
