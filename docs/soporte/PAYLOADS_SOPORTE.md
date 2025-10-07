# Payloads del Sistema de Soporte - Ejemplos Completos

## Descripción General
Esta documentación contiene todos los payloads de ejemplo para el sistema de soporte, incluyendo requests, responses y estructuras de datos para tickets, chat, FAQ y gestión de casos.

## 1. TICKETS DE SOPORTE

### 1.1 Crear Ticket

**Request:**
```json
POST /api/soporte/tickets/
Content-Type: application/json
Authorization: Bearer <token>

{
  "asunto": "Problema con el pago de mi reserva",
  "categoria": "PAGOS",
  "prioridad": "ALTA",
  "descripcion": "No puedo completar el pago de mi reserva #123. Al hacer clic en 'Pagar', la página se queda cargando y no procesa el pago. He intentado con diferentes tarjetas.",
  "archivos_adjuntos": [
    {
      "nombre": "screenshot_error.png",
      "tipo": "image/png",
      "tamaño": 245760,
      "base64": "iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reserva_relacionada": 123,
  "informacion_tecnica": {
    "navegador": "Chrome 119.0.0.0",
    "sistema_operativo": "Windows 11",
    "url_error": "/reservas/123/pago",
    "codigo_error": null
  }
}
```

**Response (201 Created):**
```json
{
  "id": 456,
  "numero": "TK-2024-000456",
  "asunto": "Problema con el pago de mi reserva",
  "categoria": "PAGOS",
  "prioridad": "ALTA",
  "estado": "ABIERTO",
  "descripcion": "No puedo completar el pago de mi reserva #123...",
  "fecha_creacion": "2024-09-20T14:30:00Z",
  "fecha_actualizacion": "2024-09-20T14:30:00Z",
  "fecha_vencimiento": "2024-09-22T14:30:00Z",
  "cliente": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan.perez@email.com",
    "telefono": "+591 70123456"
  },
  "agente_asignado": null,
  "reserva_relacionada": {
    "id": 123,
    "numero": "RSV-2024-000123",
    "fecha_evento": "2024-09-25T18:00:00Z",
    "estado": "PENDIENTE_PAGO",
    "total": 1500.00
  },
  "archivos_adjuntos": [
    {
      "id": 789,
      "nombre": "screenshot_error.png",
      "tipo": "image/png",
      "tamaño": 245760,
      "url": "https://api.domain.com/media/tickets/456/screenshot_error.png",
      "fecha_subida": "2024-09-20T14:30:00Z"
    }
  ],
  "tiempo_estimado_resolucion": "24:00:00",
  "sla_vencimiento": "2024-09-21T14:30:00Z",
  "tags": ["pago", "reserva", "urgente"],
  "estadisticas": {
    "respuestas_totales": 0,
    "tiempo_primera_respuesta": null,
    "tiempo_total_resolucion": null,
    "escalamientos": 0
  }
}
```

### 1.2 Obtener Lista de Tickets

**Request:**
```json
GET /api/soporte/mis-tickets/?page=1&size=10&estado=ABIERTO&categoria=PAGOS&fecha_desde=2024-09-01
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/soporte/mis-tickets/?page=2&size=10&estado=ABIERTO",
  "previous": null,
  "results": [
    {
      "id": 456,
      "numero": "TK-2024-000456",
      "asunto": "Problema con el pago de mi reserva",
      "categoria": "PAGOS",
      "prioridad": "ALTA",
      "estado": "ABIERTO",
      "fecha_creacion": "2024-09-20T14:30:00Z",
      "fecha_actualizacion": "2024-09-20T14:30:00Z",
      "agente_asignado": {
        "id": 5,
        "nombre": "María Rodríguez",
        "email": "maria.rodriguez@soporte.com",
        "avatar": "https://api.domain.com/media/avatars/maria.jpg"
      },
      "ultima_respuesta": {
        "fecha": "2024-09-20T15:45:00Z",
        "autor": "María Rodríguez",
        "tipo": "AGENTE",
        "resumen": "Hemos identificado el problema y estamos..."
      },
      "reserva_relacionada": {
        "id": 123,
        "numero": "RSV-2024-000123",
        "fecha_evento": "2024-09-25T18:00:00Z"
      },
      "tiempo_sin_respuesta": "02:15:00",
      "sla_estado": "EN_TIEMPO",
      "satisfaccion": null
    },
    {
      "id": 455,
      "numero": "TK-2024-000455",
      "asunto": "Consulta sobre cambio de fecha",
      "categoria": "RESERVAS",
      "prioridad": "MEDIA",
      "estado": "EN_PROGRESO",
      "fecha_creacion": "2024-09-19T10:15:00Z",
      "fecha_actualizacion": "2024-09-20T09:30:00Z",
      "agente_asignado": {
        "id": 3,
        "nombre": "Carlos López",
        "email": "carlos.lopez@soporte.com",
        "avatar": "https://api.domain.com/media/avatars/carlos.jpg"
      },
      "ultima_respuesta": {
        "fecha": "2024-09-20T09:30:00Z",
        "autor": "Juan Pérez",
        "tipo": "CLIENTE",
        "resumen": "Perfecto, procedo con el cambio entonces..."
      },
      "reserva_relacionada": {
        "id": 120,
        "numero": "RSV-2024-000120",
        "fecha_evento": "2024-10-02T16:00:00Z"
      },
      "tiempo_sin_respuesta": "05:00:00",
      "sla_estado": "EN_TIEMPO",
      "satisfaccion": 4.5
    }
  ],
  "filtros_aplicados": {
    "estado": "ABIERTO",
    "categoria": "PAGOS",
    "fecha_desde": "2024-09-01",
    "fecha_hasta": null
  },
  "estadisticas_resumen": {
    "total_tickets": 25,
    "abiertos": 12,
    "en_progreso": 8,
    "resueltos": 4,
    "cerrados": 1,
    "tiempo_promedio_respuesta": "04:30:00"
  }
}
```

### 1.3 Detalle de Ticket

