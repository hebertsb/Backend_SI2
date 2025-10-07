# Flujo de Notificaciones para Reprogramación

## Diagrama de Flujo General

```
Cliente/Admin solicita reprogramación
           ↓
    Validaciones de negocio
           ↓
    Actualización en BD
           ↓
    ┌─────────────────────┐
    │ Sistema de          │
    │ Notificaciones      │
    └─────────────────────┘
           ↓
    ┌─────────────┬─────────────┐
    │   EMAIL     │     WEB     │
    │  (Cliente)  │  (Soporte)  │
    └─────────────┴─────────────┘
```

## 1. Flujo de Email para Clientes

### Proceso Automático

1. **Trigger**: Se ejecuta la acción `reprogramar` en el endpoint
2. **Recolección de datos**: Se obtienen los datos de la reserva y usuario
3. **Construcción del email**: Se genera el contenido personalizado
4. **Envío**: Se envía vía SMTP configurado
5. **Log**: Se registra el resultado (éxito/error)

### Secuencia Detallada

```python
# 1. En el endpoint de reprogramación (views.py)
@action(detail=True, methods=["post"], url_path="reprogramar")
def reprogramar(self, request, pk=None):
    # ... validaciones y actualización ...
    
    # 2. Preparar datos para notificación
    fecha_anterior = reserva.fecha_inicio  # Antes de actualizar
    motivo = request.data.get('motivo', '')
    
    # 3. Actualizar reserva
    # ... lógica de actualización ...
    
    # 4. Enviar notificación al cliente
    notificacion_cliente = NotificacionReprogramacion.notificar_cliente(
        reserva=reserva,
        fecha_anterior=fecha_anterior,
        motivo=motivo
    )
    
    # 5. Respuesta incluye estado de notificación
    return Response({
        "mensaje": "Reserva reprogramada exitosamente",
        "notificacion_enviada": notificacion_cliente
    })
```

### Contenido del Email al Cliente

**Asunto**: `"Tu reserva #{reserva.pk} ha sido reprogramada"`

**Información incluida**:
- Saludo personalizado con nombre del cliente
- ID de la reserva
- Fecha anterior vs nueva fecha
- Motivo de la reprogramación (si se proporcionó)
- Lista de servicios incluidos
- Total y moneda
- Información de contacto

## 2. Flujo de Notificaciones Web para Soporte

### Canales de Notificación Web

#### A. Email a Administradores
- **Destinatarios**: Lista configurada en `ADMIN_EMAILS`
- **Propósito**: Notificación inmediata al equipo
- **Contenido**: Información completa para auditoría

#### B. Notificaciones en Tiempo Real (Propuesta)
Para implementar notificaciones web en vivo:

```javascript
// Frontend - Sistema de notificaciones WebSocket
const notificationSocket = new WebSocket('ws://localhost:8000/ws/notifications/');

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'reprogramacion') {
        mostrarNotificacionSoporte(data);
    }
};

function mostrarNotificacionSoporte(data) {
    const notification = {
        title: `Reprogramación - Reserva #${data.reserva_id}`,
        message: `${data.cliente_nombre} reprogramó su reserva`,
        timestamp: new Date(),
        type: 'reprogramacion',
        data: data
    };
    
    // Agregar a la lista de notificaciones
    agregarNotificacion(notification);
    
    // Mostrar toast/popup
    mostrarToast(notification);
}
```

#### C. Dashboard de Notificaciones

**Endpoint para obtener notificaciones**:
```
GET /api/notificaciones/reprogramaciones/
```

**Respuesta esperada**:
```json
{
    "notificaciones": [
        {
            "id": 1,
            "tipo": "reprogramacion",
            "reserva_id": 123,
            "cliente": {
                "nombre": "Juan Pérez",
                "email": "juan@email.com"
            },
            "fecha_anterior": "2024-01-15T10:00:00Z",
            "fecha_nueva": "2024-01-20T14:00:00Z",
            "motivo": "Cliente solicitó cambio",
            "reprogramado_por": "Admin",
            "timestamp": "2024-01-10T15:30:00Z",
            "leida": false
        }
    ],
    "total": 1,
    "no_leidas": 1
}
```

## 3. Configuración por Entorno

### Desarrollo
```python
# settings/development.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Muestra en consola
ADMIN_EMAILS = ['dev@localhost']

