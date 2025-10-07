# Guía de Integración Frontend - Notificaciones Web para Soporte

## Descripción General

Esta guía explica cómo implementar las notificaciones web en tiempo real para que el equipo de soporte pueda recibir alertas inmediatas cuando se realicen reprogramaciones de reservas.

## Arquitectura de Notificaciones Web

```
Backend Django          Frontend (React/Vue/JS)
     │                         │
     ├─ HTTP API               ├─ Polling HTTP
     ├─ WebSockets             ├─ WebSocket Client  
     ├─ Server-Sent Events     ├─ EventSource
     └─ Push Notifications     └─ Service Worker
```

## 1. Implementación con HTTP Polling

### Backend - Endpoint de Notificaciones

Crear en `reservas/views.py`:

```python
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notificaciones_soporte(request):
    """Endpoint para obtener notificaciones de reprogramación para soporte"""
    
    # Solo usuarios con permisos de soporte/admin
    if not request.user.groups.filter(name__in=['Soporte', 'Administradores']).exists():
        return Response({'error': 'Sin permisos'}, status=403)
    
    # Obtener parámetros
    desde = request.GET.get('desde')
    limite = int(request.GET.get('limite', 10))
    solo_no_leidas = request.GET.get('no_leidas', 'false').lower() == 'true'
    
    # Si no se especifica fecha, obtener últimas 24 horas
    if not desde:
        desde = timezone.now() - timedelta(hours=24)
    else:
        desde = datetime.fromisoformat(desde)
    
    # Consultar historial de reprogramaciones
    query = HistorialReprogramacion.objects.filter(
        fecha_reprogramacion__gte=desde
    ).select_related(
        'reserva__usuario', 'reprogramado_por'
    ).order_by('-fecha_reprogramacion')
    
    if solo_no_leidas:
        # Aquí podrías agregar un campo 'leida' al modelo si lo necesitas
        pass
    
    historial = query[:limite]
    
    notificaciones = []
    for item in historial:
        notificaciones.append({
            'id': item.id,
            'tipo': 'reprogramacion',
            'reserva_id': item.reserva.id,
            'cliente': {
                'id': item.reserva.usuario.id,
                'nombre': f"{item.reserva.usuario.nombres} {item.reserva.usuario.apellidos}",
                'email': item.reserva.usuario.email,
                'telefono': item.reserva.usuario.telefono
            },
            'fecha_anterior': item.fecha_anterior,
            'fecha_nueva': item.fecha_nueva,
            'motivo': item.motivo,
            'reprogramado_por': {
                'id': item.reprogramado_por.id,
                'nombre': f"{item.reprogramado_por.nombres} {item.reprogramado_por.apellidos}",
                'email': item.reprogramado_por.email
            },
            'timestamp': item.fecha_reprogramacion,
            'total_reserva': item.reserva.total,
            'moneda': item.reserva.moneda,
            'servicios': [
                {
                    'titulo': detalle.servicio.titulo,
                    'cantidad': detalle.cantidad,
                    'precio': detalle.precio_unitario
                }
                for detalle in item.reserva.detalles.all()
            ]
        })
    
    return Response({
        'notificaciones': notificaciones,
        'total': len(notificaciones),
        'timestamp_servidor': timezone.now()
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marcar_notificacion_leida(request, notificacion_id):
    """Marcar una notificación como leída"""
    # Implementar lógica para marcar como leída
    # Esto requeriría agregar un campo al modelo o crear un modelo separado
    pass
```

### URLs Configuration

En `reservas/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reservas', views.ReservaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('notificaciones/soporte/', views.notificaciones_soporte, name='notificaciones_soporte'),
    path('notificaciones/<int:notificacion_id>/leida/', views.marcar_notificacion_leida, name='marcar_leida'),
]
```

### Frontend - React Component