**Request:**
```json
GET /api/soporte/tickets/456/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 456,
  "numero": "TK-2024-000456",
  "asunto": "Problema con el pago de mi reserva",
  "categoria": "PAGOS",
  "prioridad": "ALTA",
  "estado": "EN_PROGRESO",
  "descripcion": "No puedo completar el pago de mi reserva #123...",
  "fecha_creacion": "2024-09-20T14:30:00Z",
  "fecha_actualizacion": "2024-09-20T16:45:00Z",
  "fecha_vencimiento": "2024-09-22T14:30:00Z",
  "cliente": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan.perez@email.com",
    "telefono": "+591 70123456",
    "historial_tickets": {
      "total": 5,
      "resueltos": 4,
      "satisfaccion_promedio": 4.2
    }
  },
  "agente_asignado": {
    "id": 5,
    "nombre": "María Rodríguez",
    "email": "maria.rodriguez@soporte.com",
    "avatar": "https://api.domain.com/media/avatars/maria.jpg",
    "departamento": "Pagos y Facturación",
    "experiencia_años": 3,
    "tickets_resueltos": 1250,
    "rating_promedio": 4.8
  },
  "reserva_relacionada": {
    "id": 123,
    "numero": "RSV-2024-000123",
    "fecha_evento": "2024-09-25T18:00:00Z",
    "estado": "PENDIENTE_PAGO",
    "total": 1500.00,
    "servicios": [
      {
        "id": 1,
        "nombre": "Catering Premium",
        "precio": 1200.00
      },
      {
        "id": 2,
        "nombre": "Decoración Especial",
        "precio": 300.00
      }
    ],
    "cliente": {
      "nombre": "Juan Pérez",
      "email": "juan.perez@email.com"
    }
  },
  "respuestas": [
    {
      "id": 1001,
      "autor": {
        "id": 1,
        "nombre": "Juan Pérez",
        "tipo": "CLIENTE",
        "avatar": null
      },
      "mensaje": "No puedo completar el pago de mi reserva #123. Al hacer clic en 'Pagar', la página se queda cargando y no procesa el pago.",
      "fecha_creacion": "2024-09-20T14:30:00Z",
      "archivos_adjuntos": [
        {
          "id": 789,
          "nombre": "screenshot_error.png",
          "tipo": "image/png",
          "url": "https://api.domain.com/media/tickets/456/screenshot_error.png"
        }
      ],
      "es_interno": false,
      "tiempo_respuesta": null
    },
    {
      "id": 1002,
      "autor": {
        "id": 5,
        "nombre": "María Rodríguez",
        "tipo": "AGENTE",
        "avatar": "https://api.domain.com/media/avatars/maria.jpg"
      },
      "mensaje": "Hola Juan, gracias por contactarnos. He revisado tu reserva y veo el problema. Parece ser un issue con el gateway de pagos. Voy a escalarlo al equipo técnico inmediatamente.",
      "fecha_creacion": "2024-09-20T15:45:00Z",
      "archivos_adjuntos": [],
      "es_interno": false,
      "tiempo_respuesta": "01:15:00",
      "acciones_realizadas": [
        "Revisión de logs de pago",
        "Verificación de estado de gateway",
        "Escalamiento a equipo técnico"
      ]
    },
    {
      "id": 1003,
      "autor": {
        "id": 7,
        "nombre": "Sistema Automático",
        "tipo": "SISTEMA",
        "avatar": null
      },
      "mensaje": "NOTA INTERNA: Ticket escalado al equipo técnico. Asignado a TechTeam-Level2.",
      "fecha_creacion": "2024-09-20T15:46:00Z",
      "archivos_adjuntos": [],
      "es_interno": true,
      "tiempo_respuesta": null,
      "metadatos": {
        "escalamiento_nivel": 2,
        "equipo_destino": "TechTeam-Level2",
        "razon_escalamiento": "Problema técnico gateway pagos"
      }
    },
    {
      "id": 1004,
      "autor": {
        "id": 5,
        "nombre": "María Rodríguez",
        "tipo": "AGENTE",
        "avatar": "https://api.domain.com/media/avatars/maria.jpg"
      },
      "mensaje": "Juan, hemos identificado y solucionado el problema. Era un issue temporal con nuestro proveedor de pagos. Por favor intenta realizar el pago nuevamente. Si persiste el problema, avísame inmediatamente.",
      "fecha_creacion": "2024-09-20T16:45:00Z",
      "archivos_adjuntos": [],
      "es_interno": false,
      "tiempo_respuesta": "01:00:00",
      "solucion_propuesta": "Gateway de pagos reparado - cliente puede intentar pago nuevamente"
    }
  ],
  "archivos_adjuntos": [
    {
      "id": 789,
      "nombre": "screenshot_error.png",
      "tipo": "image/png",
      "tamaño": 245760,
      "url": "https://api.domain.com/media/tickets/456/screenshot_error.png",
      "fecha_subida": "2024-09-20T14:30:00Z",
      "subido_por": {
        "id": 1,
        "nombre": "Juan Pérez"
      }
    }
  ],
  "historial_estados": [
    {
      "estado": "ABIERTO",
      "fecha": "2024-09-20T14:30:00Z",
      "cambiado_por": {
        "id": 1,
        "nombre": "Juan Pérez",
        "tipo": "CLIENTE"
      },
      "motivo": "Ticket creado"
    },
    {
      "estado": "ASIGNADO",
      "fecha": "2024-09-20T15:30:00Z",
      "cambiado_por": {
        "id": 10,
        "nombre": "Sistema de Asignación",
        "tipo": "SISTEMA"
      },
      "motivo": "Asignado automáticamente a María Rodríguez (especialista en pagos)"
    },
    {
      "estado": "EN_PROGRESO",
      "fecha": "2024-09-20T15:45:00Z",
      "cambiado_por": {
        "id": 5,
        "nombre": "María Rodríguez",
        "tipo": "AGENTE"
      },
      "motivo": "Iniciando investigación del problema"
    }
  ],
  "escalamientos": [
    {
      "id": 201,
      "nivel_anterior": 1,
      "nivel_actual": 2,
      "fecha_escalamiento": "2024-09-20T15:46:00Z",
      "motivo": "Problema técnico requiere equipo especializado",
      "escalado_por": {
        "id": 5,
        "nombre": "María Rodríguez"
      },
      "equipo_destino": "TechTeam-Level2",
      "tiempo_en_nivel_anterior": "01:16:00"
    }
  ],
  "sla": {
    "tiempo_primera_respuesta": {
      "objetivo": "01:00:00",
      "actual": "01:15:00",
      "estado": "INCUMPLIDO",
      "porcentaje": 125
    },
    "tiempo_resolucion": {
      "objetivo": "24:00:00",
      "actual": "02:15:00",
      "estado": "EN_TIEMPO",
      "porcentaje": 9.375
    },
    "vencimiento": "2024-09-22T14:30:00Z",
    "tiempo_restante": "21:45:00"
  },
  "satisfaccion": null,
  "tags": ["pago", "reserva", "urgente", "gateway", "escalado"],
  "metadatos": {
    "origen": "WEB",
    "navegador": "Chrome 119.0.0.0",
    "sistema_operativo": "Windows 11",
    "direccion_ip": "192.168.1.100",
    "sesion_id": "sess_abc123def456",
    "campana_marketing": null
  }
}
```

