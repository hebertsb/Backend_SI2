# PAYLOADS NOTIFICACIONES - Estructuras de Datos Completas

## Introducción

Este documento detalla todos los payloads necesarios para el sistema de notificaciones, incluyendo diferentes tipos de notificaciones, canales de envío y estructuras de datos para cada escenario específico del sistema de reservas.

## 1. ESTRUCTURA BASE DE NOTIFICACIÓN

### Modelo Principal
```json
{
  "id": "integer - ID único de la notificación",
  "usuario_id": "integer - ID del usuario destinatario",
  "tipo_notificacion": "string - Tipo específico de notificación",
  "canal": "string - Canal de envío (email, sms, push, in_app)",
  "titulo": "string - Título de la notificación",
  "mensaje": "text - Contenido principal del mensaje",
  "datos_adicionales": "json - Datos contextuales específicos",
  "plantilla_id": "integer - ID de plantilla utilizada (opcional)",
  "estado": "string - Estado actual (pendiente, enviada, entregada, fallida, leida)",
  "prioridad": "string - Nivel de prioridad (baja, normal, alta, urgente)",
  "programada_para": "datetime - Fecha/hora programada para envío",
  "enviada_en": "datetime - Timestamp de envío real",
  "entregada_en": "datetime - Timestamp de entrega confirmada",
  "leida_en": "datetime - Timestamp de lectura por usuario",
  "intentos_envio": "integer - Número de intentos realizados",
  "ultimo_error": "text - Descripción del último error",
  "metadatos": "json - Metadatos del proveedor de envío",
  "expira_en": "datetime - Fecha de expiración (opcional)",
  "accion_requerida": "boolean - Si requiere acción del usuario",
  "url_accion": "string - URL para acción específica",
  "created_at": "datetime - Fecha de creación",
  "updated_at": "datetime - Fecha de última actualización"
}
```

## 2. NOTIFICACIONES DE RESERVAS

### 2.1 Confirmación de Reserva

#### Payload para Crear Notificación
```json
{
  "usuario_id": 123,
  "tipo_notificacion": "reserva_confirmada",
  "canal": "email",
  "titulo": "Reserva Confirmada - {{hotel_nombre}}",
  "mensaje": "Su reserva ha sido confirmada exitosamente",
  "prioridad": "normal",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "hotel_nombre": "Hotel Paradise Resort",
    "hotel_direccion": "Av. Principal 123, Santa Cruz",
    "hotel_telefono": "+591-3-1234567",
    "fecha_checkin": "2024-03-15",
    "fecha_checkout": "2024-03-18",
    "hora_checkin": "15:00",
    "hora_checkout": "12:00",
    "numero_huespedes": 2,
    "tipo_habitacion": "Suite Deluxe",
    "monto_total": 1850.00,
    "moneda": "BOB",
    "metodo_pago": "Tarjeta de Crédito",
    "servicios_incluidos": [
      "Desayuno buffet",
      "Wi-Fi gratuito",
      "Piscina",
      "Gimnasio"
    ],
    "politicas_cancelacion": "Cancelación gratuita hasta 24 horas antes",
    "instrucciones_especiales": "Solicitar habitación en piso alto",
    "codigo_qr_checkin": "data:image/png;base64,iVBORw0KGgoAAAANSU...",
    "enlace_gestion": "https://reservas.com/gestion/CNF789123"
  },
  "accion_requerida": false,
  "plantilla_id": 1,
  "enviar_inmediatamente": true
}
```

#### Payload de Respuesta
```json
{
  "id": 789,
  "usuario_id": 123,
  "tipo_notificacion": "reserva_confirmada",
  "canal": "email",
  "titulo": "Reserva Confirmada - Hotel Paradise Resort",
  "estado": "enviada",
  "prioridad": "normal",
  "enviada_en": "2024-01-15T10:30:00Z",
  "metadatos": {
    "proveedor": "sendgrid",
    "message_id": "abc123def456",
    "template_version": "v2.1"
  },
  "created_at": "2024-01-15T10:29:55Z"
}
```

### 2.2 Recordatorio de Check-in