```jsx
// NotificacionesSoporte.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';

const NotificacionesSoporte = () => {
    const [notificaciones, setNotificaciones] = useState([]);
    const [ultimaActualizacion, setUltimaActualizacion] = useState(null);
    const [loading, setLoading] = useState(false);

    // Polling cada 30 segundos
    const obtenerNotificaciones = useCallback(async () => {
        try {
            setLoading(true);
            const params = new URLSearchParams();
            if (ultimaActualizacion) {
                params.append('desde', ultimaActualizacion);
            }
            
            const response = await fetch(`/api/reservas/notificaciones/soporte/?${params}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Si hay nuevas notificaciones, mostrar toast
                if (ultimaActualizacion && data.notificaciones.length > 0) {
                    data.notificaciones.forEach(notif => {
                        if (new Date(notif.timestamp) > new Date(ultimaActualizacion)) {
                            toast.info(`Nueva reprogramación: Reserva #${notif.reserva_id}`, {
                                onClick: () => verDetalleReserva(notif.reserva_id)
                            });
                        }
                    });
                }
                
                setNotificaciones(prevState => {
                    // Combinar y evitar duplicados
                    const nuevasNotifs = data.notificaciones.filter(nueva => 
                        !prevState.some(existente => existente.id === nueva.id)
                    );
                    return [...nuevasNotifs, ...prevState].slice(0, 50); // Limitar a 50
                });
                
                setUltimaActualizacion(data.timestamp_servidor);
            }
        } catch (error) {
            console.error('Error obteniendo notificaciones:', error);
        } finally {
            setLoading(false);
        }
    }, [ultimaActualizacion]);

    // Setup polling
    useEffect(() => {
        obtenerNotificaciones(); // Carga inicial
        
        const intervalo = setInterval(obtenerNotificaciones, 30000); // 30 segundos
        
        return () => clearInterval(intervalo);
    }, [obtenerNotificaciones]);

    const verDetalleReserva = (reservaId) => {
        // Navegar al detalle de la reserva
        window.open(`/admin/reservas/${reservaId}`, '_blank');
    };

    const formatearFecha = (fecha) => {
        return new Date(fecha).toLocaleString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="notificaciones-soporte">
            <div className="header">
                <h3>Notificaciones de Reprogramación</h3>
                <div className="status">
                    {loading && <span className="loading">🔄 Actualizando...</span>}
                    <span className="ultima-actualizacion">
                        Última actualización: {ultimaActualizacion ? formatearFecha(ultimaActualizacion) : 'Nunca'}
                    </span>
                </div>
            </div>

            <div className="lista-notificaciones">
                {notificaciones.length === 0 ? (
                    <div className="sin-notificaciones">
                        <p>No hay reprogramaciones recientes</p>
                    </div>
                ) : (
                    notificaciones.map(notif => (
                        <div key={notif.id} className="notificacion-item">
                            <div className="notificacion-header">
                                <span className="tipo-badge">📅 Reprogramación</span>
                                <span className="timestamp">{formatearFecha(notif.timestamp)}</span>
                            </div>
                            
                            <div className="notificacion-content">
                                <h4>
                                    Reserva #{notif.reserva_id} - {notif.cliente.nombre}
                                </h4>
                                
                                <div className="detalles-cambio">
                                    <div className="fecha-cambio">
                                        <span className="label">Fecha anterior:</span>
                                        <span className="fecha-anterior">{formatearFecha(notif.fecha_anterior)}</span>
                                    </div>
                                    <div className="fecha-cambio">
                                        <span className="label">Nueva fecha:</span>
                                        <span className="fecha-nueva">{formatearFecha(notif.fecha_nueva)}</span>
                                    </div>
                                </div>
                                
                                {notif.motivo && (
                                    <div className="motivo">
                                        <strong>Motivo:</strong> {notif.motivo}
                                    </div>
                                )}
                                
                                <div className="info-adicional">
                                    <span>Cliente: {notif.cliente.email}</span>
                                    <span>Total: {notif.total_reserva} {notif.moneda}</span>
                                    <span>Por: {notif.reprogramado_por.nombre}</span>
                                </div>
                            </div>
                            
                            <div className="notificacion-acciones">
                                <button 
                                    onClick={() => verDetalleReserva(notif.reserva_id)}
                                    className="btn-ver-detalle"
                                >
                                    Ver Reserva
                                </button>
                                <button 
                                    onClick={() => window.open(`mailto:${notif.cliente.email}`, '_blank')}
                                    className="btn-contactar"
                                >
                                    Contactar Cliente
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default NotificacionesSoporte;
```

### CSS para el Componente

```css
/* NotificacionesSoporte.css */
.notificaciones-soporte {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

.header h3 {
    margin: 0;
    color: #333;
}

.status {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-size: 0.9em;
    color: #666;
}

.loading {
    color: #007bff;
    font-weight: bold;
}

.sin-notificaciones {
    text-align: center;
    padding: 40px 20px;
    color: #888;
    background-color: #f8f9fa;
    border-radius: 8px;
}

.notificacion-item {
    background: white;
    border: 1px solid #ddd;
    border-left: 4px solid #ffc107;
    border-radius: 8px;
    margin-bottom: 15px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: box-shadow 0.2s;
}

.notificacion-item:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.notificacion-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.tipo-badge {
    background-color: #ffc107;
    color: #333;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    font-weight: bold;
}

.timestamp {
    color: #666;
    font-size: 0.9em;
}

.notificacion-content h4 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 1.1em;
}

.detalles-cambio {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 4px;
    margin: 10px 0;
}

.fecha-cambio {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
}

.fecha-cambio .label {
    font-weight: bold;
    color: #555;
}

.fecha-anterior {
    color: #dc3545;
    text-decoration: line-through;
}

.fecha-nueva {
    color: #28a745;
    font-weight: bold;
}

.motivo {
    margin: 10px 0;
    padding: 8px;
    background-color: #e3f2fd;
    border-radius: 4px;
    font-size: 0.9em;
}

.info-adicional {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin: 10px 0;
    font-size: 0.9em;
    color: #666;
}

.notificacion-acciones {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #eee;
}

.btn-ver-detalle, .btn-contactar {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
    transition: background-color 0.2s;
}

.btn-ver-detalle {
    background-color: #007bff;
    color: white;
}

.btn-ver-detalle:hover {
    background-color: #0056b3;
}

.btn-contactar {
    background-color: #28a745;
    color: white;
}

.btn-contactar:hover {
    background-color: #1e7e34;
}

@media (max-width: 768px) {
    .notificaciones-soporte {
        padding: 10px;
    }
    
    .header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .info-adicional {
        flex-direction: column;
        gap: 5px;
    }
    
    .notificacion-acciones {
        flex-direction: column;
    }
}
```

## 2. Implementación con WebSockets

### Backend - Configuración WebSocket

Instalar Django Channels:
```bash
pip install channels redis
```

En `settings.py`:
```python
INSTALLED_APPS = [
    # ... otras apps
    'channels',
]

ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

Crear `consumers.py`:
```python
# reservas/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class NotificacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Solo permitir conexión a usuarios de soporte
        if not await self.es_usuario_soporte(self.user):
            await self.close()
            return
        
        self.room_group_name = 'notificaciones_soporte'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Manejar mensajes del cliente si es necesario
        pass

    async def notificacion_reprogramacion(self, event):
        # Enviar notificación al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'reprogramacion',
            'data': event['data']
        }))

    @database_sync_to_async
    def es_usuario_soporte(self, user):
        if user.is_anonymous:
            return False
        return user.groups.filter(name__in=['Soporte', 'Administradores']).exists()
```

Routing en `routing.py`:
```python
# reservas/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/$', consumers.NotificacionesConsumer.as_asgi()),
]
```

### Modificar notificaciones para enviar WebSocket

En `reservas/notifications.py`:
```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificacionReprogramacion:
    @staticmethod
    def notificar_administrador(reserva, fecha_anterior, reprogramado_por, motivo=None):
        # ... código de email existente ...
        
        # Enviar notificación WebSocket
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                'notificaciones_soporte',
                {
                    'type': 'notificacion_reprogramacion',
                    'data': {
                        'reserva_id': reserva.id,
                        'cliente_nombre': f"{reserva.usuario.nombres} {reserva.usuario.apellidos}",
                        'fecha_anterior': fecha_anterior.isoformat(),
                        'fecha_nueva': reserva.fecha_inicio.isoformat(),
                        'motivo': motivo,
                        'reprogramado_por': f"{reprogramado_por.nombres} {reprogramado_por.apellidos}",
                        'timestamp': timezone.now().isoformat()
                    }
                }
            )
        
        return resultado_email
```

### Frontend - Cliente WebSocket

```javascript
// useNotificacionesWebSocket.js
import { useState, useEffect, useRef } from 'react';

export const useNotificacionesWebSocket = (token) => {
    const [notificaciones, setNotificaciones] = useState([]);
    const [conectado, setConectado] = useState(false);
    const socketRef = useRef(null);

    useEffect(() => {
        if (!token) return;

        const wsUrl = `ws://localhost:8000/ws/notificaciones/?token=${token}`;
        socketRef.current = new WebSocket(wsUrl);

        socketRef.current.onopen = () => {
            console.log('WebSocket conectado');
            setConectado(true);
        };

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'reprogramacion') {
                const nuevaNotificacion = {
                    id: Date.now(),
                    ...data.data,
                    timestamp: new Date(data.data.timestamp)
                };
                
                setNotificaciones(prev => [nuevaNotificacion, ...prev]);
                
                // Mostrar notificación del navegador
                if (Notification.permission === 'granted') {
                    new Notification('Nueva Reprogramación', {
                        body: `Reserva #${data.data.reserva_id} - ${data.data.cliente_nombre}`,
                        icon: '/favicon.ico'
                    });
                }
            }
        };

        socketRef.current.onclose = () => {
            console.log('WebSocket desconectado');
            setConectado(false);
        };

        socketRef.current.onerror = (error) => {
            console.error('Error WebSocket:', error);
            setConectado(false);
        };

        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, [token]);

    const enviarMensaje = (mensaje) => {
        if (socketRef.current && conectado) {
            socketRef.current.send(JSON.stringify(mensaje));
        }
    };

    return { notificaciones, conectado, enviarMensaje };
};
```

## 3. Panel de Control Completo

```jsx
// PanelSoporte.jsx
import React, { useState } from 'react';
import NotificacionesSoporte from './NotificacionesSoporte';
import { useNotificacionesWebSocket } from './useNotificacionesWebSocket';

const PanelSoporte = () => {
    const token = localStorage.getItem('token');
    const { notificaciones: notificacionesWS, conectado } = useNotificacionesWebSocket(token);
    const [vista, setVista] = useState('tiempo-real');

    // Solicitar permisos de notificación
    React.useEffect(() => {
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }, []);

    return (
        <div className="panel-soporte">
            <header className="panel-header">
                <h1>Panel de Soporte - Reprogramaciones</h1>
                <div className="estado-conexion">
                    <span className={`indicador ${conectado ? 'conectado' : 'desconectado'}`}>
                        {conectado ? '🟢 Conectado' : '🔴 Desconectado'}
                    </span>
                </div>
            </header>

            <nav className="panel-nav">
                <button 
                    className={vista === 'tiempo-real' ? 'activo' : ''}
                    onClick={() => setVista('tiempo-real')}
                >
                    Tiempo Real ({notificacionesWS.length})
                </button>
                <button 
                    className={vista === 'historial' ? 'activo' : ''}
                    onClick={() => setVista('historial')}
                >
                    Historial
                </button>
            </nav>

            <main className="panel-content">
                {vista === 'tiempo-real' ? (
                    <div className="notificaciones-tiempo-real">
                        <h2>Notificaciones en Tiempo Real</h2>
                        {notificacionesWS.length === 0 ? (
                            <p>No hay notificaciones nuevas</p>
                        ) : (
                            notificacionesWS.map(notif => (
                                <div key={notif.id} className="notificacion-ws">
                                    <strong>Reserva #{notif.reserva_id}</strong>
                                    <p>Cliente: {notif.cliente_nombre}</p>
                                    <p>Reprogramado: {new Date(notif.timestamp).toLocaleString()}</p>
                                </div>
                            ))
                        )}
                    </div>
                ) : (
                    <NotificacionesSoporte />
                )}
            </main>
        </div>
    );
};

export default PanelSoporte;
```

## 4. Configuración de Producción

### Variables de Entorno
```env
# .env
REDIS_URL=redis://localhost:6379
WEBSOCKET_ENABLED=true
NOTIFICATION_POLLING_INTERVAL=30000
```

### Nginx para WebSockets
```nginx
# nginx.conf
location /ws/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 5. Testing

### Test WebSocket Consumer
```python
# tests/test_consumers.py
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from reservas.consumers import NotificacionesConsumer

class TestNotificacionesConsumer(TestCase):
    async def test_conexion_usuario_soporte(self):
        user = await self.crear_usuario_soporte()
        communicator = WebsocketCommunicator(NotificacionesConsumer.as_asgi(), "/ws/notificaciones/")
        communicator.scope["user"] = user
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        await communicator.disconnect()
```

Esta guía proporciona una implementación completa de notificaciones web para el equipo de soporte, con opciones tanto de polling HTTP como WebSockets en tiempo real.