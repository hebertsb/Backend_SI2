# API NOTIFICACIONES - Sistema Completo de Comunicaciones

## Introducción

Sistema integral de notificaciones que maneja comunicaciones en tiempo real, emails, SMS y notificaciones push para el sistema de reservas. Incluye gestión de plantillas, preferencias de usuarios y estadísticas de entrega.

## Estructura del Sistema

### Modelos Base

```python
# Modelo de Notificación
class Notificacion:
    id = "integer - ID único"
    usuario = "ForeignKey - Usuario destinatario"
    tipo_notificacion = "string - Tipo (reserva_confirmada, reprogramacion, cancelacion, recordatorio, promocion)"
    canal = "string - Canal (email, sms, push, in_app)"
    titulo = "string - Título de la notificación"
    mensaje = "text - Contenido del mensaje"
    datos_adicionales = "json - Datos contextuales"
    plantilla = "ForeignKey - Plantilla utilizada"
    estado = "string - Estado (pendiente, enviada, entregada, fallida, leida)"
    prioridad = "string - Prioridad (baja, normal, alta, urgente)"
    programada_para = "datetime - Fecha/hora programada"
    enviada_en = "datetime - Timestamp de envío"
    entregada_en = "datetime - Timestamp de entrega"
    leida_en = "datetime - Timestamp de lectura"
    intentos_envio = "integer - Número de intentos"
    ultimo_error = "text - Último error de envío"
    metadatos = "json - Metadatos adicionales"
    created_at = "datetime"
    updated_at = "datetime"

# Modelo de Plantilla
class PlantillaNotificacion:
    id = "integer - ID único"
    nombre = "string - Nombre de la plantilla"
    tipo = "string - Tipo de notificación"
    canal = "string - Canal específico"
    asunto = "string - Asunto (para email)"
    contenido_html = "text - Contenido HTML"
    contenido_texto = "text - Contenido texto plano"
    variables = "json - Variables disponibles"
    activa = "boolean"
    idioma = "string - Idioma de la plantilla"

# Modelo de Preferencias
class PreferenciasNotificacion:
    usuario = "OneToOne - Usuario"
    email_reservas = "boolean"
    email_promociones = "boolean"
    sms_recordatorios = "boolean"
    push_tiempo_real = "boolean"
    horario_no_molestar_inicio = "time"
    horario_no_molestar_fin = "time"
    dias_no_molestar = "json - Array de días"
```

## 1. ENDPOINTS PRINCIPALES

### 1.1 Listar Notificaciones del Usuario

```http
GET /api/notificaciones/
```

#### Headers
```json
{
  "Authorization": "Bearer {token}",
  "Content-Type": "application/json"
}
```

#### Query Parameters
```json
{
  "estado": "pendiente|enviada|entregada|fallida|leida",
  "tipo": "reserva_confirmada|reprogramacion|cancelacion|recordatorio|promocion",
  "canal": "email|sms|push|in_app",
  "fecha_desde": "2024-01-01",
  "fecha_hasta": "2024-12-31",
  "solo_no_leidas": "true|false",
  "page": 1,
  "page_size": 20
}
```