### 1.4 Responder a Ticket

**Request:**
```json
POST /api/soporte/tickets/456/responder/
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- mensaje: "Perfecto, acabo de intentar nuevamente y ya pude completar el pago. Muchas gracias por la rápida solución!"
- archivo_0: [archivo binario]
- notificar_agente: true
- cambiar_estado: "RESUELTO"
```

**Response (201 Created):**
```json
{
  "id": 1005,
  "autor": {
    "id": 1,
    "nombre": "Juan Pérez",
    "tipo": "CLIENTE",
    "avatar": null
  },
  "mensaje": "Perfecto, acabo de intentar nuevamente y ya pude completar el pago. Muchas gracias por la rápida solución!",
  "fecha_creacion": "2024-09-20T17:30:00Z",
  "archivos_adjuntos": [
    {
      "id": 790,
      "nombre": "pago_exitoso.png",
      "tipo": "image/png",
      "url": "https://api.domain.com/media/tickets/456/pago_exitoso.png"
    }
  ],
  "es_interno": false,
  "ticket": {
    "id": 456,
    "estado": "RESUELTO",
    "fecha_actualizacion": "2024-09-20T17:30:00Z"
  },
  "notificaciones_enviadas": [
    {
      "destinatario": "maria.rodriguez@soporte.com",
      "tipo": "EMAIL",
      "estado": "ENVIADO"
    },
    {
      "destinatario": "sistema",
      "tipo": "WEBHOOK",
      "estado": "ENVIADO"
    }
  ],
  "tiempo_respuesta": "00:45:00"
}
```

## 2. CHAT EN TIEMPO REAL

### 2.1 Establecer Conexión WebSocket

**WebSocket URL:**
```
ws://localhost:8000/ws/soporte/ticket/456/?token=<jwt_token>
```

**Mensaje de Conexión Establecida:**
```json
{
  "tipo": "connection_established",
  "data": {
    "ticket_id": 456,
    "chat_id": "chat_456_abc123",
    "usuario": {
      "id": 1,
      "nombre": "Juan Pérez",
      "tipo": "CLIENTE"
    },
    "agente_online": {
      "id": 5,
      "nombre": "María Rodríguez",
      "estado": "DISPONIBLE",
      "ultima_actividad": "2024-09-20T17:25:00Z"
    },
    "historial_reciente": [
      {
        "id": "msg_001",
        "autor": "María Rodríguez",
        "mensaje": "¡Hola! Veo que tu problema de pago ya está resuelto. ¿Hay algo más en lo que pueda ayudarte?",
        "timestamp": "2024-09-20T17:20:00Z",
        "tipo": "AGENTE"
      }
    ],
    "configuracion": {
      "max_file_size": 10485760,
      "allowed_file_types": ["jpg", "png", "pdf", "doc", "docx"],
      "typing_timeout": 3000,
      "auto_disconnect": 1800000
    }
  },
  "timestamp": "2024-09-20T17:30:00Z"
}
```

### 2.2 Enviar Mensaje de Chat

**Mensaje Enviado (Cliente → Servidor):**
```json
{
  "tipo": "mensaje",
  "data": {
    "mensaje": "Hola María, sí, tengo una pregunta sobre los servicios adicionales que puedo agregar a mi reserva.",
    "ticket_id": 456,
    "reply_to": null,
    "archivos": [],
    "metadata": {
      "client_timestamp": "2024-09-20T17:31:00Z",
      "client_id": "client_uuid_123"
    }
  }
}
```

**Confirmación del Servidor:**
```json
{
  "tipo": "mensaje_confirmado",
  "data": {
    "mensaje_id": "msg_002",
    "client_id": "client_uuid_123",
    "timestamp": "2024-09-20T17:31:05Z",
    "estado": "ENTREGADO"
  }
}
```

**Mensaje Recibido (Servidor → Cliente):**
```json
{
  "tipo": "mensaje_recibido",
  "data": {
    "id": "msg_003",
    "autor": {
      "id": 5,
      "nombre": "María Rodríguez",
      "tipo": "AGENTE",
      "avatar": "https://api.domain.com/media/avatars/maria.jpg"
    },
    "mensaje": "¡Por supuesto! Te puedo ayudar con eso. ¿Qué tipo de servicios adicionales te interesan? Tenemos catering, decoración, música en vivo, fotógrafo, entre otros.",
    "timestamp": "2024-09-20T17:32:00Z",
    "ticket_id": 456,
    "reply_to": "msg_002",
    "archivos": [],
    "acciones_sugeridas": [
      {
        "texto": "Ver catálogo de servicios",
        "url": "/catalogo/servicios",
        "tipo": "LINK"
      },
      {
        "texto": "Contactar con especialista",
        "accion": "transfer_to_sales",
        "tipo": "ACTION"
      }
    ]
  }
}
```

### 2.3 Indicador de Escritura

**Cliente Escribiendo:**
```json
{
  "tipo": "typing_start",
  "data": {
    "ticket_id": 456,
    "usuario_id": 1
  }
}
```