#### Payload Email
```json
{
  "usuario_id": 123,
  "tipo_notificacion": "recordatorio_checkin",
  "canal": "email",
  "titulo": "Recordatorio: Check-in mañana en {{hotel_nombre}}",
  "mensaje": "Su check-in es mañana. Prepare su documentación.",
  "prioridad": "alta",
  "programada_para": "2024-03-14T12:00:00Z",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "hotel_nombre": "Hotel Paradise Resort",
    "fecha_checkin": "2024-03-15",
    "hora_checkin": "15:00",
    "direccion_hotel": "Av. Principal 123, Santa Cruz",
    "telefono_hotel": "+591-3-1234567",
    "documentos_requeridos": [
      "Cédula de identidad o pasaporte",
      "Comprobante de reserva",
      "Tarjeta de crédito para garantía"
    ],
    "instrucciones_llegada": "Presentarse en recepción con 30 minutos de anticipación",
    "mapa_ubicacion": "https://maps.google.com/...",
    "condiciones_climaticas": {
      "temperatura": "28°C",
      "condicion": "Soleado",
      "recomendacion": "Ropa ligera y protector solar"
    }
  },
  "accion_requerida": false,
  "plantilla_id": 3
}
```

#### Payload SMS
```json
{
  "usuario_id": 123,
  "tipo_notificacion": "recordatorio_checkin",
  "canal": "sms",
  "titulo": "Recordatorio Check-in",
  "mensaje": "{{nombre_cliente}}, su check-in en {{hotel_nombre}} es mañana {{fecha_checkin}} a las {{hora_checkin}}. Confirmación: {{numero_confirmacion}}",
  "prioridad": "alta",
  "programada_para": "2024-03-14T18:00:00Z",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "nombre_cliente": "Juan Pérez",
    "hotel_nombre": "Hotel Paradise",
    "fecha_checkin": "15/03/2024",
    "hora_checkin": "15:00",
    "enlace_corto": "https://bit.ly/reserva789"
  },
  "plantilla_id": 4
}
```

### 2.3 Cancelación de Reserva

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "reserva_cancelada",
  "canal": "email",
  "titulo": "Reserva Cancelada - Reembolso Procesado",
  "mensaje": "Su reserva ha sido cancelada y el reembolso está siendo procesado",
  "prioridad": "alta",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "hotel_nombre": "Hotel Paradise Resort",
    "fecha_cancelacion": "2024-01-15T14:30:00Z",
    "motivo_cancelacion": "Solicitud del cliente",
    "fecha_checkin_original": "2024-03-15",
    "monto_original": 1850.00,
    "monto_reembolso": 1665.00,
    "descuentos_aplicados": [
      {
        "concepto": "Penalización por cancelación",
        "monto": 185.00,
        "porcentaje": 10
      }
    ],
    "metodo_reembolso": "Tarjeta de crédito terminada en 4532",
    "tiempo_estimado_reembolso": "3-5 días hábiles",
    "numero_transaccion": "REF987654321",
    "soporte_contacto": {
      "telefono": "+591-3-1234567",
      "email": "soporte@reservas.com",
      "horario": "Lunes a Viernes 8:00-18:00"
    }
  },
  "accion_requerida": false,
  "plantilla_id": 5
}
```

## 3. NOTIFICACIONES DE REPROGRAMACIÓN

### 3.1 Solicitud de Reprogramación Enviada

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "reprogramacion_solicitada",
  "canal": "in_app",
  "titulo": "Solicitud de Reprogramación Enviada",
  "mensaje": "Su solicitud de reprogramación está siendo revisada",
  "prioridad": "normal",
  "datos_adicionales": {
    "reserva_id": 456,
    "solicitud_id": 789,
    "numero_confirmacion": "CNF789123",
    "hotel_nombre": "Hotel Paradise Resort",
    "fecha_original": "2024-03-15",
    "fecha_nueva_solicitada": "2024-03-22",
    "motivo_reprogramacion": "Cambio en itinerario de trabajo",
    "fecha_solicitud": "2024-01-15T10:30:00Z",
    "tiempo_estimado_respuesta": "24-48 horas",
    "costo_reprogramacion": 150.00,
    "reglas_aplicadas": [
      {
        "regla": "Tiempo mínimo 24 horas",
        "estado": "cumplida",
        "descripcion": "Solicitud realizada con 68 días de anticipación"
      },
      {
        "regla": "Máximo 3 reprogramaciones",
        "estado": "cumplida",
        "descripcion": "Esta es la primera reprogramación"
      },
      {
        "regla": "Disponibilidad de fechas",
        "estado": "pendiente",
        "descripcion": "Verificando disponibilidad para la nueva fecha"
      }
    ],
    "estado_solicitud": "en_revision",
    "enlace_seguimiento": "https://reservas.com/reprogramacion/789"
  },
  "accion_requerida": false,
  "url_accion": "https://reservas.com/reprogramacion/789",
  "plantilla_id": 6
}
```

