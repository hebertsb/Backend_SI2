# GUÍA DE PLANTILLAS Y CONFIGURACIÓN DE CANALES

## Introducción

Esta guía describe el sistema completo de plantillas para notificaciones, configuración de canales de envío (email, SMS, push, in-app) y las mejores prácticas para implementar un sistema de comunicaciones robusto y personalizable.

## 1. SISTEMA DE PLANTILLAS

### 1.1 Arquitectura de Plantillas

```python
# Modelo de Plantilla
class PlantillaNotificacion(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_notificacion = models.CharField(max_length=50, choices=TIPOS_NOTIFICACION)
    canal = models.CharField(max_length=20, choices=CANALES)
    idioma = models.CharField(max_length=5, default='es')
    version = models.CharField(max_length=10, default='1.0')
    
    # Contenido de la plantilla
    asunto = models.CharField(max_length=200, blank=True)  # Para email
    contenido_html = models.TextField(blank=True)
    contenido_texto = models.TextField()
    contenido_json = models.JSONField(blank=True, null=True)  # Para push/in-app
    
    # Configuración
    variables_requeridas = models.JSONField(default=list)
    variables_opcionales = models.JSONField(default=list)
    activa = models.BooleanField(default=True)
    es_predeterminada = models.BooleanField(default=False)
    
    # Metadatos
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['tipo_notificacion', 'canal', 'idioma', 'es_predeterminada']
```

### 1.2 Motor de Renderizado

```python
from jinja2 import Environment, BaseLoader, TemplateError
import json

class NotificationTemplateEngine:
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
        self.env.globals['formatear_fecha'] = self.formatear_fecha
        self.env.globals['formatear_moneda'] = self.formatear_moneda
        self.env.globals['pluralizar'] = self.pluralizar
    
    def renderizar_plantilla(self, plantilla, datos):
        """Renderiza una plantilla con los datos proporcionados"""
        try:
            # Renderizar asunto
            asunto_renderizado = None
            if plantilla.asunto:
                template_asunto = self.env.from_string(plantilla.asunto)
                asunto_renderizado = template_asunto.render(**datos)
            
            # Renderizar contenido HTML
            contenido_html_renderizado = None
            if plantilla.contenido_html:
                template_html = self.env.from_string(plantilla.contenido_html)
                contenido_html_renderizado = template_html.render(**datos)
            
            # Renderizar contenido texto
            template_texto = self.env.from_string(plantilla.contenido_texto)
            contenido_texto_renderizado = template_texto.render(**datos)
            
            # Renderizar contenido JSON (para push/in-app)
            contenido_json_renderizado = None
            if plantilla.contenido_json:
                template_json = self.env.from_string(json.dumps(plantilla.contenido_json))
                contenido_json_str = template_json.render(**datos)
                contenido_json_renderizado = json.loads(contenido_json_str)
            
            return {
                'asunto': asunto_renderizado,
                'contenido_html': contenido_html_renderizado,
                'contenido_texto': contenido_texto_renderizado,
                'contenido_json': contenido_json_renderizado
            }
            
        except TemplateError as e:
            raise ValueError(f"Error renderizando plantilla: {str(e)}")
    
    def validar_variables(self, plantilla, datos):
        """Valida que todas las variables requeridas estén presentes"""
        variables_faltantes = []
        for variable in plantilla.variables_requeridas:
            if variable not in datos or datos[variable] is None:
                variables_faltantes.append(variable)
        
        if variables_faltantes:
            raise ValueError(f"Variables requeridas faltantes: {', '.join(variables_faltantes)}")
    
    def formatear_fecha(self, fecha, formato='%d/%m/%Y'):
        """Formatea fechas para plantillas"""
        if isinstance(fecha, str):
            from datetime import datetime
            fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
        return fecha.strftime(formato)
    
    def formatear_moneda(self, monto, moneda='BOB'):
        """Formatea montos monetarios"""
        return f"{monto:,.2f} {moneda}"
    
    def pluralizar(self, cantidad, singular, plural):
        """Pluralización inteligente"""
        return singular if cantidad == 1 else plural
```

### 1.3 Plantillas por Tipo de Notificación