**Cliente Dejó de Escribir:**
```json
{
  "tipo": "typing_stop",
  "data": {
    "ticket_id": 456,
    "usuario_id": 1
  }
}
```

**Notificación de Escritura:**
```json
{
  "tipo": "usuario_escribiendo",
  "data": {
    "usuario": {
      "id": 5,
      "nombre": "María Rodríguez",
      "tipo": "AGENTE"
    },
    "timestamp": "2024-09-20T17:33:00Z",
    "duracion_estimada": 3000
  }
}
```

### 2.4 Envío de Archivos en Chat

**Solicitud de Upload:**
```json
{
  "tipo": "file_upload_request",
  "data": {
    "nombre_archivo": "catalogo_servicios.pdf",
    "tamaño": 2048576,
    "tipo_mime": "application/pdf",
    "ticket_id": 456
  }
}
```

**Autorización de Upload:**
```json
{
  "tipo": "file_upload_authorized",
  "data": {
    "upload_id": "upload_789abc",
    "upload_url": "https://api.domain.com/api/soporte/chat/upload/upload_789abc/",
    "headers": {
      "Authorization": "Bearer temp_upload_token_xyz"
    },
    "expira_en": 300
  }
}
```

**Confirmación de Archivo Subido:**
```json
{
  "tipo": "file_uploaded",
  "data": {
    "archivo_id": "file_456def",
    "nombre": "catalogo_servicios.pdf",
    "url": "https://api.domain.com/media/chat/456/catalogo_servicios.pdf",
    "tamaño": 2048576,
    "tipo_mime": "application/pdf",
    "thumbnail": "https://api.domain.com/media/chat/456/thumbs/catalogo_servicios.jpg",
    "mensaje_id": "msg_004",
    "timestamp": "2024-09-20T17:35:00Z"
  }
}
```

### 2.5 Transferencia de Chat

**Transferir a Otro Agente:**
```json
{
  "tipo": "transfer_chat",
  "data": {
    "ticket_id": 456,
    "agente_destino": {
      "id": 8,
      "nombre": "Carlos López",
      "departamento": "Ventas",
      "especialidad": "Servicios Adicionales"
    },
    "motivo": "Cliente interesado en servicios adicionales",
    "notas_transferencia": "Cliente pregunta sobre catering y decoración para reserva #123",
    "mantener_historial": true
  }
}
```

**Notificación de Transferencia:**
```json
{
  "tipo": "chat_transferred",
  "data": {
    "nuevo_agente": {
      "id": 8,
      "nombre": "Carlos López",
      "avatar": "https://api.domain.com/media/avatars/carlos.jpg",
      "departamento": "Ventas",
      "estado": "DISPONIBLE"
    },
    "agente_anterior": {
      "id": 5,
      "nombre": "María Rodríguez"
    },
    "motivo": "Cliente interesado en servicios adicionales",
    "timestamp": "2024-09-20T17:36:00Z",
    "mensaje_automatico": "Hola Juan, soy Carlos del equipo de ventas. María me ha transferido tu consulta sobre servicios adicionales. ¿En qué puedo ayudarte específicamente?"
  }
}
```

## 3. SISTEMA FAQ

### 3.1 Obtener FAQs

**Request:**
```json
GET /api/soporte/faqs/?categoria=PAGOS&q=pago&activas=true&page=1&size=10
```

**Response (200 OK):**
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/soporte/faqs/?page=2&categoria=PAGOS",
  "previous": null,
  "results": [
    {
      "id": 1,
      "pregunta": "¿Qué métodos de pago aceptan?",
      "respuesta": "Aceptamos tarjetas de crédito y débito (Visa, Mastercard, American Express), transferencias bancarias, y pagos en efectivo en nuestras oficinas. También trabajamos con QR de Tigo Money y otras billeteras digitales.",
      "categoria": "PAGOS",
      "subcategoria": "METODOS_PAGO",
      "tags": ["pago", "tarjeta", "transferencia", "efectivo", "qr"],
      "fecha_creacion": "2024-01-15T10:00:00Z",
      "fecha_actualizacion": "2024-09-10T14:30:00Z",
      "activa": true,
      "orden": 1,
      "autor": {
        "id": 10,
        "nombre": "Admin Sistema",
        "departamento": "Soporte"
      },
      "estadisticas": {
        "visualizaciones": 2450,
        "valoraciones_positivas": 198,
        "valoraciones_negativas": 12,
        "porcentaje_utilidad": 94.3,
        "ultima_valoracion": "2024-09-20T15:30:00Z"
      },
      "contenido_relacionado": [
        {
          "tipo": "FAQ",
          "id": 2,
          "titulo": "¿Puedo pagar en cuotas?"
        },
        {
          "tipo": "ARTICULO",
          "id": 15,
          "titulo": "Guía completa de pagos"
        }
      ]
    },
    {
      "id": 2,
      "pregunta": "¿Puedo pagar en cuotas?",
      "respuesta": "Sí, ofrecemos planes de pago en cuotas para reservas superiores a Bs. 1000. Puedes dividir el pago en 2, 3 o 6 cuotas sin intereses con tarjetas de crédito participantes. Para montos mayores a Bs. 5000, también tenemos planes especiales de hasta 12 cuotas.",
      "categoria": "PAGOS",
      "subcategoria": "FINANCIAMIENTO",
      "tags": ["cuotas", "financiamiento", "tarjeta", "sin intereses"],
      "fecha_creacion": "2024-01-15T10:05:00Z",
      "fecha_actualizacion": "2024-08-20T11:15:00Z",
      "activa": true,
      "orden": 2,
      "autor": {
        "id": 10,
        "nombre": "Admin Sistema",
        "departamento": "Soporte"
      },
      "estadisticas": {
        "visualizaciones": 1890,
        "valoraciones_positivas": 145,
        "valoraciones_negativas": 8,
        "porcentaje_utilidad": 94.8,
        "ultima_valoracion": "2024-09-19T18:45:00Z"
      },
      "contenido_relacionado": [
        {
          "tipo": "FAQ",
          "id": 1,
          "titulo": "¿Qué métodos de pago aceptan?"
        },
        {
          "tipo": "CALCULADORA",
          "id": 1,
          "titulo": "Calculadora de cuotas"
        }
      ]
    }
  ],
  "categorias_disponibles": [
    {
      "categoria": "PAGOS",
      "nombre": "Pagos y Facturación",
      "count": 15,
      "subcategorias": [
        {"codigo": "METODOS_PAGO", "nombre": "Métodos de Pago", "count": 5},
        {"codigo": "FINANCIAMIENTO", "nombre": "Financiamiento", "count": 4},
        {"codigo": "FACTURACION", "nombre": "Facturación", "count": 6}
      ]
    },
    {
      "categoria": "RESERVAS",
      "nombre": "Reservas y Eventos",
      "count": 20,
      "subcategorias": [
        {"codigo": "PROCESO_RESERVA", "nombre": "Proceso de Reserva", "count": 8},
        {"codigo": "MODIFICACIONES", "nombre": "Modificaciones", "count": 7},
        {"codigo": "CANCELACIONES", "nombre": "Cancelaciones", "count": 5}
      ]
    }
  ],
  "filtros_aplicados": {
    "categoria": "PAGOS",
    "busqueda": "pago",
    "solo_activas": true
  },
  "sugerencias_busqueda": [
    "métodos de pago",
    "pago en cuotas",
    "transferencia bancaria",
    "pago con QR"
  ]
}
```

### 3.2 Valorar FAQ

**Request:**
```json
POST /api/soporte/faqs/1/valorar/
Content-Type: application/json
Authorization: Bearer <token>