### 3.2 Reprogramación Aprobada

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "reprogramacion_aprobada",
  "canal": "email",
  "titulo": "¡Reprogramación Aprobada! Nueva fecha confirmada",
  "mensaje": "Su solicitud de reprogramación ha sido aprobada",
  "prioridad": "alta",
  "datos_adicionales": {
    "reserva_id": 456,
    "solicitud_id": 789,
    "numero_confirmacion": "CNF789123",
    "nuevo_numero_confirmacion": "CNF789124",
    "hotel_nombre": "Hotel Paradise Resort",
    "fecha_original": "2024-03-15",
    "fecha_nueva": "2024-03-22",
    "hora_checkin": "15:00",
    "hora_checkout": "12:00",
    "fecha_aprobacion": "2024-01-16T09:15:00Z",
    "costo_reprogramacion": 150.00,
    "monto_total_actualizado": 2000.00,
    "diferencia_tarifaria": 0.00,
    "metodo_pago_cargo": "Tarjeta terminada en 4532",
    "resumen_cambios": {
      "fecha_checkin": {
        "anterior": "2024-03-15",
        "nueva": "2024-03-22"
      },
      "fecha_checkout": {
        "anterior": "2024-03-18", 
        "nueva": "2024-03-25"
      },
      "noches": {
        "anterior": 3,
        "nueva": 3
      }
    },
    "nueva_politica_cancelacion": "Cancelación gratuita hasta 24 horas antes de la nueva fecha",
    "instrucciones_adicionales": "Por favor guarde este nuevo número de confirmación"
  },
  "accion_requerida": false,
  "plantilla_id": 7
}
```

### 3.3 Reprogramación Rechazada

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "reprogramacion_rechazada",
  "canal": "email",
  "titulo": "Solicitud de Reprogramación No Aprobada",
  "mensaje": "Lamentamos informar que su solicitud no pudo ser procesada",
  "prioridad": "alta",
  "datos_adicionales": {
    "reserva_id": 456,
    "solicitud_id": 789,
    "numero_confirmacion": "CNF789123",
    "hotel_nombre": "Hotel Paradise Resort",
    "fecha_solicitada": "2024-03-22",
    "fecha_rechazo": "2024-01-16T14:20:00Z",
    "motivos_rechazo": [
      {
        "codigo": "NO_DISPONIBILIDAD",
        "descripcion": "No hay disponibilidad en las fechas solicitadas",
        "detalle": "El hotel está completamente reservado para esas fechas"
      },
      {
        "codigo": "TARIFA_DIFERENCIAL",
        "descripcion": "Diferencia tarifaria significativa",
        "detalle": "La nueva fecha requiere un pago adicional de $500"
      }
    ],
    "alternativas_sugeridas": [
      {
        "fecha_checkin": "2024-03-20",
        "fecha_checkout": "2024-03-23",
        "diferencia_costo": 75.00,
        "disponibilidad": "Confirmar en 24 horas"
      },
      {
        "fecha_checkin": "2024-03-25",
        "fecha_checkout": "2024-03-28", 
        "diferencia_costo": 0.00,
        "disponibilidad": "Disponible inmediatamente"
      }
    ],
    "opciones_cliente": [
      "Mantener reserva original",
      "Elegir fecha alternativa",
      "Cancelar reserva (aplican políticas de cancelación)"
    ],
    "fecha_limite_decision": "2024-01-20T23:59:59Z",
    "contacto_soporte": {
      "telefono": "+591-3-1234567",
      "email": "soporte@reservas.com",
      "chat_online": "https://reservas.com/chat"
    }
  },
  "accion_requerida": true,
  "url_accion": "https://reservas.com/reprogramacion/789/alternativas",
  "expira_en": "2024-01-20T23:59:59Z",
  "plantilla_id": 8
}
```