#### Response Success (200)
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/notificaciones/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "tipo_notificacion": "reserva_confirmada",
      "canal": "email",
      "titulo": "Reserva Confirmada - Hotel Paradise",
      "mensaje": "Su reserva para el Hotel Paradise ha sido confirmada",
      "estado": "entregada",
      "prioridad": "normal",
      "programada_para": "2024-01-15T10:00:00Z",
      "enviada_en": "2024-01-15T10:00:05Z",
      "entregada_en": "2024-01-15T10:00:12Z",
      "leida_en": null,
      "datos_adicionales": {
        "reserva_id": 456,
        "hotel_nombre": "Hotel Paradise",
        "fecha_checkin": "2024-02-01",
        "fecha_checkout": "2024-02-05"
      },
      "metadatos": {
        "proveedor_email": "sendgrid",
        "message_id": "abc123"
      },
      "created_at": "2024-01-15T09:55:00Z"
    }
  ]
}
```

### 1.2 Crear Nueva Notificación

```http
POST /api/notificaciones/
```

#### Payload - Notificación Inmediata
```json
{
  "usuario_id": 25,
  "tipo_notificacion": "reserva_confirmada",
  "canal": "email",
  "titulo": "Reserva Confirmada",
  "mensaje": "Su reserva ha sido confirmada exitosamente",
  "prioridad": "normal",
  "datos_adicionales": {
    "reserva_id": 789,
    "numero_confirmacion": "CNF789456",
    "hotel_nombre": "Grand Hotel",
    "monto_total": 1500.00
  },
  "enviar_inmediatamente": true
}
```

#### Payload - Notificación Programada
```json
{
  "usuario_id": 25,
  "tipo_notificacion": "recordatorio",
  "canal": "sms",
  "titulo": "Recordatorio Check-in",
  "mensaje": "Recordatorio: Su check-in es mañana a las 15:00",
  "prioridad": "alta",
  "programada_para": "2024-02-01T12:00:00Z",
  "datos_adicionales": {
    "reserva_id": 789,
    "hora_checkin": "15:00",
    "telefono_hotel": "+591-3-1234567"
  }
}
```

#### Response Success (201)
```json
{
  "id": 124,
  "usuario": 25,
  "tipo_notificacion": "reserva_confirmada",
  "canal": "email",
  "titulo": "Reserva Confirmada",
  "mensaje": "Su reserva ha sido confirmada exitosamente",
  "estado": "enviada",
  "prioridad": "normal",
  "programada_para": "2024-01-15T10:30:00Z",
  "enviada_en": "2024-01-15T10:30:03Z",
  "datos_adicionales": {
    "reserva_id": 789,
    "numero_confirmacion": "CNF789456"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 1.3 Marcar Notificación como Leída

```http
PATCH /api/notificaciones/{id}/marcar-leida/
```

#### Response Success (200)
```json
{
  "id": 124,
  "estado": "leida",
  "leida_en": "2024-01-15T14:30:00Z",
  "message": "Notificación marcada como leída"
}
```

### 1.4 Marcar Todas como Leídas

```http
POST /api/notificaciones/marcar-todas-leidas/
```

#### Payload (opcional)
```json
{
  "tipo_notificacion": "promocion",
  "fecha_hasta": "2024-01-15"
}
```

#### Response Success (200)
```json
{
  "marcadas": 12,
  "message": "12 notificaciones marcadas como leídas"
}
```

## 2. NOTIFICACIONES EN TIEMPO REAL

### 2.1 WebSocket Connection

```javascript
// Conexión WebSocket para notificaciones en tiempo real
const notificationSocket = new WebSocket(
  `ws://localhost:8000/ws/notifications/${userId}/`
);

notificationSocket.onopen = function(e) {
  console.log('Conectado a notificaciones en tiempo real');
};

notificationSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  handleNotification(data);
};

// Estructura de mensaje WebSocket
{
  "type": "notification",
  "data": {
    "id": 125,
    "tipo_notificacion": "reprogramacion_aprobada",
    "titulo": "Reprogramación Aprobada",
    "mensaje": "Su solicitud de reprogramación ha sido aprobada",
    "prioridad": "alta",
    "datos_adicionales": {
      "reserva_id": 456,
      "nueva_fecha": "2024-03-15"
    },
    "timestamp": "2024-01-15T16:00:00Z"
  }
}
```

### 2.2 React Hook para Notificaciones

```javascript
// Custom Hook para manejar notificaciones
import { useState, useEffect } from 'react';
import { notification } from 'antd';

const useNotifications = (userId) => {
  const [socket, setSocket] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/notifications/${userId}/`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'notification') {
        const newNotification = data.data;
        
        // Agregar a la lista
        setNotifications(prev => [newNotification, ...prev]);
        setUnreadCount(prev => prev + 1);
        
        // Mostrar notificación visual
        notification[newNotification.prioridad === 'urgente' ? 'error' : 'info']({
          message: newNotification.titulo,
          description: newNotification.mensaje,
          duration: newNotification.prioridad === 'urgente' ? 0 : 4.5,
          onClick: () => handleNotificationClick(newNotification)
        });
      }
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [userId]);

  const markAsRead = async (notificationId) => {
    try {
      await fetch(`/api/notificaciones/${notificationId}/marcar-leida/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setNotifications(prev => 
        prev.map(n => 
          n.id === notificationId 
            ? { ...n, estado: 'leida', leida_en: new Date().toISOString() }
            : n
        )
      );
      
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  return {
    notifications,
    unreadCount,
    markAsRead,
    socket
  };
};