{
  "es_util": true,
  "comentario": "Muy útil, me ayudó a entender todos los métodos disponibles",
  "categoria_feedback": "COMPLETA",
  "sugerencia_mejora": null
}
```

**Response (200 OK):**
```json
{
  "id": 501,
  "faq": {
    "id": 1,
    "pregunta": "¿Qué métodos de pago aceptan?"
  },
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez"
  },
  "es_util": true,
  "comentario": "Muy útil, me ayudó a entender todos los métodos disponibles",
  "categoria_feedback": "COMPLETA",
  "fecha_valoracion": "2024-09-20T17:40:00Z",
  "estadisticas_actualizadas": {
    "valoraciones_positivas": 199,
    "valoraciones_negativas": 12,
    "porcentaje_utilidad": 94.3,
    "total_valoraciones": 211
  },
  "agradecimiento": {
    "mensaje": "¡Gracias por tu valoración! Nos ayuda a mejorar nuestro contenido.",
    "puntos_obtenidos": 5
  }
}
```

### 3.3 Búsqueda Inteligente de FAQs

**Request:**
```json
POST /api/soporte/faqs/busqueda-inteligente/
Content-Type: application/json

{
  "consulta": "no me funciona el pago con tarjeta",
  "contexto": {
    "ticket_id": 456,
    "categoria_preferida": "PAGOS",
    "historial_usuario": ["pagos", "tarjetas", "problemas técnicos"]
  },
  "incluir_sugerencias": true,
  "max_resultados": 5
}
```

**Response (200 OK):**
```json
{
  "resultados": [
    {
      "faq": {
        "id": 15,
        "pregunta": "Mi tarjeta de crédito no funciona, ¿qué puedo hacer?",
        "respuesta": "Si tu tarjeta no funciona, verifica: 1) Que tengas fondos suficientes...",
        "categoria": "PAGOS",
        "relevancia_score": 0.95
      },
      "fragmentos_destacados": [
        "tarjeta de crédito no funciona",
        "verifica que tengas fondos suficientes",
        "problemas con el gateway de pagos"
      ],
      "motivo_relevancia": "Coincidencia exacta con problema reportado"
    },
    {
      "faq": {
        "id": 16,
        "pregunta": "¿Por qué aparece 'error de procesamiento' al pagar?",
        "respuesta": "El error de procesamiento puede deberse a varios factores...",
        "categoria": "PAGOS",
        "relevancia_score": 0.88
      },
      "fragmentos_destacados": [
        "error de procesamiento al pagar",
        "problemas temporales con el sistema"
      ],
      "motivo_relevancia": "Problema similar relacionado con pagos"
    }
  ],
  "sugerencias_adicionales": [
    {
      "tipo": "ACCION",
      "titulo": "Crear ticket de soporte",
      "descripcion": "Si ninguna FAQ resuelve tu problema, crear un ticket personalizado",
      "url": "/soporte/tickets/crear?categoria=PAGOS&contexto=pago_tarjeta"
    },
    {
      "tipo": "CONTACTO",
      "titulo": "Chat con agente",
      "descripcion": "Habla directamente con un especialista en pagos",
      "disponible": true,
      "tiempo_espera": "2 minutos"
    }
  ],
  "estadisticas_busqueda": {
    "tiempo_respuesta": "0.145s",
    "total_faqs_analizadas": 245,
    "algoritmo_usado": "semantic_search_v2",
    "confianza_promedio": 0.91
  },
  "busquedas_relacionadas": [
    "problemas pago tarjeta",
    "error gateway pagos",
    "métodos pago alternativos",
    "contactar soporte pagos"
  ]
}
```

## 4. GESTIÓN DE CASOS

### 4.1 Crear Caso de Soporte

**Request:**
```json
POST /api/soporte/casos/
Content-Type: application/json
Authorization: Bearer <token>