## 4. NOTIFICACIONES PROMOCIONALES

### 4.1 Oferta Personalizada

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "promocion_personalizada",
  "canal": "email",
  "titulo": "¡Oferta Exclusiva Solo Para Ti! 40% de Descuento",
  "mensaje": "Oferta especial basada en tus preferencias de viaje",
  "prioridad": "normal",
  "datos_adicionales": {
    "codigo_promocion": "EXCLUSIVO40",
    "descuento_porcentaje": 40,
    "descuento_maximo": 800.00,
    "fecha_inicio": "2024-01-15",
    "fecha_vencimiento": "2024-02-15",
    "condiciones": [
      "Válido para reservas de mínimo 3 noches",
      "Aplicable en hoteles seleccionados",
      "No acumulable con otras promociones",
      "Sujeto a disponibilidad"
    ],
    "hoteles_incluidos": [
      {
        "id": 101,
        "nombre": "Hotel Paradise Resort",
        "ubicacion": "Santa Cruz",
        "categoria": 5,
        "precio_base": 450.00,
        "precio_con_descuento": 270.00,
        "imagen": "https://images.reservas.com/hotel_101.jpg"
      },
      {
        "id": 102,
        "nombre": "Grand Plaza Hotel",
        "ubicacion": "La Paz",
        "categoria": 4,
        "precio_base": 350.00,
        "precio_con_descuento": 210.00,
        "imagen": "https://images.reservas.com/hotel_102.jpg"
      }
    ],
    "criterios_personalizacion": {
      "ubicacion_preferida": "Santa Cruz",
      "categoria_favorita": 5,
      "rango_precio": "premium",
      "ultima_reserva": "2023-11-15",
      "frecuencia_reservas": "cliente_frecuente"
    },
    "estadisticas_ahorro": {
      "ahorro_promedio": 320.00,
      "noches_recomendadas": 4,
      "ahorro_total_estimado": 1280.00
    },
    "llamada_accion": "Reserva ahora y ahorra hasta $800",
    "enlace_reserva": "https://reservas.com/promocion/EXCLUSIVO40"
  },
  "accion_requerida": false,
  "url_accion": "https://reservas.com/promocion/EXCLUSIVO40",
  "expira_en": "2024-02-15T23:59:59Z",
  "plantilla_id": 10
}
```

### 4.2 Flash Sale

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "flash_sale",
  "canal": "push",
  "titulo": "⚡ FLASH SALE: 60% OFF - Solo 2 horas!",
  "mensaje": "Descuentos increíbles por tiempo limitado",
  "prioridad": "urgente",
  "datos_adicionales": {
    "codigo_promocion": "FLASH60",
    "descuento_porcentaje": 60,
    "tiempo_restante": "01:45:32",
    "fecha_fin": "2024-01-15T23:59:59Z",
    "inventario_limitado": true,
    "habitaciones_disponibles": 15,
    "hoteles_flash": [
      {
        "id": 103,
        "nombre": "Resort Tropical",
        "ubicacion": "Tarija",
        "precio_original": 500.00,
        "precio_flash": 200.00,
        "habitaciones_restantes": 5,
        "imagen": "https://images.reservas.com/hotel_103.jpg"
      }
    ],
    "condiciones_especiales": [
      "Válido solo por 2 horas",
      "Máximo 2 habitaciones por cliente",
      "Pago inmediato requerido",
      "No reembolsable"
    ],
    "contador_regresivo": {
      "horas": 1,
      "minutos": 45,
      "segundos": 32
    },
    "urgencia_mensaje": "¡Solo quedan 15 habitaciones disponibles!",
    "testimonio_cliente": {
      "nombre": "María G.",
      "comentario": "¡Increíble resort! La mejor oferta que he encontrado",
      "calificacion": 5
    }
  },
  "accion_requerida": true,
  "url_accion": "https://reservas.com/flash/FLASH60",
  "expira_en": "2024-01-15T23:59:59Z",
  "plantilla_id": 11
}
```