# Para testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
```

### Producción
```python
# settings/production.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_EMAILS = [
    'admin@tuagencia.com',
    'soporte@tuagencia.com',
    'gerencia@tuagencia.com'
]
```

## 4. Manejo de Errores

### Estrategias de Recuperación

```python
def notificar_cliente_con_reintentos(reserva, fecha_anterior, motivo=None, max_reintentos=3):
    """Notifica al cliente con sistema de reintentos"""
    for intento in range(max_reintentos):
        try:
            resultado = NotificacionReprogramacion.notificar_cliente(
                reserva, fecha_anterior, motivo
            )
            if resultado:
                return True
        except Exception as e:
            logger.warning(f"Intento {intento + 1} fallido para reserva {reserva.pk}: {e}")
            if intento < max_reintentos - 1:
                time.sleep(2 ** intento)  # Backoff exponencial
    
    logger.error(f"Falló el envío de notificación después de {max_reintentos} intentos")
    return False
```

### Cola de Reintentos (Celery)

```python
# tasks.py
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def enviar_notificacion_reprogramacion(self, reserva_id, fecha_anterior_str, motivo):
    try:
        reserva = Reserva.objects.get(id=reserva_id)
        fecha_anterior = datetime.fromisoformat(fecha_anterior_str)
        
        resultado = NotificacionReprogramacion.notificar_cliente(
            reserva, fecha_anterior, motivo
        )
        
        if not resultado:
            raise Exception("Falló el envío de email")
            
    except Exception as exc:
        logger.error(f"Error en notificación: {exc}")
        raise self.retry(exc=exc, countdown=60)
```

## 5. Testing del Sistema

### Test de Notificación de Cliente

```python
from django.test import TestCase
from django.core import mail
from reservas.notifications import NotificacionReprogramacion

class TestNotificacionReprogramacion(TestCase):
    def test_notificar_cliente_exitoso(self):
        # Arrange
        reserva = crear_reserva_test()
        fecha_anterior = datetime(2024, 1, 15, 10, 0)
        motivo = "Prueba"
        
        # Act
        resultado = NotificacionReprogramacion.notificar_cliente(
            reserva, fecha_anterior, motivo
        )
        
        # Assert
        self.assertTrue(resultado)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(f"reserva #{reserva.pk}", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [reserva.usuario.email])
```

## 6. Monitoreo y Métricas

### Métricas Importantes

1. **Tasa de entrega**: Porcentaje de emails enviados exitosamente
2. **Tiempo de envío**: Latencia desde trigger hasta entrega
3. **Errores por tipo**: SMTP, template, datos faltantes
4. **Notificaciones por día**: Volumen de reprogramaciones

### Dashboard de Monitoreo

```python
# views.py
@api_view(['GET'])
@permission_classes([IsAdminUser])
def metricas_notificaciones(request):
    desde = request.GET.get('desde', datetime.now() - timedelta(days=7))
    hasta = request.GET.get('hasta', datetime.now())
    
    # Consultas de métricas
    total_reprogramaciones = HistorialReprogramacion.objects.filter(
        fecha_reprogramacion__range=[desde, hasta]
    ).count()
    
    notificaciones_enviadas = HistorialReprogramacion.objects.filter(
        fecha_reprogramacion__range=[desde, hasta],
        notificacion_enviada=True
    ).count()
    
    tasa_entrega = (notificaciones_enviadas / total_reprogramaciones * 100) if total_reprogramaciones > 0 else 0
    
    return Response({
        'periodo': {'desde': desde, 'hasta': hasta},
        'total_reprogramaciones': total_reprogramaciones,
        'notificaciones_enviadas': notificaciones_enviadas,
        'tasa_entrega': round(tasa_entrega, 2),
    })
```

## 7. Mejores Prácticas

### Seguridad
- ✅ Usar variables de entorno para credenciales SMTP
- ✅ Validar emails antes del envío
- ✅ Rate limiting para prevenir spam
- ✅ Logs sin información sensible

### Performance
- ✅ Envío asíncrono con Celery
- ✅ Templates precargados
- ✅ Connection pooling para SMTP
- ✅ Compresión de imágenes en emails

### Experiencia de Usuario
- ✅ Mensajes claros y personalizados
- ✅ Templates responsive
- ✅ Links de acción (cancelar, contactar)
- ✅ Información completa pero concisa

### Mantenibilidad
- ✅ Separación de responsabilidades
- ✅ Configuración centralizada
- ✅ Tests automatizados
- ✅ Documentación actualizada