{
  "tipo_caso": "RECLAMO",
  "urgencia": "ALTA",
  "titulo": "Servicio de catering deficiente en evento del 18/09",
  "descripcion": "El servicio de catering contratado para el evento del pasado 18 de septiembre no cumplió con las expectativas. La comida llegó fría, faltaron varios platos del menú acordado y el personal de servicio fue insuficiente para el número de invitados.",
  "cliente_afectado": 1,
  "reservas_relacionadas": [123, 124],
  "impacto_estimado": "ALTO",
  "servicios_afectados": [
    {
      "servicio_id": 5,
      "nombre": "Catering Premium",
      "problema_especifico": "Comida fría y platos faltantes"
    }
  ],
  "evidencias": [
    {
      "tipo": "FOTO",
      "descripcion": "Fotos de la comida fría",
      "archivo": "evidencia_catering_01.jpg"
    },
    {
      "tipo": "DOCUMENTO",
      "descripcion": "Contrato original del servicio",
      "archivo": "contrato_catering.pdf"
    }
  ],
  "compensacion_solicitada": {
    "tipo": "REEMBOLSO_PARCIAL",
    "monto": 800.00,
    "justificacion": "Reembolso del 50% del servicio de catering por incumplimiento"
  },
  "fecha_limite_resolucion": "2024-09-25T23:59:59Z"
}
```

**Response (201 Created):**
```json
{
  "id": 789,
  "numero_caso": "CS-2024-000789",
  "tipo_caso": "RECLAMO",
  "urgencia": "ALTA",
  "estado": "ABIERTO",
  "titulo": "Servicio de catering deficiente en evento del 18/09",
  "descripcion": "El servicio de catering contratado para el evento...",
  "fecha_creacion": "2024-09-20T18:00:00Z",
  "fecha_actualizacion": "2024-09-20T18:00:00Z",
  "fecha_limite_resolucion": "2024-09-25T23:59:59Z",
  "cliente_afectado": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan.perez@email.com",
    "telefono": "+591 70123456",
    "nivel_cliente": "PREMIUM",
    "historial_casos": {
      "total": 2,
      "resueltos": 1,
      "satisfaccion_promedio": 4.0
    }
  },
  "agente_asignado": {
    "id": 12,
    "nombre": "Ana García",
    "departamento": "Gestión de Casos",
    "especialidad": "Reclamos de Servicios",
    "email": "ana.garcia@gestion.com"
  },
  "supervisor": {
    "id": 15,
    "nombre": "Luis Mendoza",
    "departamento": "Gestión de Casos",
    "cargo": "Supervisor Senior"
  },
  "reservas_relacionadas": [
    {
      "id": 123,
      "numero": "RSV-2024-000123",
      "fecha_evento": "2024-09-18T18:00:00Z",
      "estado": "COMPLETADA",
      "total": 1500.00,
      "servicios": [
        {
          "id": 5,
          "nombre": "Catering Premium",
          "precio": 1200.00,
          "estado": "PROBLEMATICO"
        }
      ]
    },
    {
      "id": 124,
      "numero": "RSV-2024-000124",
      "fecha_evento": "2024-09-19T12:00:00Z",
      "estado": "COMPLETADA",
      "total": 800.00
    }
  ],
  "impacto_estimado": "ALTO",
  "prioridad_calculada": "CRITICA",
  "sla": {
    "primera_respuesta": "01:00:00",
    "resolucion": "72:00:00",
    "vencimiento_primera_respuesta": "2024-09-20T19:00:00Z",
    "vencimiento_resolucion": "2024-09-23T18:00:00Z"
  },
  "compensacion_solicitada": {
    "tipo": "REEMBOLSO_PARCIAL",
    "monto": 800.00,
    "moneda": "BOB",
    "justificacion": "Reembolso del 50% del servicio de catering por incumplimiento",
    "estado": "PENDIENTE_EVALUACION"
  },
  "evidencias": [
    {
      "id": 301,
      "tipo": "FOTO",
      "descripcion": "Fotos de la comida fría",
      "archivo": "evidencia_catering_01.jpg",
      "url": "https://api.domain.com/media/casos/789/evidencia_catering_01.jpg",
      "fecha_subida": "2024-09-20T18:00:00Z"
    },
    {
      "id": 302,
      "tipo": "DOCUMENTO",
      "descripcion": "Contrato original del servicio",
      "archivo": "contrato_catering.pdf",
      "url": "https://api.domain.com/media/casos/789/contrato_catering.pdf",
      "fecha_subida": "2024-09-20T18:00:00Z"
    }
  ],
  "timeline": [
    {
      "id": 1,
      "fecha": "2024-09-20T18:00:00Z",
      "evento": "CASO_CREADO",
      "descripcion": "Caso creado por el cliente",
      "autor": {
        "id": 1,
        "nombre": "Juan Pérez",
        "tipo": "CLIENTE"
      }
    },
    {
      "id": 2,
      "fecha": "2024-09-20T18:01:00Z",
      "evento": "ASIGNACION_AUTOMATICA",
      "descripcion": "Caso asignado automáticamente a Ana García",
      "autor": {
        "id": 0,
        "nombre": "Sistema",
        "tipo": "SISTEMA"
      },
      "metadatos": {
        "regla_asignacion": "Especialista en reclamos de servicios",
        "score_compatibilidad": 0.95
      }
    }
  ],
  "alertas_activas": [
    {
      "tipo": "SLA_WARNING",
      "mensaje": "Caso de alta urgencia - Requiere primera respuesta en 59 minutos",
      "nivel": "WARNING",
      "vencimiento": "2024-09-20T19:00:00Z"
    },
    {
      "tipo": "ESCALATION_RULE",
      "mensaje": "Cliente PREMIUM - Aplicar protocolo de atención prioritaria",
      "nivel": "INFO",
      "accion_requerida": "Contacto directo en 30 minutos"
    }
  ],
  "acciones_automaticas": [
    "Notificación enviada al agente asignado",
    "Email de confirmación enviado al cliente",
    "Alerta creada para supervisor",
    "Investigación de proveedores iniciada"
  ],
  "proximo_paso": {
    "accion": "PRIMERA_RESPUESTA",
    "responsable": "Ana García",
    "fecha_limite": "2024-09-20T19:00:00Z",
    "descripcion": "Contactar al cliente para confirmar recepción del caso y solicitar información adicional"
  }
}
```

### 4.2 Actualizar Estado de Caso

**Request:**
```json
PATCH /api/soporte/casos/789/
Content-Type: application/json
Authorization: Bearer <token>