// Componente de Centro de Notificaciones
const NotificationCenter = ({ userId }) => {
  const { notifications, unreadCount, markAsRead } = useNotifications(userId);
  const [visible, setVisible] = useState(false);

  const content = (
    <div style={{ width: 350, maxHeight: 400, overflowY: 'auto' }}>
      <div style={{ padding: '8px 16px', borderBottom: '1px solid #f0f0f0' }}>
        <Text strong>Notificaciones ({unreadCount} no leídas)</Text>
      </div>
      
      <List
        dataSource={notifications.slice(0, 10)}
        renderItem={(item) => (
          <List.Item
            style={{
              backgroundColor: item.estado === 'leida' ? '#fff' : '#f6ffed',
              cursor: 'pointer'
            }}
            onClick={() => {
              if (item.estado !== 'leida') {
                markAsRead(item.id);
              }
            }}
          >
            <List.Item.Meta
              avatar={<Badge dot={item.estado !== 'leida'} />}
              title={item.titulo}
              description={
                <div>
                  <div>{item.mensaje}</div>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {new Date(item.created_at).toLocaleString()}
                  </Text>
                </div>
              }
            />
          </List.Item>
        )}
      />
      
      <div style={{ padding: '8px 16px', textAlign: 'center' }}>
        <Button type="link" size="small">
          Ver todas las notificaciones
        </Button>
      </div>
    </div>
  );

  return (
    <Popover
      content={content}
      title={null}
      trigger="click"
      visible={visible}
      onVisibleChange={setVisible}
      placement="bottomRight"
    >
      <Badge count={unreadCount} size="small">
        <Button
          type="text"
          icon={<BellOutlined />}
          size="large"
        />
      </Badge>
    </Popover>
  );
};
```

## 3. GESTIÓN DE PLANTILLAS

### 3.1 Listar Plantillas

```http
GET /api/notificaciones/plantillas/
```

#### Query Parameters
```json
{
  "tipo": "reserva_confirmada|reprogramacion|cancelacion",
  "canal": "email|sms|push",
  "activa": "true|false",
  "idioma": "es|en"
}
```

#### Response Success (200)
```json
{
  "results": [
    {
      "id": 1,
      "nombre": "Confirmación de Reserva Email",
      "tipo": "reserva_confirmada",
      "canal": "email",
      "asunto": "Confirmación de Reserva #{numero_confirmacion}",
      "contenido_html": "<h1>¡Reserva Confirmada!</h1><p>Estimado/a {{nombre_cliente}},</p>...",
      "contenido_texto": "Reserva Confirmada! Estimado/a {{nombre_cliente}}...",
      "variables": [
        "nombre_cliente",
        "numero_confirmacion",
        "hotel_nombre",
        "fecha_checkin",
        "fecha_checkout",
        "monto_total"
      ],
      "activa": true,
      "idioma": "es"
    }
  ]
}
```

### 3.2 Crear Nueva Plantilla

```http
POST /api/notificaciones/plantillas/
```

#### Payload
```json
{
  "nombre": "Recordatorio Check-in SMS",
  "tipo": "recordatorio",
  "canal": "sms",
  "contenido_texto": "Hola {{nombre_cliente}}! Su check-in en {{hotel_nombre}} es el {{fecha_checkin}} a las {{hora_checkin}}. Confirmación: {{numero_confirmacion}}",
  "variables": [
    "nombre_cliente",
    "hotel_nombre", 
    "fecha_checkin",
    "hora_checkin",
    "numero_confirmacion"
  ],
  "activa": true,
  "idioma": "es"
}
```

### 3.3 Vista Previa de Plantilla

```http
POST /api/notificaciones/plantillas/{id}/preview/
```

#### Payload - Datos de Prueba
```json
{
  "datos_muestra": {
    "nombre_cliente": "Juan Pérez",
    "hotel_nombre": "Hotel Paradise",
    "fecha_checkin": "2024-02-01",
    "hora_checkin": "15:00",
    "numero_confirmacion": "CNF123456",
    "monto_total": "1,500.00 BOB"
  }
}
```

#### Response Success (200)
```json
{
  "asunto_renderizado": "Confirmación de Reserva #CNF123456",
  "contenido_html_renderizado": "<h1>¡Reserva Confirmada!</h1><p>Estimado/a Juan Pérez,</p><p>Su reserva en Hotel Paradise ha sido confirmada...</p>",
  "contenido_texto_renderizado": "Reserva Confirmada! Estimado/a Juan Pérez, Su reserva en Hotel Paradise ha sido confirmada..."
}
```

## 4. PREFERENCIAS DE USUARIO

### 4.1 Obtener Preferencias

```http
GET /api/notificaciones/preferencias/
```

#### Response Success (200)
```json
{
  "email_reservas": true,
  "email_promociones": false,
  "sms_recordatorios": true,
  "sms_promociones": false,
  "push_tiempo_real": true,
  "push_promociones": false,
  "horario_no_molestar_inicio": "22:00",
  "horario_no_molestar_fin": "08:00",
  "dias_no_molestar": ["domingo"],
  "idioma_preferido": "es",
  "zona_horaria": "America/La_Paz"
}
```

### 4.2 Actualizar Preferencias

```http
PUT /api/notificaciones/preferencias/
```

#### Payload
```json
{
  "email_reservas": true,
  "email_promociones": true,
  "sms_recordatorios": true,
  "sms_promociones": false,
  "push_tiempo_real": true,
  "push_promociones": true,
  "horario_no_molestar_inicio": "23:00",
  "horario_no_molestar_fin": "07:00",
  "dias_no_molestar": ["domingo"],
  "idioma_preferido": "es"
}
```

## 5. ESTADÍSTICAS Y REPORTES

### 5.1 Estadísticas de Entrega

```http
GET /api/notificaciones/estadisticas/
```

#### Query Parameters
```json
{
  "fecha_desde": "2024-01-01",
  "fecha_hasta": "2024-01-31",
  "tipo": "reserva_confirmada",
  "canal": "email"
}
```

#### Response Success (200)
```json
{
  "resumen": {
    "total_enviadas": 1250,
    "total_entregadas": 1180,
    "total_fallidas": 70,
    "total_leidas": 890,
    "tasa_entrega": 94.4,
    "tasa_lectura": 75.4,
    "tiempo_promedio_lectura": "2.5 horas"
  },
  "por_canal": {
    "email": {
      "enviadas": 800,
      "entregadas": 760,
      "fallidas": 40,
      "tasa_entrega": 95.0
    },
    "sms": {
      "enviadas": 300,
      "entregadas": 285,
      "fallidas": 15,
      "tasa_entrega": 95.0
    },
    "push": {
      "enviadas": 150,
      "entregadas": 135,
      "fallidas": 15,
      "tasa_entrega": 90.0
    }
  },
  "por_tipo": {
    "reserva_confirmada": {
      "enviadas": 400,
      "leidas": 350,
      "tasa_lectura": 87.5
    },
    "recordatorio": {
      "enviadas": 300,
      "leidas": 280,
      "tasa_lectura": 93.3
    },
    "promocion": {
      "enviadas": 550,
      "leidas": 260,
      "tasa_lectura": 47.3
    }
  }
}
```

## 6. NOTIFICACIONES MASIVAS

### 6.1 Envío Masivo de Promociones

```http
POST /api/notificaciones/envio-masivo/
```

#### Payload - Segmentación por Criterios
```json
{
  "titulo": "Oferta Especial - 50% de Descuento",
  "mensaje": "Aprovecha nuestra oferta especial en hoteles seleccionados",
  "tipo_notificacion": "promocion",
  "canal": "email",
  "plantilla_id": 5,
  "criterios_segmentacion": {
    "ubicacion": "Santa Cruz",
    "nivel_membresia": ["oro", "platino"],
    "ultima_reserva_desde": "2023-01-01",
    "ha_usado_reprogramacion": true
  },
  "programar_para": "2024-01-20T09:00:00Z",
  "datos_adicionales": {
    "codigo_descuento": "ESPECIAL50",
    "fecha_vencimiento": "2024-02-29",
    "hoteles_incluidos": ["hotel_1", "hotel_2", "hotel_3"]
  }
}
```

#### Response Success (202)
```json
{
  "tarea_id": "abc123def456",
  "destinatarios_estimados": 485,
  "fecha_programada": "2024-01-20T09:00:00Z",
  "estado": "programada",
  "message": "Envío masivo programado exitosamente"
}
```

### 6.2 Estado de Envío Masivo

```http
GET /api/notificaciones/envio-masivo/{tarea_id}/estado/
```

#### Response Success (200)
```json
{
  "tarea_id": "abc123def456",
  "estado": "en_progreso",
  "progreso": {
    "total": 485,
    "procesados": 320,
    "enviados": 315,
    "fallidos": 5,
    "porcentaje": 66.0
  },
  "iniciado_en": "2024-01-20T09:00:00Z",
  "estimado_finalizacion": "2024-01-20T09:15:00Z"
}
```

## 7. INTEGRACIÓN CON RESERVAS

### 7.1 Notificaciones Automáticas de Reserva

```python
# Ejemplo de integración con signals de Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reserva, Notificacion

