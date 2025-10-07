# Ejemplos de Payloads y Templates - Sistema de Notificaciones

## Payloads de API

### 1. Request para Reprogramación

```json
POST /api/reservas/123/reprogramar/
{
    "nueva_fecha": "2025-02-15T14:30:00Z",
    "motivo": "Cliente solicitó cambio de horario por compromisos laborales"
}
```

### 2. Response Exitosa de Reprogramación

```json
{
    "mensaje": "Reserva reprogramada exitosamente",
    "reserva": {
        "id": 123,
        "fecha_inicio": "2024-02-15T14:30:00Z",
        "fecha_fin": "2024-02-15T16:30:00Z",
        "estado": "confirmada",
        "numero_reprogramaciones": 1,
        "total": 150.00,
        "moneda": "BOB"
    },
    "notificaciones": {
        "cliente_notificado": true,
        "soporte_notificado": true
    },
    "historial": {
        "id": 45,
        "fecha_anterior": "2024-02-10T10:00:00Z",
        "fecha_nueva": "2024-02-15T14:30:00Z",
        "motivo": "Cliente solicitó cambio de horario por compromisos laborales",
        "fecha_reprogramacion": "2024-01-20T15:45:00Z"
    }
}
```

### 3. Response con Error en Notificación

```json
{
    "mensaje": "Reserva reprogramada exitosamente",
    "reserva": {
        "id": 123,
        "fecha_inicio": "2024-02-15T14:30:00Z",
        "estado": "confirmada"
    },
    "notificaciones": {
        "cliente_notificado": false,
        "soporte_notificado": true,
        "errores": [
            "Error enviando email al cliente: SMTP connection timeout"
        ]
    },
    "warnings": [
        "La notificación al cliente falló, pero se creó notificación en panel de soporte"
    ]
}
```

### 4. Payload de Notificaciones para Soporte

```json
GET /api/reservas/notificaciones/soporte/

{
    "notificaciones": [
        {
            "id": 45,
            "tipo": "reprogramacion",
            "reserva_id": 123,
            "cliente": {
                "id": 67,
                "nombre": "María Elena Rodríguez",
                "email": "maria.rodriguez@email.com",
                "telefono": "+591 7123-4567"
            },
            "fecha_anterior": "2024-02-10T10:00:00Z",
            "fecha_nueva": "2024-02-15T14:30:00Z",
            "motivo": "Cliente solicitó cambio de horario por compromisos laborales",
            "reprogramado_por": {
                "id": 12,
                "nombre": "Ana Pérez",
                "email": "ana.perez@agencia.com",
                "rol": "Agente de Soporte"
            },
            "timestamp": "2024-01-20T15:45:00Z",
            "total_reserva": 150.00,
            "moneda": "BOB",
            "servicios": [
                {
                    "titulo": "Tour a Samaipata",
                    "cantidad": 2,
                    "precio": 75.00
                }
            ],
            "urgencia": "normal",
            "leida": false
        },
        {
            "id": 44,
            "tipo": "reprogramacion",
            "reserva_id": 119,
            "cliente": {
                "id": 65,
                "nombre": "Carlos Mendoza",
                "email": "carlos.mendoza@email.com",
                "telefono": "+591 7987-6543"
            },
            "fecha_anterior": "2024-02-08T08:00:00Z",
            "fecha_nueva": "2024-02-12T09:00:00Z",
            "motivo": "Problema de transporte",
            "reprogramado_por": {
                "id": 15,
                "nombre": "Luis Vargas",
                "email": "luis.vargas@agencia.com",
                "rol": "Administrador"
            },
            "timestamp": "2024-01-19T11:30:00Z",
            "total_reserva": 320.00,
            "moneda": "BOB",
            "servicios": [
                {
                    "titulo": "Paquete Familiar Sucre",
                    "cantidad": 1,
                    "precio": 320.00
                }
            ],
            "urgencia": "alta",
            "leida": true
        }
    ],
    "total": 2,
    "no_leidas": 1,
    "timestamp_servidor": "2024-01-20T16:00:00Z"
}
```