{
  "estado": "EN_INVESTIGACION",
  "nota_actualizacion": "Iniciando investigación con el proveedor de catering. Se ha contactado con el responsable del servicio para obtener su versión de los hechos.",
  "acciones_realizadas": [
    "Contacto con proveedor de catering",
    "Revisión de contrato de servicios",
    "Análisis de evidencias fotográficas"
  ],
  "siguiente_paso": {
    "accion": "REUNION_PROVEEDOR",
    "fecha_programada": "2024-09-21T10:00:00Z",
    "responsable": "Ana García",
    "descripcion": "Reunión con representante del proveedor para discutir los problemas reportados"
  },
  "tiempo_estimado_resolucion": "48:00:00"
}
```

**Response (200 OK):**
```json
{
  "id": 789,
  "numero_caso": "CS-2024-000789",
  "estado": "EN_INVESTIGACION",
  "fecha_actualizacion": "2024-09-20T19:30:00Z",
  "tiempo_primera_respuesta": "01:30:00",
  "sla_primera_respuesta": {
    "objetivo": "01:00:00",
    "actual": "01:30:00",
    "estado": "INCUMPLIDO",
    "porcentaje": 150
  },
  "nota_actualizacion": "Iniciando investigación con el proveedor de catering...",
  "acciones_realizadas": [
    "Contacto con proveedor de catering",
    "Revisión de contrato de servicios",
    "Análisis de evidencias fotográficas"
  ],
  "siguiente_paso": {
    "accion": "REUNION_PROVEEDOR",
    "fecha_programada": "2024-09-21T10:00:00Z",
    "responsable": "Ana García",
    "descripcion": "Reunión con representante del proveedor para discutir los problemas reportados"
  },
  "tiempo_estimado_resolucion": "48:00:00",
  "timeline_actualizado": [
    {
      "id": 3,
      "fecha": "2024-09-20T19:30:00Z",
      "evento": "ESTADO_ACTUALIZADO",
      "descripcion": "Estado cambiado a EN_INVESTIGACION",
      "autor": {
        "id": 12,
        "nombre": "Ana García",
        "tipo": "AGENTE"
      },
      "detalles": {
        "estado_anterior": "ABIERTO",
        "estado_nuevo": "EN_INVESTIGACION",
        "nota": "Iniciando investigación con el proveedor de catering..."
      }
    }
  ],
  "notificaciones_enviadas": [
    {
      "destinatario": "juan.perez@email.com",
      "tipo": "EMAIL",
      "asunto": "Actualización de su caso CS-2024-000789",
      "estado": "ENVIADO"
    },
    {
      "destinatario": "Luis Mendoza",
      "tipo": "INTERNAL_NOTIFICATION",
      "asunto": "Caso en investigación - Primera respuesta tardía",
      "estado": "ENVIADO"
    }
  ]
}
```

## 5. ESCALAMIENTO AUTOMÁTICO

### 5.1 Configurar Reglas de Escalamiento

**Request:**
```json
POST /api/soporte/escalamiento/reglas/
Content-Type: application/json
Authorization: Bearer <token>