#### Email - Confirmación de Reserva
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{asunto}}</title>
    <style>
        .container {
            max-width: 600px;
            margin: 0 auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff;
        }
        .header {
            background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }
        .content {
            padding: 30px 20px;
            line-height: 1.6;
            color: #333;
        }
        .reservation-card {
            background-color: #f8f9fa;
            border-left: 4px solid #1890ff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 5px 0;
            border-bottom: 1px solid #e8e8e8;
        }
        .detail-label {
            font-weight: 600;
            color: #666;
        }
        .detail-value {
            color: #333;
        }
        .button {
            display: inline-block;
            background-color: #52c41a;
            color: white !important;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin: 20px 0;
            text-align: center;
        }
        .button:hover {
            background-color: #389e0d;
        }
        .services-list {
            list-style: none;
            padding: 0;
        }
        .services-list li {
            padding: 5px 0;
            color: #52c41a;
        }
        .services-list li:before {
            content: "✓ ";
            font-weight: bold;
        }
        .footer {
            background-color: #001529;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 14px;
        }
        .qr-code {
            text-align: center;
            margin: 20px 0;
        }
        .warning-box {
            background-color: #fff7e6;
            border: 1px solid #ffd591;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
        .warning-box h4 {
            color: #fa8c16;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 ¡Reserva Confirmada!</h1>
        </div>
        
        <div class="content">
            <p>Estimado/a <strong>{{nombre_cliente}}</strong>,</p>
            
            <p>Nos complace confirmar que su reserva ha sido procesada exitosamente. A continuación encontrará todos los detalles de su estadía:</p>
            
            <div class="reservation-card">
                <h3 style="margin-top: 0; color: #1890ff;">{{hotel_nombre}}</h3>
                
                <div class="detail-row">
                    <span class="detail-label">Número de Confirmación:</span>
                    <span class="detail-value"><strong>{{numero_confirmacion}}</strong></span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Check-in:</span>
                    <span class="detail-value">{{formatear_fecha(fecha_checkin, '%A, %d de %B de %Y')}} a las {{hora_checkin}}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Check-out:</span>
                    <span class="detail-value">{{formatear_fecha(fecha_checkout, '%A, %d de %B de %Y')}} a las {{hora_checkout}}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Tipo de Habitación:</span>
                    <span class="detail-value">{{tipo_habitacion}}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Huéspedes:</span>
                    <span class="detail-value">{{numero_huespedes}} {{pluralizar(numero_huespedes, 'persona', 'personas')}}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Total Pagado:</span>
                    <span class="detail-value"><strong>{{formatear_moneda(monto_total, moneda)}}</strong></span>
                </div>
            </div>
            
            {% if servicios_incluidos %}
            <h4>Servicios Incluidos:</h4>
            <ul class="services-list">
                {% for servicio in servicios_incluidos %}
                <li>{{servicio}}</li>
                {% endfor %}
            </ul>
            {% endif %}
            
            <div class="qr-code">
                <h4>Código QR para Check-in Rápido</h4>
                {% if codigo_qr_checkin %}
                <img src="{{codigo_qr_checkin}}" alt="Código QR" style="max-width: 150px;">
                {% endif %}
                <p style="font-size: 12px; color: #666;">Presente este código en recepción para un check-in más rápido</p>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Información Importante</h4>
                <p><strong>Política de Cancelación:</strong> {{politicas_cancelacion}}</p>
                {% if instrucciones_especiales %}
                <p><strong>Instrucciones Especiales:</strong> {{instrucciones_especiales}}</p>
                {% endif %}
            </div>
            
            <div style="text-align: center;">
                <a href="{{enlace_gestion}}" class="button">Gestionar mi Reserva</a>
            </div>
            
            <p>El hotel se pondrá en contacto con usted dentro de las próximas 2 horas para confirmar los detalles adicionales.</p>
            
            <p><strong>Información de Contacto del Hotel:</strong><br>
            📍 {{hotel_direccion}}<br>
            📞 {{hotel_telefono}}</p>
            
            <p>¡Esperamos que disfrute su estadía!</p>
        </div>
        
        <div class="footer">
            <p><strong>Sistema de Reservas</strong></p>
            <p>📞 +591-3-1234567 | ✉️ soporte@reservas.com</p>
            <p>Lunes a Domingo, 24/7</p>
            <p style="margin-top: 15px; font-size: 12px;">
                © 2024 Sistema de Reservas. Todos los derechos reservados.
            </p>
        </div>
    </div>
</body>
</html>
```

#### SMS - Recordatorio
```text
Hola {{nombre_cliente}}! 👋 

Su check-in en {{hotel_nombre}} es {{formatear_fecha(fecha_checkin, 'mañana')}} a las {{hora_checkin}}.

📋 Documentos necesarios:
- Cédula/Pasaporte
- Confirmación: {{numero_confirmacion}}

📍 {{hotel_direccion}}
📞 {{hotel_telefono}}

¿Preguntas? Responda HELP
Gestionar: {{enlace_corto}}
```

#### Push Notification - Reprogramación
```json
{
  "title": "{{titulo}}",
  "body": "{{mensaje_corto}}",
  "icon": "https://reservas.com/icons/notification.png",
  "badge": "https://reservas.com/icons/badge.png",
  "data": {
    "type": "{{tipo_notificacion}}",
    "reserva_id": "{{reserva_id}}",
    "action_url": "{{url_accion}}",
    "priority": "{{prioridad}}",
    "timestamp": "{{timestamp}}"
  },
  "actions": [
    {
      "action": "view",
      "title": "Ver Detalles",
      "url": "{{url_accion}}"
    },
    {
      "action": "dismiss",
      "title": "Cerrar"
    }
  ],
  "requireInteraction": {% if prioridad == 'urgente' %}true{% else %}false{% endif %},
  "silent": false,
  "vibrate": [200, 100, 200]
}
```

## 2. CONFIGURACIÓN DE CANALES

### 2.1 Configuración Email (SendGrid)

```python
# settings.py
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-sendgrid-api-key'

# Configuración específica
EMAIL_CONFIG = {
    'provider': 'sendgrid',
    'settings': {
        'api_key': os.getenv('SENDGRID_API_KEY'),
        'default_from_email': 'noreply@reservas.com',
        'default_from_name': 'Sistema de Reservas',
        'tracking': {
            'click_tracking': True,
            'open_tracking': True,
            'subscription_tracking': False
        },
        'limits': {
            'daily_limit': 10000,
            'hourly_limit': 1000,
            'per_user_daily': 50
        },
        'retry': {
            'max_attempts': 3,
            'base_delay': 300,  # 5 minutos
            'max_delay': 3600   # 1 hora
        }
    }
}

# Clase para manejo de emails
class EmailService:
    def __init__(self):
        self.client = sendgrid.SendGridAPIClient(api_key=EMAIL_CONFIG['settings']['api_key'])
    
    def enviar_email(self, destinatario, asunto, contenido_html, contenido_texto, datos_tracking=None):
        """Envía email usando SendGrid"""
        try:
            message = Mail(
                from_email=From(
                    EMAIL_CONFIG['settings']['default_from_email'],
                    EMAIL_CONFIG['settings']['default_from_name']
                ),
                to_emails=destinatario,
                subject=asunto,
                html_content=contenido_html,
                plain_text_content=contenido_texto
            )
            
            # Configurar tracking
            if EMAIL_CONFIG['settings']['tracking']['click_tracking']:
                message.tracking_settings = TrackingSettings()
                message.tracking_settings.click_tracking = ClickTracking(True, True)
            
            if EMAIL_CONFIG['settings']['tracking']['open_tracking']:
                message.tracking_settings.open_tracking = OpenTracking(True)
            
            # Añadir custom args para tracking
            if datos_tracking:
                message.custom_args = datos_tracking
            
            response = self.client.send(message)
            
            return {
                'success': True,
                'message_id': response.headers.get('X-Message-Id'),
                'status_code': response.status_code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
```

### 2.2 Configuración SMS (Twilio)

```python
from twilio.rest import Client

SMS_CONFIG = {
    'provider': 'twilio',
    'settings': {
        'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
        'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
        'from_number': '+59173456789',
        'limits': {
            'daily_limit': 5000,
            'hourly_limit': 500,
            'per_user_daily': 20,
            'character_limit': 160
        },
        'retry': {
            'max_attempts': 2,
            'base_delay': 60,
            'max_delay': 300
        },
        'url_shortener': {
            'enabled': True,
            'service': 'bitly',
            'api_key': os.getenv('BITLY_API_KEY')
        }
    }
}

class SMSService:
    def __init__(self):
        self.client = Client(
            SMS_CONFIG['settings']['account_sid'],
            SMS_CONFIG['settings']['auth_token']
        )
        self.url_shortener = URLShortenerService()
    
    def enviar_sms(self, destinatario, mensaje, datos_tracking=None):
        """Envía SMS usando Twilio"""
        try:
            # Acortar URLs si es necesario
            if SMS_CONFIG['settings']['url_shortener']['enabled']:
                mensaje = self.url_shortener.acortar_urls_en_texto(mensaje)
            
            # Verificar límite de caracteres
            if len(mensaje) > SMS_CONFIG['settings']['limits']['character_limit']:
                return {
                    'success': False,
                    'error': f'Mensaje excede el límite de {SMS_CONFIG["settings"]["limits"]["character_limit"]} caracteres'
                }
            
            message = self.client.messages.create(
                body=mensaje,
                from_=SMS_CONFIG['settings']['from_number'],
                to=destinatario,
                status_callback='https://reservas.com/sms/webhook/status'
            )
            
            return {
                'success': True,
                'message_sid': message.sid,
                'status': message.status
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
```

### 2.3 Configuración Push Notifications (Firebase)

```python
import firebase_admin
from firebase_admin import messaging

PUSH_CONFIG = {
    'provider': 'firebase',
    'settings': {
        'credentials_path': 'path/to/firebase-credentials.json',
        'limits': {
            'daily_limit': 100000,
            'hourly_limit': 10000,
            'per_user_daily': 100,
            'payload_max_size': 4096  # 4KB
        },
        'retry': {
            'max_attempts': 3,
            'base_delay': 30,
            'max_delay': 300
        }
    }
}

class PushNotificationService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = firebase_admin.credentials.Certificate(
                PUSH_CONFIG['settings']['credentials_path']
            )
            firebase_admin.initialize_app(cred)
    
    def enviar_push(self, tokens, titulo, mensaje, datos_adicionales=None, acciones=None):
        """Envía push notification usando Firebase"""
        try:
            # Construir el mensaje
            notification = messaging.Notification(
                title=titulo,
                body=mensaje
            )
            
            # Configurar datos adicionales
            data = datos_adicionales or {}
            
            # Configurar acciones específicas para Android
            android_config = None
            if acciones:
                android_config = messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        click_action='FLUTTER_NOTIFICATION_CLICK'
                    )
                )
            
            # Crear mensaje multicast
            message = messaging.MulticastMessage(
                notification=notification,
                data=data,
                tokens=tokens,
                android=android_config
            )
            
            # Enviar
            response = messaging.send_multicast(message)
            
            return {
                'success': True,
                'success_count': response.success_count,
                'failure_count': response.failure_count,
                'responses': response.responses
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
```

### 2.4 Configuración In-App Notifications

```python
# WebSocket consumer para notificaciones en tiempo real
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'notifications_{self.user_id}'
        
        # Unirse al grupo de notificaciones del usuario
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar notificaciones no leídas al conectar
        await self.send_unread_notifications()
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'mark_read':
            await self.mark_notification_read(data['notification_id'])
        elif data['type'] == 'mark_all_read':
            await self.mark_all_notifications_read()
    
    async def notification_message(self, event):
        """Envía notificación al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def send_unread_notifications(self):
        from .models import Notificacion
        unread = Notificacion.objects.filter(
            usuario_id=self.user_id,
            estado__in=['enviada', 'entregada']
        ).order_by('-created_at')[:10]
        
        for notification in unread:
            self.send(text_data=json.dumps({
                'type': 'notification',
                'data': {
                    'id': notification.id,
                    'titulo': notification.titulo,
                    'mensaje': notification.mensaje,
                    'tipo': notification.tipo_notificacion,
                    'created_at': notification.created_at.isoformat()
                }
            }))
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        from .models import Notificacion
        from django.utils import timezone
        
        Notificacion.objects.filter(
            id=notification_id,
            usuario_id=self.user_id
        ).update(
            estado='leida',
            leida_en=timezone.now()
        )
```

## 3. SISTEMA DE COLAS Y PROCESAMIENTO

### 3.1 Configuración Celery

```python
# celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('notifications')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configuración de colas
app.conf.task_routes = {
    'notifications.tasks.enviar_email': {'queue': 'email'},
    'notifications.tasks.enviar_sms': {'queue': 'sms'},
    'notifications.tasks.enviar_push': {'queue': 'push'},
    'notifications.tasks.enviar_masivo': {'queue': 'bulk'},
}

app.conf.task_annotations = {
    'notifications.tasks.enviar_email': {'rate_limit': '100/m'},
    'notifications.tasks.enviar_sms': {'rate_limit': '50/m'},
    'notifications.tasks.enviar_push': {'rate_limit': '1000/m'},
}

# Tasks
from celery import shared_task
from .services import EmailService, SMSService, PushNotificationService
from .models import Notificacion

@shared_task(bind=True, max_retries=3)
def procesar_notificacion(self, notificacion_id):
    """Procesa una notificación individual"""
    try:
        notificacion = Notificacion.objects.get(id=notificacion_id)
        
        # Renderizar plantilla
        contenido = renderizar_plantilla_notificacion(notificacion)
        
        # Enviar según el canal
        if notificacion.canal == 'email':
            resultado = EmailService().enviar_email(
                notificacion.usuario.email,
                contenido['asunto'],
                contenido['contenido_html'],
                contenido['contenido_texto']
            )
        elif notificacion.canal == 'sms':
            resultado = SMSService().enviar_sms(
                notificacion.usuario.telefono,
                contenido['contenido_texto']
            )
        elif notificacion.canal == 'push':
            resultado = PushNotificationService().enviar_push(
                [notificacion.usuario.fcm_token],
                notificacion.titulo,
                contenido['contenido_texto']
            )
        
        # Actualizar estado
        if resultado['success']:
            notificacion.estado = 'enviada'
            notificacion.enviada_en = timezone.now()
            notificacion.metadatos = resultado
        else:
            notificacion.estado = 'fallida'
            notificacion.ultimo_error = resultado['error']
            notificacion.intentos_envio += 1
        
        notificacion.save()
        
        return resultado
        
    except Exception as e:
        # Retry logic
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        else:
            notificacion.estado = 'fallida'
            notificacion.ultimo_error = str(e)
            notificacion.save()
            raise
```

## 4. PANEL DE ADMINISTRACIÓN DE PLANTILLAS

### 4.1 Componente React para Gestión

```javascript
import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Select, Button, Tabs, Switch, Table, Modal, message } from 'antd';
import { CodeEditor } from '@/components/CodeEditor';

const { TextArea } = Input;
const { TabPane } = Tabs;
const { Option } = Select;

const GestionPlantillas = () => {
  const [plantillas, setPlantillas] = useState([]);
  const [plantillaActual, setPlantillaActual] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [previewModal, setPreviewModal] = useState(false);
  const [previewContent, setPreviewContent] = useState({});

  useEffect(() => {
    cargarPlantillas();
  }, []);

  const cargarPlantillas = async () => {
    try {
      const response = await fetch('/api/notificaciones/plantillas/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setPlantillas(data.results);
    } catch (error) {
      message.error('Error cargando plantillas');
    }
  };

  const guardarPlantilla = async (values) => {
    try {
      const url = plantillaActual.id 
        ? `/api/notificaciones/plantillas/${plantillaActual.id}/`
        : '/api/notificaciones/plantillas/';
      
      const method = plantillaActual.id ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        message.success('Plantilla guardada exitosamente');
        setModalVisible(false);
        cargarPlantillas();
        form.resetFields();
      }
    } catch (error) {
      message.error('Error guardando plantilla');
    }
  };

  const previsualizarPlantilla = async (plantilla) => {
    try {
      const response = await fetch(`/api/notificaciones/plantillas/${plantilla.id}/preview/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          datos_muestra: {
            nombre_cliente: 'Juan Pérez',
            hotel_nombre: 'Hotel Paradise',
            numero_confirmacion: 'CNF123456',
            fecha_checkin: '2024-03-15',
            monto_total: '1,500.00',
            moneda: 'BOB'
          }
        })
      });

      const data = await response.json();
      setPreviewContent(data);
      setPreviewModal(true);
    } catch (error) {
      message.error('Error generando vista previa');
    }
  };

  const columnas = [
    {
      title: 'Nombre',
      dataIndex: 'nombre',
      key: 'nombre'
    },
    {
      title: 'Tipo',
      dataIndex: 'tipo_notificacion',
      key: 'tipo_notificacion'
    },
    {
      title: 'Canal',
      dataIndex: 'canal',
      key: 'canal',
      render: (canal) => (
        <span style={{ 
          color: canal === 'email' ? '#1890ff' : 
                canal === 'sms' ? '#52c41a' : 
                canal === 'push' ? '#fa8c16' : '#666'
        }}>
          {canal.toUpperCase()}
        </span>
      )
    },
    {
      title: 'Idioma',
      dataIndex: 'idioma',
      key: 'idioma'
    },
    {
      title: 'Estado',
      dataIndex: 'activa',
      key: 'activa',
      render: (activa) => (
        <Switch checked={activa} disabled />
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <div>
          <Button 
            size="small" 
            onClick={() => {
              setPlantillaActual(record);
              form.setFieldsValue(record);
              setModalVisible(true);
            }}
          >
            Editar
          </Button>
          <Button 
            size="small" 
            style={{ marginLeft: 8 }}
            onClick={() => previsualizarPlantilla(record)}
          >
            Vista Previa
          </Button>
        </div>
      )
    }
  ];

  return (
    <div>
      <Card 
        title="Gestión de Plantillas de Notificaciones"
        extra={
          <Button 
            type="primary" 
            onClick={() => {
              setPlantillaActual({});
              form.resetFields();
              setModalVisible(true);
            }}
          >
            Nueva Plantilla
          </Button>
        }
      >
        <Table 
          dataSource={plantillas} 
          columns={columnas} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={plantillaActual.id ? 'Editar Plantilla' : 'Nueva Plantilla'}
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={900}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={guardarPlantilla}
        >
          <Form.Item
            name="nombre"
            label="Nombre de la Plantilla"
            rules={[{ required: true, message: 'Nombre requerido' }]}
          >
            <Input placeholder="Ej: Confirmación de Reserva Email" />
          </Form.Item>

          <div style={{ display: 'flex', gap: '16px' }}>
            <Form.Item
              name="tipo_notificacion"
              label="Tipo"
              style={{ flex: 1 }}
              rules={[{ required: true, message: 'Tipo requerido' }]}
            >
              <Select placeholder="Seleccionar tipo">
                <Option value="reserva_confirmada">Reserva Confirmada</Option>
                <Option value="recordatorio_checkin">Recordatorio Check-in</Option>
                <Option value="reprogramacion_aprobada">Reprogramación Aprobada</Option>
                <Option value="promocion_personalizada">Promoción</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="canal"
              label="Canal"
              style={{ flex: 1 }}
              rules={[{ required: true, message: 'Canal requerido' }]}
            >
              <Select placeholder="Seleccionar canal">
                <Option value="email">Email</Option>
                <Option value="sms">SMS</Option>
                <Option value="push">Push</Option>
                <Option value="in_app">In-App</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="idioma"
              label="Idioma"
              style={{ flex: 1 }}
            >
              <Select defaultValue="es">
                <Option value="es">Español</Option>
                <Option value="en">English</Option>
              </Select>
            </Form.Item>
          </div>

          <Tabs defaultActiveKey="contenido">
            <TabPane tab="Contenido" key="contenido">
              <Form.Item
                name="asunto"
                label="Asunto (solo para email)"
              >
                <Input placeholder="{{hotel_nombre}} - Confirmación de Reserva" />
              </Form.Item>

              <Form.Item
                name="contenido_texto"
                label="Contenido Texto"
                rules={[{ required: true, message: 'Contenido requerido' }]}
              >
                <TextArea 
                  rows={6}
                  placeholder="Estimado {{nombre_cliente}}, su reserva..."
                />
              </Form.Item>

              <Form.Item
                name="contenido_html"
                label="Contenido HTML (opcional)"
              >
                <CodeEditor
                  language="html"
                  placeholder="<h1>{{titulo}}</h1><p>{{mensaje}}</p>"
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="Variables" key="variables">
              <Form.Item
                name="variables_requeridas"
                label="Variables Requeridas"
              >
                <Select
                  mode="tags"
                  placeholder="nombre_cliente, hotel_nombre, etc."
                />
              </Form.Item>

              <Form.Item
                name="variables_opcionales"
                label="Variables Opcionales"
              >
                <Select
                  mode="tags"
                  placeholder="servicios_incluidos, promociones, etc."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="Configuración" key="configuracion">
              <Form.Item
                name="activa"
                valuePropName="checked"
              >
                <Switch /> Plantilla Activa
              </Form.Item>

              <Form.Item
                name="es_predeterminada"
                valuePropName="checked"
              >
                <Switch /> Plantilla Predeterminada
              </Form.Item>
            </TabPane>
          </Tabs>

          <div style={{ textAlign: 'right', marginTop: 24 }}>
            <Button onClick={() => setModalVisible(false)}>
              Cancelar
            </Button>
            <Button type="primary" htmlType="submit" style={{ marginLeft: 8 }}>
              Guardar
            </Button>
          </div>
        </Form>
      </Modal>

      <Modal
        title="Vista Previa de Plantilla"
        visible={previewModal}
        onCancel={() => setPreviewModal(false)}
        footer={null}
        width={800}
      >
        <Tabs>
          {previewContent.asunto_renderizado && (
            <TabPane tab="Asunto" key="asunto">
              <div style={{ padding: 16, backgroundColor: '#f5f5f5' }}>
                {previewContent.asunto_renderizado}
              </div>
            </TabPane>
          )}
          
          <TabPane tab="Texto" key="texto">
            <div style={{ padding: 16, backgroundColor: '#f5f5f5', whiteSpace: 'pre-wrap' }}>
              {previewContent.contenido_texto_renderizado}
            </div>
          </TabPane>
          
          {previewContent.contenido_html_renderizado && (
            <TabPane tab="HTML" key="html">
              <div 
                style={{ padding: 16, border: '1px solid #d9d9d9' }}
                dangerouslySetInnerHTML={{ 
                  __html: previewContent.contenido_html_renderizado 
                }}
              />
            </TabPane>
          )}
        </Tabs>
      </Modal>
    </div>
  );
};

export default GestionPlantillas;
```

## 5. MEJORES PRÁCTICAS

### 5.1 Diseño de Plantillas

1. **Responsive Design**: Asegurar que los emails se vean bien en móviles
2. **Fallbacks**: Siempre incluir versión texto plano
3. **Branding Consistente**: Mantener colores y tipografías de marca
4. **Call-to-Action Claros**: Botones y enlaces bien visibles
5. **Contenido Scaneable**: Usar headlines, bullets y espacios en blanco

### 5.2 Gestión de Variables

1. **Validación**: Siempre validar variables requeridas
2. **Fallbacks**: Proporcionar valores por defecto
3. **Escapado**: Escapar contenido HTML para evitar XSS
4. **Formato**: Usar filtros para formatear fechas, monedas, etc.

### 5.3 Configuración de Canales

1. **Rate Limiting**: Implementar límites por canal y usuario
2. **Retry Logic**: Configurar reintentos con backoff exponencial
3. **Monitoring**: Monitorear tasas de entrega y errores
4. **Failover**: Tener canales alternativos para casos críticos

### 5.4 Testing

1. **Unit Tests**: Probar renderizado de plantillas
2. **Integration Tests**: Probar envío por cada canal
3. **A/B Testing**: Experimentar con diferentes versiones
4. **Load Testing**: Probar bajo carga alta

Esta guía proporciona una base sólida para implementar un sistema completo de notificaciones con plantillas flexibles y configuración robusta de canales.