### 5. WebSocket Payload - Notificación en Tiempo Real

```json
{
    "type": "reprogramacion",
    "data": {
        "reserva_id": 125,
        "cliente_nombre": "Pedro Sánchez",
        "cliente_email": "pedro.sanchez@email.com",
        "fecha_anterior": "2024-02-20T16:00:00Z",
        "fecha_nueva": "2024-02-22T10:00:00Z",
        "motivo": "Cambio de planes de viaje",
        "reprogramado_por": "Sistema Automático",
        "timestamp": "2024-01-20T16:15:00Z",
        "total": 200.00,
        "moneda": "BOB",
        "urgencia": "normal",
        "numero_reprogramaciones": 2
    }
}
```

## Templates de Email

### 1. Template HTML para Cliente

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reprogramación de Reserva</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 25px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .info-box {
            background-color: #f8f9fa;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .warning-box {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .fecha-cambio {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 4px;
        }
        .fecha-anterior {
            color: #dc3545;
            text-decoration: line-through;
            font-weight: normal;
        }
        .fecha-nueva {
            color: #28a745;
            font-weight: bold;
            font-size: 1.1em;
        }
        .servicios-list {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .servicio-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #dee2e6;
        }
        .servicio-item:last-child {
            border-bottom: none;
        }
        .total-box {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin: 20px 0;
        }
        .total-box .total-amount {
            font-size: 1.5em;
            font-weight: bold;
        }
        .contact-info {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 5px;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
        @media (max-width: 600px) {
            .fecha-cambio {
                flex-direction: column;
                align-items: flex-start;
            }
            .servicio-item {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 Reserva Reprogramada</h1>
            <p>Tu reserva #{{ reserva.pk }} ha sido actualizada</p>
        </div>

        <p>Hola <strong>{{ usuario.nombres }} {{ usuario.apellidos }}</strong>,</p>
        
        <p>Te informamos que tu reserva ha sido reprogramada exitosamente según tu solicitud.</p>

        <div class="info-box">
            <h3>📅 Cambio de Fechas</h3>
            <div class="fecha-cambio">
                <div>
                    <strong>Fecha anterior:</strong><br>
                    <span class="fecha-anterior">{{ fecha_anterior|date:"l, d 'de' F 'de' Y 'a las' H:i" }}</span>
                </div>
                <div style="text-align: center; font-size: 1.5em;">→</div>
                <div>
                    <strong>Nueva fecha:</strong><br>
                    <span class="fecha-nueva">{{ fecha_nueva|date:"l, d 'de' F 'de' Y 'a las' H:i" }}</span>
                </div>
            </div>
        </div>

        {% if motivo %}
        <div class="warning-box">
            <strong>💬 Motivo de la reprogramación:</strong><br>
            {{ motivo }}
        </div>
        {% endif %}

        <div class="servicios-list">
            <h3>🎯 Servicios Incluidos</h3>
            {% for detalle in servicios %}
            <div class="servicio-item">
                <span>{{ detalle.servicio.titulo }}</span>
                <span>{{ detalle.cantidad }}x - {{ detalle.precio_unitario }} {{ reserva.moneda }}</span>
            </div>
            {% endfor %}
        </div>

        <div class="total-box">
            <div>💰 Total de tu Reserva</div>
            <div class="total-amount">{{ reserva.total }} {{ reserva.moneda }}</div>
        </div>

        <div class="contact-info">
            <h3>📞 ¿Necesitas ayuda?</h3>
            <p>Si tienes alguna pregunta o necesitas hacer algún cambio adicional, no dudes en contactarnos:</p>
            <a href="mailto:soporte@tuagencia.com" class="button">📧 Enviar Email</a>
            <a href="tel:+59122345678" class="button">📱 Llamar Ahora</a>
        </div>

        <div class="warning-box">
            <strong>⚠️ Importante:</strong> 
            <ul>
                <li>Presenta este email como comprobante de tu reserva</li>
                <li>Llega 15 minutos antes de la hora programada</li>
                <li>Trae documento de identidad válido</li>
            </ul>
        </div>

        <div class="footer">
            <p>¡Esperamos verte pronto!</p>
            <p><strong>Equipo de Turismo Bolivia</strong></p>
            <p>📍 Dirección de la Agencia | 📞 +591 2234-5678 | 🌐 www.tuagencia.com</p>
            <hr>
            <p style="font-size: 0.8em; color: #999;">
                Este email fue enviado automáticamente. Por favor no respondas a esta dirección.
            </p>
        </div>
    </div>
</body>
</html>
```

### 2. Template HTML para Administradores

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notificación Admin - Reprogramación</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 25px;
        }
        .alert-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .cliente-info {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .reserva-info {
            background-color: #f3e5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .cambio-info {
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }
        .info-item {
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .info-item strong {
            color: #495057;
        }
        .servicios-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .servicios-table th,
        .servicios-table td {
            border: 1px solid #dee2e6;
            padding: 12px;
            text-align: left;
        }
        .servicios-table th {
            background-color: #6c757d;
            color: white;
        }
        .acciones {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-warning {
            background-color: #ffc107;
            color: #212529;
        }
        .urgencia-alta {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
        }
        .urgencia-normal {
            background-color: #d1ecf1;
            border-left: 4px solid #17a2b8;
        }
        @media (max-width: 600px) {
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Nueva Reprogramación Registrada</h1>
            <p>Reserva #{{ reserva.pk }} - Acción Requerida</p>
        </div>

        <div class="alert-box">
            <strong>⏰ Notificación de Reprogramación</strong><br>
            Se ha registrado una nueva reprogramación que requiere tu atención.
            Reprogramaciones totales de esta reserva: <strong>{{ reserva.numero_reprogramaciones }}</strong>
        </div>

        <div class="cliente-info">
            <h3>👤 Información del Cliente</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Nombre:</strong><br>
                    {{ usuario.nombres }} {{ usuario.apellidos }}
                </div>
                <div class="info-item">
                    <strong>Email:</strong><br>
                    <a href="mailto:{{ usuario.email }}">{{ usuario.email }}</a>
                </div>
                <div class="info-item">
                    <strong>Teléfono:</strong><br>
                    {% if usuario.telefono %}
                        <a href="tel:{{ usuario.telefono }}">{{ usuario.telefono }}</a>
                    {% else %}
                        <em>No proporcionado</em>
                    {% endif %}
                </div>
                <div class="info-item">
                    <strong>Cliente desde:</strong><br>
                    {{ usuario.date_joined|date:"d/m/Y" }}
                </div>
            </div>
        </div>

        <div class="reserva-info">
            <h3>📋 Detalles de la Reserva</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>ID Reserva:</strong><br>
                    #{{ reserva.pk }}
                </div>
                <div class="info-item">
                    <strong>Estado:</strong><br>
                    {{ reserva.estado|capfirst }}
                </div>
                <div class="info-item">
                    <strong>Total:</strong><br>
                    {{ reserva.total }} {{ reserva.moneda }}
                </div>
                <div class="info-item">
                    <strong>Forma de Pago:</strong><br>
                    {{ reserva.forma_pago|default:"No especificado" }}
                </div>
            </div>
        </div>

        <div class="cambio-info {% if reserva.numero_reprogramaciones > 2 %}urgencia-alta{% else %}urgencia-normal{% endif %}">
            <h3>🔄 Detalles del Cambio</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Fecha Anterior:</strong><br>
                    <span style="color: #dc3545; text-decoration: line-through;">
                        {{ fecha_anterior|date:"l, d 'de' F 'de' Y 'a las' H:i" }}
                    </span>
                </div>
                <div class="info-item">
                    <strong>Nueva Fecha:</strong><br>
                    <span style="color: #28a745; font-weight: bold;">
                        {{ fecha_nueva|date:"l, d 'de' F 'de' Y 'a las' H:i" }}
                    </span>
                </div>
                <div class="info-item">
                    <strong>Reprogramado por:</strong><br>
                    {{ reprogramado_por.nombres }} {{ reprogramado_por.apellidos }}<br>
                    <small>{{ reprogramado_por.email }}</small>
                </div>
                <div class="info-item">
                    <strong>Fecha de Reprogramación:</strong><br>
                    {{ fecha_reprogramacion|date:"d/m/Y H:i" }}
                </div>
            </div>

            {% if motivo %}
            <div style="margin-top: 15px; padding: 10px; background-color: #fff3cd; border-radius: 5px;">
                <strong>💬 Motivo:</strong><br>
                {{ motivo }}
            </div>
            {% else %}
            <div style="margin-top: 15px; padding: 10px; background-color: #f8d7da; border-radius: 5px;">
                <strong>⚠️ Sin motivo especificado</strong>
            </div>
            {% endif %}
        </div>

        <h3>🎯 Servicios Incluidos</h3>
        <table class="servicios-table">
            <thead>
                <tr>
                    <th>Servicio</th>
                    <th>Cantidad</th>
                    <th>Precio Unitario</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                {% for detalle in servicios %}
                <tr>
                    <td>{{ detalle.servicio.titulo }}</td>
                    <td>{{ detalle.cantidad }}</td>
                    <td>{{ detalle.precio_unitario }} {{ reserva.moneda }}</td>
                    <td>{{ detalle.cantidad|mul:detalle.precio_unitario }} {{ reserva.moneda }}</td>
                </tr>
                {% endfor %}
            </tbody>
            <tfoot>
                <tr style="background-color: #f8f9fa; font-weight: bold;">
                    <td colspan="3">Total</td>
                    <td>{{ reserva.total }} {{ reserva.moneda }}</td>
                </tr>
            </tfoot>
        </table>

        <div class="acciones">
            <h3>🎯 Acciones Requeridas</h3>
            <ul>
                <li><strong>Verificar disponibilidad</strong> para la nueva fecha y hora</li>
                <li><strong>Confirmar recursos</strong> (guías, transporte, equipos)</li>
                <li><strong>Contactar al cliente</strong> si hay algún problema</li>
                <li><strong>Actualizar calendario</strong> de disponibilidad</li>
                {% if reserva.numero_reprogramaciones > 2 %}
                <li style="color: #dc3545;"><strong>⚠️ ATENCIÓN:</strong> Esta reserva ha sido reprogramada {{ reserva.numero_reprogramaciones }} veces</li>
                {% endif %}
            </ul>

            <div style="text-align: center; margin-top: 20px;">
                <a href="http://admin.tuagencia.com/reservas/{{ reserva.pk }}/" class="button btn-primary">
                    📋 Ver Reserva Completa
                </a>
                <a href="mailto:{{ usuario.email }}?subject=Reprogramación Reserva #{{ reserva.pk }}" class="button btn-success">
                    📧 Contactar Cliente
                </a>
                <a href="http://admin.tuagencia.com/calendario/" class="button btn-warning">
                    📅 Ver Calendario
                </a>
            </div>
        </div>

        {% if reserva.numero_reprogramaciones > 2 %}
        <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4 style="color: #721c24; margin-top: 0;">🚨 Alerta: Múltiples Reprogramaciones</h4>
            <p>Esta reserva ha sido reprogramada <strong>{{ reserva.numero_reprogramaciones }} veces</strong>. 
            Considera contactar al cliente para entender mejor sus necesidades o evaluar alternativas.</p>
        </div>
        {% endif %}

        <div style="text-align: center; margin-top: 30px; color: #666; font-size: 0.9em;">
            <p>Sistema de Gestión de Reservas - Turismo Bolivia</p>
            <p>Notificación automática generada el {{ "now"|date:"d/m/Y H:i" }}</p>
        </div>
    </div>
</body>
</html>
```

### 3. Template de Email de Texto Plano (Fallback)

```text
# Para Cliente
REPROGRAMACIÓN DE RESERVA #{{ reserva.pk }}

Hola {{ usuario.nombres }} {{ usuario.apellidos }},

Tu reserva ha sido reprogramada exitosamente.

DETALLES DEL CAMBIO:
- Fecha anterior: {{ fecha_anterior|date:"d/m/Y H:i" }}
- Nueva fecha: {{ fecha_nueva|date:"d/m/Y H:i" }}
- Estado: {{ reserva.estado }}
- Total: {{ reserva.total }} {{ reserva.moneda }}

{% if motivo %}
MOTIVO: {{ motivo }}
{% endif %}

SERVICIOS INCLUIDOS:
{% for detalle in servicios %}
- {{ detalle.servicio.titulo }} (x{{ detalle.cantidad }})
{% endfor %}

INFORMACIÓN IMPORTANTE:
- Llega 15 minutos antes
- Trae documento de identidad
- Conserva este email como comprobante

¿Preguntas? Contáctanos:
📧 soporte@tuagencia.com
📞 +591 2234-5678

¡Esperamos verte!
Equipo de Turismo Bolivia
```

```text
# Para Administradores
NUEVA REPROGRAMACIÓN - RESERVA #{{ reserva.pk }}

CLIENTE: {{ usuario.nombres }} {{ usuario.apellidos }}
EMAIL: {{ usuario.email }}
TELÉFONO: {{ usuario.telefono|default:"No proporcionado" }}

CAMBIO DE FECHA:
- Anterior: {{ fecha_anterior|date:"d/m/Y H:i" }}
- Nueva: {{ fecha_nueva|date:"d/m/Y H:i" }}
- Reprogramado por: {{ reprogramado_por.nombres }} {{ reprogramado_por.apellidos }}
- Total reprogramaciones: {{ reserva.numero_reprogramaciones }}

{% if motivo %}
MOTIVO: {{ motivo }}
{% else %}
MOTIVO: Sin especificar
{% endif %}

SERVICIOS:
{% for detalle in servicios %}
- {{ detalle.servicio.titulo }} (x{{ detalle.cantidad }}) - {{ detalle.precio_unitario }} {{ reserva.moneda }}
{% endfor %}

TOTAL: {{ reserva.total }} {{ reserva.moneda }}

ACCIONES REQUERIDAS:
- Verificar disponibilidad para nueva fecha
- Confirmar recursos necesarios
- Contactar cliente si hay problemas
- Actualizar calendario

{% if reserva.numero_reprogramaciones > 2 %}
⚠️ ALERTA: Esta reserva ha sido reprogramada {{ reserva.numero_reprogramaciones }} veces
{% endif %}

Ver reserva completa: http://admin.tuagencia.com/reservas/{{ reserva.pk }}/
```

## Variables de Contexto Disponibles

### Para Templates de Cliente
```python
{
    'usuario': reserva.usuario,  # Objeto Usuario completo
    'reserva': reserva,          # Objeto Reserva completo
    'fecha_anterior': datetime,  # Fecha anterior de la reserva
    'fecha_nueva': reserva.fecha_inicio,  # Nueva fecha
    'motivo': motivo,           # Motivo de reprogramación (opcional)
    'servicios': reserva.detalles.all(),  # QuerySet de detalles
}
```

### Para Templates de Administrador
```python
{
    'reserva': reserva,
    'usuario': reserva.usuario,
    'fecha_anterior': datetime,
    'fecha_nueva': reserva.fecha_inicio,
    'reprogramado_por': user_object,  # Usuario que reprogramó
    'motivo': motivo,
    'servicios': reserva.detalles.all(),
    'fecha_reprogramacion': timezone.now(),
}
```

## Configuración de Desarrollo y Testing

### Variables de Entorno para Testing
```env
# .env.testing
EMAIL_BACKEND=django.core.mail.backends.locmem.EmailBackend
ADMIN_EMAILS=test@localhost,admin@localhost
DEFAULT_FROM_EMAIL=test@sistema.com
```

### Payload de Testing
```python
# Para tests automatizados
test_payload = {
    "reserva_id": 123,
    "fecha_inicio": "2024-02-15T14:30:00Z",
    "motivo": "Testing reprogramación automática",
    "esperado": {
        "cliente_notificado": True,
        "admin_notificado": True,
        "emails_enviados": 2
    }
}
```