{
  "nombre": "Escalamiento Cliente Premium",
  "descripcion": "Reglas especiales para clientes premium",
  "activa": true,
  "condiciones": [
    {
      "campo": "cliente.nivel",
      "operador": "EQUALS",
      "valor": "PREMIUM"
    },
    {
      "campo": "urgencia",
      "operador": "IN",
      "valor": ["ALTA", "CRITICA"]
    },
    {
      "campo": "tiempo_sin_respuesta",
      "operador": "GREATER_THAN",
      "valor": "00:30:00"
    }
  ],
  "acciones": [
    {
      "tipo": "ESCALAR_NIVEL",
      "parametros": {
        "nivel_destino": 2,
        "mantener_agente": false,
        "notificar_supervisor": true
      }
    },
    {
      "tipo": "NOTIFICAR_URGENTE",
      "parametros": {
        "destinatarios": ["supervisor@empresa.com", "manager@empresa.com"],
        "canal": "EMAIL_SMS",
        "template": "escalamiento_premium"
      }
    },
    {
      "tipo": "ACTUALIZAR_SLA",
      "parametros": {
        "nueva_prioridad": "CRITICA",
        "reducir_tiempo_resolucion": "50%"
      }
    }
  ],
  "horario_activacion": {
    "dias_semana": ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"],
    "hora_inicio": "08:00:00",
    "hora_fin": "18:00:00",
    "zona_horaria": "America/La_Paz"
  },
  "frecuencia_evaluacion": "00:05:00",
  "prioridad": 1
}
```

**Response (201 Created):**
```json
{
  "id": 101,
  "nombre": "Escalamiento Cliente Premium",
  "descripcion": "Reglas especiales para clientes premium",
  "activa": true,
  "fecha_creacion": "2024-09-20T20:00:00Z",
  "fecha_ultima_ejecucion": null,
  "estadisticas": {
    "ejecuciones_totales": 0,
    "tickets_escalados": 0,
    "casos_escalados": 0,
    "efectividad": null
  },
  "condiciones": [
    {
      "campo": "cliente.nivel",
      "operador": "EQUALS",
      "valor": "PREMIUM",
      "descripcion_humana": "Cliente es nivel PREMIUM"
    },
    {
      "campo": "urgencia",
      "operador": "IN",
      "valor": ["ALTA", "CRITICA"],
      "descripcion_humana": "Urgencia es ALTA o CRITICA"
    },
    {
      "campo": "tiempo_sin_respuesta",
      "operador": "GREATER_THAN",
      "valor": "00:30:00",
      "descripcion_humana": "Más de 30 minutos sin respuesta"
    }
  ],
  "acciones": [
    {
      "tipo": "ESCALAR_NIVEL",
      "parametros": {
        "nivel_destino": 2,
        "mantener_agente": false,
        "notificar_supervisor": true
      },
      "descripcion_humana": "Escalar a nivel 2 con notificación a supervisor"
    },
    {
      "tipo": "NOTIFICAR_URGENTE",
      "parametros": {
        "destinatarios": ["supervisor@empresa.com", "manager@empresa.com"],
        "canal": "EMAIL_SMS",
        "template": "escalamiento_premium"
      },
      "descripcion_humana": "Enviar notificación urgente por email y SMS"
    },
    {
      "tipo": "ACTUALIZAR_SLA",
      "parametros": {
        "nueva_prioridad": "CRITICA",
        "reducir_tiempo_resolucion": "50%"
      },
      "descripcion_humana": "Actualizar SLA a crítico y reducir tiempo de resolución 50%"
    }
  ],
  "configuracion_validada": true,
  "proxima_evaluacion": "2024-09-20T20:05:00Z"
}
```

### 5.2 Monitor de Escalamiento en Tiempo Real

**Request:**
```json
GET /api/soporte/escalamiento/monitor/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "resumen": {
    "escalamientos_activos": 5,
    "reglas_activas": 12,
    "tickets_en_riesgo": 8,
    "casos_criticos": 3,
    "ultima_actualizacion": "2024-09-20T20:30:00Z"
  },
  "escalamientos_recientes": [
    {
      "id": 501,
      "tipo": "TICKET",
      "item_id": 456,
      "numero": "TK-2024-000456",
      "titulo": "Problema con el pago de mi reserva",
      "nivel_anterior": 1,
      "nivel_actual": 2,
      "fecha_escalamiento": "2024-09-20T19:45:00Z",
      "regla_aplicada": "Escalamiento Cliente Premium",
      "motivo": "Cliente PREMIUM con más de 30 minutos sin respuesta",
      "agente_anterior": {
        "id": 5,
        "nombre": "María Rodríguez"
      },
      "agente_actual": {
        "id": 8,
        "nombre": "Carlos López",
        "nivel": 2
      },
      "tiempo_en_nivel_anterior": "01:15:00",
      "acciones_ejecutadas": [
        "Escalamiento a nivel 2",
        "Notificación urgente enviada",
        "SLA actualizado a crítico"
      ],
      "estado_actual": "EN_PROGRESO",
      "sla_actualizado": {
        "tiempo_resolucion_anterior": "24:00:00",
        "tiempo_resolucion_actual": "12:00:00",
        "vencimiento": "2024-09-21T08:00:00Z"
      }
    },
    {
      "id": 502,
      "tipo": "CASO",
      "item_id": 789,
      "numero": "CS-2024-000789",
      "titulo": "Servicio de catering deficiente en evento del 18/09",
      "nivel_anterior": 1,
      "nivel_actual": 3,
      "fecha_escalamiento": "2024-09-20T20:15:00Z",
      "regla_aplicada": "Escalamiento Casos Críticos",
      "motivo": "Caso de reclamo con compensación > $500 y SLA vencido",
      "agente_anterior": {
        "id": 12,
        "nombre": "Ana García"
      },
      "supervisor_asignado": {
        "id": 15,
        "nombre": "Luis Mendoza",
        "cargo": "Supervisor Senior"
      },
      "tiempo_en_nivel_anterior": "02:15:00",
      "acciones_ejecutadas": [
        "Escalamiento a supervisor senior",
        "Alerta crítica enviada",
        "Reunión urgente programada"
      ],
      "estado_actual": "ESCALADO_CRITICO",
      "compensacion_involucrada": {
        "monto": 800.00,
        "moneda": "BOB"
      }
    }
  ],
  "alertas_activas": [
    {
      "id": "alert_001",
      "tipo": "SLA_VENCIMIENTO_PROXIMO",
      "nivel": "WARNING",
      "mensaje": "3 tickets vencen SLA en los próximos 30 minutos",
      "tickets_afectados": [457, 458, 459],
      "tiempo_restante": "00:25:00",
      "accion_sugerida": "Revisar asignaciones y priorizar atención"
    },
    {
      "id": "alert_002",
      "tipo": "COLA_SATURADA",
      "nivel": "ERROR",
      "mensaje": "Cola de nivel 1 tiene 15 tickets pendientes (máximo recomendado: 10)",
      "cola_afectada": "Soporte Nivel 1",
      "tickets_en_cola": 15,
      "tiempo_espera_promedio": "02:30:00",
      "accion_sugerida": "Asignar agentes adicionales o redistribuir carga"
    },
    {
      "id": "alert_003",
      "tipo": "REGLA_ESCALAMIENTO_FALLIDA",
      "nivel": "ERROR",
      "mensaje": "Regla 'Escalamiento Nocturno' falló por falta de agentes disponibles",
      "regla_afectada": "Escalamiento Nocturno",
      "tickets_afectados": [460],
      "error": "No hay agentes de nivel 2 disponibles en horario nocturno",
      "accion_sugerida": "Configurar agente de guardia o ajustar regla"
    }
  ],
  "metricas_tiempo_real": {
    "tiempo_promedio_primera_respuesta": "01:25:00",
    "tiempo_promedio_resolucion": "18:30:00",
    "escalamientos_por_hora": 2.5,
    "tasa_escalamiento": "12%",
    "satisfaccion_post_escalamiento": 4.2,
    "sla_cumplimiento": {
      "primera_respuesta": "87%",
      "resolucion": "92%"
    }
  },
  "predicciones": [
    {
      "tipo": "ESCALAMIENTO_PREDICHO",
      "ticket_id": 461,
      "probabilidad": 0.78,
      "tiempo_estimado": "00:15:00",
      "razon": "Cliente VIP sin respuesta por 45 minutos en horario laboral"
    },
    {
      "tipo": "SLA_RIESGO",
      "items_afectados": 6,
      "probabilidad": 0.65,
      "tiempo_estimado": "01:30:00",
      "razon": "Carga de trabajo actual y tiempo promedio de resolución"
    }
  ],
  "recomendaciones": [
    {
      "tipo": "OPTIMIZACION_REGLAS",
      "descripcion": "La regla 'Escalamiento Cliente Premium' está escalando el 23% de los tickets VIP. Considerar ajustar el tiempo de espera de 30 a 45 minutos.",
      "impacto_estimado": "Reducción del 35% en escalamientos innecesarios",
      "prioridad": "MEDIA"
    },
    {
      "tipo": "REDISTRIBUCION_CARGA",
      "descripcion": "El agente María Rodríguez tiene 8 tickets activos (máximo recomendado: 5). Considerar redistribuir 3 tickets.",
      "impacto_estimado": "Mejora del 20% en tiempo de respuesta",
      "prioridad": "ALTA"
    }
  ]
}
```

Esta documentación proporciona ejemplos completos de todos los payloads del sistema de soporte, desde la creación básica de tickets hasta el monitoreo avanzado de escalamiento automático, incluyendo todas las estructuras de datos y respuestas que el frontend necesitará para una integración completa.