@receiver(post_save, sender=Reserva)
def crear_notificacion_reserva(sender, instance, created, **kwargs):
    if created:
        # Notificación de confirmación
        Notificacion.objects.create(
            usuario=instance.usuario,
            tipo_notificacion='reserva_confirmada',
            canal='email',
            titulo=f'Reserva Confirmada - {instance.servicio.nombre}',
            datos_adicionales={
                'reserva_id': instance.id,
                'numero_confirmacion': instance.numero_confirmacion,
                'hotel_nombre': instance.servicio.nombre,
                'fecha_checkin': instance.fecha_inicio.isoformat(),
                'fecha_checkout': instance.fecha_fin.isoformat(),
                'monto_total': str(instance.monto_total)
            },
            prioridad='normal'
        )
        
        # Programar recordatorio 24h antes
        fecha_recordatorio = instance.fecha_inicio - timedelta(days=1)
        if fecha_recordatorio > timezone.now():
            Notificacion.objects.create(
                usuario=instance.usuario,
                tipo_notificacion='recordatorio',
                canal='sms',
                titulo='Recordatorio Check-in',
                mensaje=f'Su check-in en {instance.servicio.nombre} es mañana',
                programada_para=fecha_recordatorio.replace(hour=12),
                datos_adicionales={
                    'reserva_id': instance.id,
                    'hotel_nombre': instance.servicio.nombre
                },
                prioridad='alta'
            )