## 5. NOTIFICACIONES DE SISTEMA

### 5.1 Mantenimiento Programado

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "mantenimiento_sistema",
  "canal": "in_app",
  "titulo": "Mantenimiento Programado del Sistema",
  "mensaje": "El sistema estará en mantenimiento por mejoras",
  "prioridad": "normal",
  "datos_adicionales": {
    "fecha_inicio": "2024-01-20T02:00:00Z",
    "fecha_fin": "2024-01-20T04:00:00Z",
    "duracion_estimada": "2 horas",
    "zona_horaria": "America/La_Paz",
    "servicios_afectados": [
      "Nuevas reservas",
      "Modificaciones de reservas",
      "Pagos online"
    ],
    "servicios_disponibles": [
      "Consulta de reservas existentes",
      "Información de contacto",
      "FAQs"
    ],
    "motivo_mantenimiento": "Actualización de seguridad y mejoras de rendimiento",
    "mejoras_incluidas": [
      "Mayor velocidad de carga",
      "Nueva funcionalidad de filtros",
      "Seguridad reforzada",
      "Interfaz mejorada"
    ],
    "contacto_emergencia": {
      "telefono": "+591-3-1234567",
      "disponible": "24/7 para emergencias únicamente"
    },
    "fecha_notificacion_previa": "2024-01-18T10:00:00Z"
  },
  "accion_requerida": false,
  "plantilla_id": 15
}
```

### 5.2 Actualización de Términos y Condiciones

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "actualizacion_terminos",
  "canal": "email",
  "titulo": "Actualización de Términos y Condiciones",
  "mensaje": "Hemos actualizado nuestros términos de servicio",
  "prioridad": "normal",
  "datos_adicionales": {
    "fecha_vigencia": "2024-02-01T00:00:00Z",
    "version_actual": "3.1",
    "version_nueva": "3.2",
    "cambios_principales": [
      {
        "seccion": "Política de Cancelación",
        "cambio": "Ampliación del período de cancelación gratuita",
        "detalle": "De 24 a 48 horas antes del check-in"
      },
      {
        "seccion": "Protección de Datos",
        "cambio": "Nuevas medidas de seguridad",
        "detalle": "Implementación de cifrado avanzado"
      },
      {
        "seccion": "Política de Reembolsos",
        "cambio": "Proceso simplificado",
        "detalle": "Reembolsos automáticos en casos aplicables"
      }
    ],
    "impacto_usuario": "Estos cambios mejoran sus derechos como cliente",
    "accion_requerida_usuario": false,
    "enlace_terminos_completos": "https://reservas.com/terminos-v3.2",
    "enlace_comparacion": "https://reservas.com/terminos/comparacion/v3.1-v3.2",
    "contacto_legal": {
      "email": "legal@reservas.com",
      "telefono": "+591-3-1234567"
    },
    "fecha_envio_notificacion": "2024-01-15T10:00:00Z"
  },
  "accion_requerida": false,
  "url_accion": "https://reservas.com/terminos-v3.2",
  "plantilla_id": 16
}
```

## 6. NOTIFICACIONES DE PAGOS