```

## 8. COMPONENTES REACT PARA FRONTEND

### 8.1 Configuración de Preferencias

```javascript
// Componente para configurar preferencias de notificaciones
import React, { useState, useEffect } from 'react';
import { Card, Switch, TimePicker, Select, Button, message } from 'antd';

const PreferenciasNotificaciones = () => {
  const [preferencias, setPreferencias] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    cargarPreferencias();
  }, []);

  const cargarPreferencias = async () => {
    try {
      const response = await fetch('/api/notificaciones/preferencias/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setPreferencias(data);
    } catch (error) {
      message.error('Error cargando preferencias');
    }
  };

  const guardarPreferencias = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/notificaciones/preferencias/', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(preferencias)
      });

      if (response.ok) {
        message.success('Preferencias actualizadas');
      }
    } catch (error) {
      message.error('Error guardando preferencias');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Configuración de Notificaciones">
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        <div>
          <h4>Notificaciones por Email</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Confirmaciones de reserva</span>
              <Switch
                checked={preferencias.email_reservas}
                onChange={(checked) => 
                  setPreferencias({...preferencias, email_reservas: checked})
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Promociones y ofertas</span>
              <Switch
                checked={preferencias.email_promociones}
                onChange={(checked) => 
                  setPreferencias({...preferencias, email_promociones: checked})
                }
              />
            </div>
          </div>
        </div>

        <div>
          <h4>Notificaciones por SMS</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Recordatorios importantes</span>
              <Switch
                checked={preferencias.sms_recordatorios}
                onChange={(checked) => 
                  setPreferencias({...preferencias, sms_recordatorios: checked})
                }
              />
            </div>
          </div>
        </div>

        <div>
          <h4>Horario "No Molestar"</h4>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <span>Desde:</span>
            <TimePicker
              value={preferencias.horario_no_molestar_inicio}
              onChange={(time) => 
                setPreferencias({
                  ...preferencias, 
                  horario_no_molestar_inicio: time
                })
              }
              format="HH:mm"
            />
            <span>Hasta:</span>
            <TimePicker
              value={preferencias.horario_no_molestar_fin}
              onChange={(time) => 
                setPreferencias({
                  ...preferencias, 
                  horario_no_molestar_fin: time
                })
              }
              format="HH:mm"
            />
          </div>
        </div>

        <Button 
          type="primary" 
          onClick={guardarPreferencias}
          loading={loading}
        >
          Guardar Preferencias
        </Button>
      </div>
    </Card>
  );
};
```

## 9. CÓDIGOS DE ERROR

### Error 400 - Datos Inválidos
```json
{
  "error": "Datos inválidos",
  "details": {
    "canal": ["Canal no soportado"],
    "programada_para": ["Fecha no puede ser en el pasado"]
  }
}
```

### Error 429 - Límite de Rate
```json
{
  "error": "Límite de notificaciones excedido",
  "limite": 100,
  "periodo": "1 hora",
  "reintentar_en": 3600
}
```

## Notas Importantes

1. **Rate Limiting**: Límites por usuario y tipo de notificación
2. **Reintentos**: Sistema automático de reintentos para notificaciones fallidas
3. **Batch Processing**: Procesamiento en lotes para envíos masivos
4. **Tracking**: Seguimiento completo del ciclo de vida de notificaciones
5. **Templates**: Sistema flexible de plantillas con variables dinámicas
6. **Preferences**: Respeto total a las preferencias del usuario
7. **Real-time**: WebSockets para notificaciones instantáneas
8. **Multi-channel**: Soporte para email, SMS, push y in-app
9. **Scheduling**: Programación de notificaciones futuras
10. **Analytics**: Estadísticas detalladas de rendimiento