### 6.1 Pago Confirmado

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "pago_confirmado",
  "canal": "email",
  "titulo": "Pago Procesado Exitosamente",
  "mensaje": "Su pago ha sido procesado y confirmado",
  "prioridad": "normal",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "transaccion_id": "TXN987654321",
    "monto_pagado": 1850.00,
    "moneda": "BOB",
    "metodo_pago": "Tarjeta de Crédito",
    "tarjeta_terminacion": "4532",
    "fecha_transaccion": "2024-01-15T10:30:00Z",
    "codigo_autorizacion": "AUTH123456",
    "estado_pago": "aprobado",
    "desglose_pago": {
      "subtotal": 1500.00,
      "impuestos": 195.00,
      "servicios": 100.00,
      "descuentos": -45.00,
      "total": 1850.00
    },
    "conceptos_pagados": [
      {
        "descripcion": "Alojamiento 3 noches",
        "cantidad": 3,
        "precio_unitario": 500.00,
        "subtotal": 1500.00
      },
      {
        "descripcion": "Desayuno incluido",
        "cantidad": 3,
        "precio_unitario": 0.00,
        "subtotal": 0.00,
        "nota": "Incluido en tarifa"
      }
    ],
    "politica_reembolso": "Reembolso disponible hasta 24 horas antes del check-in",
    "factura_electronica": {
      "numero": "FACT-2024-001234",
      "enlace_descarga": "https://reservas.com/facturas/FACT-2024-001234.pdf"
    },
    "siguiente_paso": "Recibirá confirmación del hotel en las próximas 2 horas"
  },
  "accion_requerida": false,
  "plantilla_id": 20
}
```

### 6.2 Pago Rechazado

```json
{
  "usuario_id": 123,
  "tipo_notificacion": "pago_rechazado",
  "canal": "email",
  "titulo": "Problema con el Pago - Acción Requerida",
  "mensaje": "Su pago no pudo ser procesado",
  "prioridad": "urgente",
  "datos_adicionales": {
    "reserva_id": 456,
    "numero_confirmacion": "CNF789123",
    "transaccion_id": "TXN987654322",
    "monto_intentado": 1850.00,
    "moneda": "BOB",
    "metodo_pago": "Tarjeta de Crédito",
    "tarjeta_terminacion": "4532",
    "fecha_intento": "2024-01-15T10:30:00Z",
    "motivo_rechazo": {
      "codigo": "INSUFFICIENT_FUNDS",
      "descripcion": "Fondos insuficientes",
      "detalle_banco": "Su banco ha rechazado la transacción por fondos insuficientes"
    },
    "acciones_sugeridas": [
      {
        "accion": "Verificar saldo",
        "descripcion": "Confirme que tiene fondos suficientes en su cuenta"
      },
      {
        "accion": "Contactar banco",
        "descripcion": "Su banco puede haber bloqueado la transacción por seguridad"
      },
      {
        "accion": "Usar otra tarjeta",
        "descripcion": "Intente con un método de pago diferente"
      }
    ],
    "tiempo_limite": "2024-01-16T10:30:00Z",
    "consecuencias_no_pago": "La reserva será cancelada automáticamente si no se completa el pago",
    "intentos_restantes": 2,
    "metodos_alternativos": [
      "Transferencia bancaria",
      "Pago en efectivo en oficinas",
      "Otra tarjeta de crédito"
    ],
    "soporte_pagos": {
      "telefono": "+591-3-1234567",
      "email": "pagos@reservas.com",
      "horario": "24/7"
    }
  },
  "accion_requerida": true,
  "url_accion": "https://reservas.com/pago/reintentar/CNF789123",
  "expira_en": "2024-01-16T10:30:00Z",
  "plantilla_id": 21
}
```

## 7. CONFIGURACIÓN DE PLANTILLAS

### 7.1 Variables Disponibles por Tipo

```json
{
  "reserva_confirmada": [
    "nombre_cliente",
    "numero_confirmacion", 
    "hotel_nombre",
    "hotel_direccion",
    "fecha_checkin",
    "fecha_checkout",
    "hora_checkin",
    "hora_checkout",
    "tipo_habitacion",
    "numero_huespedes",
    "monto_total",
    "servicios_incluidos",
    "politicas_cancelacion"
  ],
  "recordatorio_checkin": [
    "nombre_cliente",
    "hotel_nombre",
    "fecha_checkin",
    "hora_checkin",
    "numero_confirmacion",
    "direccion_hotel",
    "telefono_hotel",
    "documentos_requeridos"
  ],
  "reprogramacion_aprobada": [
    "nombre_cliente",
    "hotel_nombre",
    "fecha_original",
    "fecha_nueva",
    "nuevo_numero_confirmacion",
    "costo_reprogramacion",
    "diferencia_tarifaria"
  ],
  "promocion_personalizada": [
    "nombre_cliente",
    "codigo_promocion",
    "descuento_porcentaje",
    "fecha_vencimiento",
    "hoteles_incluidos",
    "ahorro_estimado"
  ]
}
```

### 7.2 Ejemplo de Plantilla HTML

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{asunto}}</title>
    <style>
        .container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background-color: #1890ff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f5f5f5; }
        .footer { background-color: #001529; color: white; padding: 15px; text-align: center; }
        .button { background-color: #52c41a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{titulo}}</h1>
        </div>
        
        <div class="content">
            <p>Estimado/a {{nombre_cliente}},</p>
            
            <p>{{mensaje_principal}}</p>
            
            {% if datos_reserva %}
            <div class="reserva-details">
                <h3>Detalles de su reserva:</h3>
                <ul>
                    <li><strong>Hotel:</strong> {{hotel_nombre}}</li>
                    <li><strong>Confirmación:</strong> {{numero_confirmacion}}</li>
                    <li><strong>Check-in:</strong> {{fecha_checkin}} a las {{hora_checkin}}</li>
                    <li><strong>Check-out:</strong> {{fecha_checkout}} a las {{hora_checkout}}</li>
                    <li><strong>Total:</strong> {{monto_total}} {{moneda}}</li>
                </ul>
            </div>
            {% endif %}
            
            {% if accion_requerida %}
            <div style="text-align: center; margin: 20px 0;">
                <a href="{{url_accion}}" class="button">{{texto_boton}}</a>
            </div>
            {% endif %}
            
            <p>Si tiene alguna pregunta, no dude en contactarnos.</p>
        </div>
        
        <div class="footer">
            <p>© 2024 Sistema de Reservas. Todos los derechos reservados.</p>
            <p>📞 +591-3-1234567 | ✉️ soporte@reservas.com</p>
        </div>
    </div>
</body>
</html>
```

## 8. METADATOS Y CONFIGURACIÓN

### 8.1 Configuración de Canales

```json
{
  "canales": {
    "email": {
      "proveedor": "sendgrid",
      "limite_diario": 10000,
      "limite_por_usuario": 50,
      "retry_attempts": 3,
      "retry_interval": 300,
      "plantillas_soportadas": ["html", "texto"],
      "adjuntos_max_size": "10MB"
    },
    "sms": {
      "proveedor": "twilio",
      "limite_diario": 5000,
      "limite_por_usuario": 20,
      "retry_attempts": 2,
      "retry_interval": 60,
      "caracteres_max": 160,
      "enlaces_cortos": true
    },
    "push": {
      "proveedor": "firebase",
      "limite_diario": 100000,
      "limite_por_usuario": 100,
      "retry_attempts": 3,
      "retry_interval": 30,
      "payload_max_size": "4KB"
    },
    "in_app": {
      "almacenamiento": "base_datos",
      "retention_days": 90,
      "auto_mark_read": false,
      "real_time": true
    }
  }
}
```

### 8.2 Prioridades y Comportamiento

```json
{
  "prioridades": {
    "baja": {
      "orden": 1,
      "delay_permitido": 3600,
      "batch_processing": true,
      "retry_attempts": 1
    },
    "normal": {
      "orden": 2,
      "delay_permitido": 300,
      "batch_processing": true,
      "retry_attempts": 2
    },
    "alta": {
      "orden": 3,
      "delay_permitido": 60,
      "batch_processing": false,
      "retry_attempts": 3
    },
    "urgente": {
      "orden": 4,
      "delay_permitido": 0,
      "batch_processing": false,
      "retry_attempts": 5,
      "escalation": true
    }
  }
}
```

## Notas Importantes

1. **Validación**: Todos los payloads son validados antes del procesamiento
2. **Plantillas**: Usar variables en formato {{variable}} para reemplazo dinámico  
3. **Fechas**: Formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ) para timestamps
4. **Montos**: Usar decimal/float para precisión en cálculos monetarios
5. **URLs**: Todas las URLs deben ser válidas y accesibles
6. **Expiración**: Las notificaciones con acciones pueden tener fecha de expiración
7. **Metadatos**: Los metadatos del proveedor son útiles para troubleshooting
8. **Localización**: Considerar zona horaria y idioma del usuario
9. **Rate Limiting**: Respetar límites por canal y usuario
10. **Tracking**: Cada notificación debe tener ID único para seguimiento