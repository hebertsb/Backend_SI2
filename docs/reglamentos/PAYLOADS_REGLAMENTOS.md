# PAYLOADS REGLAMENTOS - Gestión de Políticas y Reglas

## Estructura del Modelo ReglasReprogramacion

```json
{
  "id": "integer - ID único de la regla",
  "tipo_regla": "string - Tipo de regla (reprogramacion, cancelacion, politica)",
  "nombre_regla": "string - Nombre descriptivo",
  "descripcion": "string - Descripción detallada",
  "dias_minimos_reprogramacion": "integer - Días mínimos para reprogramar",
  "dias_maximos_reprogramacion": "integer - Días máximos para reprogramar",
  "hora_limite_reprogramacion": "time - Hora límite del día",
  "permite_cambio_servicio": "boolean - Permite cambiar servicio",
  "costo_reprogramacion": "decimal - Costo por reprogramar",
  "maximo_reprogramaciones": "integer - Máximo de reprogramaciones",
  "descuento_por_reprogramacion": "decimal - Descuento aplicable",
  "activa": "boolean - Si la regla está activa",
  "fecha_inicio_vigencia": "date - Inicio de vigencia",
  "fecha_fin_vigencia": "date - Fin de vigencia",
  "prioridad": "integer - Prioridad de aplicación",
  "condiciones_especiales": "json - Condiciones adicionales",
  "created_at": "datetime - Fecha de creación",
  "updated_at": "datetime - Fecha de actualización"
}
```

## 1. CREAR NUEVA REGLA

### Request URL
```
POST /api/reglamentos/
```

### Headers
```json
{
  "Authorization": "Bearer {token}",
  "Content-Type": "application/json"
}
```

### Payload - Regla de Reprogramación Básica
```json
{
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Reprogramación Estándar Hotel 5 Estrellas",
  "descripcion": "Regla para hoteles de lujo con mayor flexibilidad",
  "dias_minimos_reprogramacion": 3,
  "dias_maximos_reprogramacion": 30,
  "hora_limite_reprogramacion": "18:00:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "50.00",
  "maximo_reprogramaciones": 2,
  "descuento_por_reprogramacion": "10.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-01-01",
  "fecha_fin_vigencia": "2024-12-31",
  "prioridad": 1
}
```

### Payload - Regla de Cancelación con Condiciones
```json
{
  "tipo_regla": "cancelacion",
  "nombre_regla": "Cancelación con Penalización",
  "descripcion": "Regla de cancelación con penalización según tiempo",
  "dias_minimos_reprogramacion": 0,
  "dias_maximos_reprogramacion": 0,
  "hora_limite_reprogramacion": "12:00:00",
  "permite_cambio_servicio": false,
  "costo_reprogramacion": "0.00",
  "maximo_reprogramaciones": 0,
  "descuento_por_reprogramacion": "0.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-01-01",
  "fecha_fin_vigencia": null,
  "prioridad": 5,
  "condiciones_especiales": {
    "penalizacion_24h": 25.00,
    "penalizacion_48h": 15.00,
    "penalizacion_72h": 5.00,
    "reembolso_completo_dias": 7
  }
}
```

### Payload - Política Especial VIP
```json
{
  "tipo_regla": "politica",
  "nombre_regla": "Política VIP Sin Restricciones",
  "descripcion": "Política especial para clientes VIP",
  "dias_minimos_reprogramacion": 0,
  "dias_maximos_reprogramacion": 365,
  "hora_limite_reprogramacion": "23:59:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "0.00",
  "maximo_reprogramaciones": 999,
  "descuento_por_reprogramacion": "0.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-01-01",
  "fecha_fin_vigencia": null,
  "prioridad": 10,
  "condiciones_especiales": {
    "cliente_vip": true,
    "sin_penalizaciones": true,
    "cambio_fecha_ilimitado": true,
    "upgrade_automatico": true
  }
}
```

### Response Success (201)
```json
{
  "id": 15,
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Reprogramación Estándar Hotel 5 Estrellas",
  "descripcion": "Regla para hoteles de lujo con mayor flexibilidad",
  "dias_minimos_reprogramacion": 3,
  "dias_maximos_reprogramacion": 30,
  "hora_limite_reprogramacion": "18:00:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "50.00",
  "maximo_reprogramaciones": 2,
  "descuento_por_reprogramacion": "10.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-01-01",
  "fecha_fin_vigencia": "2024-12-31",
  "prioridad": 1,
  "condiciones_especiales": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Response Error (400)
```json
{
  "error": "Datos inválidos",
  "details": {
    "dias_minimos_reprogramacion": ["Este campo es requerido"],
    "hora_limite_reprogramacion": ["Formato de hora inválido"],
    "costo_reprogramacion": ["No puede ser negativo"]
  }
}
```

## 2. ACTUALIZAR REGLA

### Request URL
```
PUT /api/reglamentos/{id}/
PATCH /api/reglamentos/{id}/
```

### Payload - Actualización Completa (PUT)
```json
{
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Reprogramación Estándar Actualizada",
  "descripcion": "Regla actualizada con nuevos parámetros",
  "dias_minimos_reprogramacion": 2,
  "dias_maximos_reprogramacion": 45,
  "hora_limite_reprogramacion": "20:00:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "75.00",
  "maximo_reprogramaciones": 3,
  "descuento_por_reprogramacion": "15.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-02-01",
  "fecha_fin_vigencia": "2024-12-31",
  "prioridad": 2,
  "condiciones_especiales": {
    "temporada_alta": true,
    "costo_adicional_fin_semana": 25.00
  }
}
```

### Payload - Actualización Parcial (PATCH)
```json
{
  "costo_reprogramacion": "100.00",
  "maximo_reprogramaciones": 1,
  "condiciones_especiales": {
    "temporada_alta": true,
    "costo_adicional_fin_semana": 50.00,
    "descuento_cliente_frecuente": 20.00
  }
}
```

### Payload - Activar/Desactivar Regla
```json
{
  "activa": false
}
```

### Response Success (200)
```json
{
  "id": 15,
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Reprogramación Estándar Actualizada",
  "descripcion": "Regla actualizada con nuevos parámetros",
  "dias_minimos_reprogramacion": 2,
  "dias_maximos_reprogramacion": 45,
  "hora_limite_reprogramacion": "20:00:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "100.00",
  "maximo_reprogramaciones": 1,
  "descuento_por_reprogramacion": "15.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-02-01",
  "fecha_fin_vigencia": "2024-12-31",
  "prioridad": 2,
  "condiciones_especiales": {
    "temporada_alta": true,
    "costo_adicional_fin_semana": 50.00,
    "descuento_cliente_frecuente": 20.00
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z"
}
```

## 3. ACTUALIZACIÓN MASIVA DE REGLAS

### Request URL
```
POST /api/reglamentos/bulk-update/
```

### Payload - Actualizar Múltiples Reglas
```json
{
  "reglas": [
    {
      "id": 1,
      "costo_reprogramacion": "80.00",
      "activa": true
    },
    {
      "id": 2,
      "maximo_reprogramaciones": 2,
      "descuento_por_reprogramacion": "20.00"
    },
    {
      "id": 3,
      "fecha_fin_vigencia": "2024-06-30",
      "prioridad": 5
    }
  ]
}
```

### Payload - Aplicar Cambio Global
```json
{
  "filtros": {
    "tipo_regla": "reprogramacion",
    "activa": true
  },
  "cambios": {
    "costo_reprogramacion": "60.00",
    "fecha_fin_vigencia": "2024-12-31"
  }
}
```

### Response Success (200)
```json
{
  "actualizadas": 3,
  "errores": [],
  "detalles": [
    {
      "id": 1,
      "status": "actualizada",
      "cambios": ["costo_reprogramacion", "activa"]
    },
    {
      "id": 2,
      "status": "actualizada", 
      "cambios": ["maximo_reprogramaciones", "descuento_por_reprogramacion"]
    },
    {
      "id": 3,
      "status": "actualizada",
      "cambios": ["fecha_fin_vigencia", "prioridad"]
    }
  ]
}
```

## 4. IMPORTAR REGLAS DESDE ARCHIVO

### Request URL
```
POST /api/reglamentos/import/
```

### Headers
```json
{
  "Authorization": "Bearer {token}",
  "Content-Type": "multipart/form-data"
}
```

### Payload - Datos del Archivo
```json
{
  "archivo": "archivo.json",
  "formato": "json",
  "sobrescribir": false,
  "validar_antes": true
}
```

### Estructura del Archivo JSON
```json
{
  "reglas": [
    {
      "tipo_regla": "reprogramacion",
      "nombre_regla": "Regla Importada 1",
      "descripcion": "Primera regla desde importación",
      "dias_minimos_reprogramacion": 3,
      "dias_maximos_reprogramacion": 30,
      "hora_limite_reprogramacion": "18:00:00",
      "permite_cambio_servicio": true,
      "costo_reprogramacion": "50.00",
      "maximo_reprogramaciones": 2,
      "activa": true,
      "fecha_inicio_vigencia": "2024-01-01",
      "prioridad": 1
    },
    {
      "tipo_regla": "cancelacion",
      "nombre_regla": "Regla Importada 2",
      "descripcion": "Segunda regla desde importación",
      "dias_minimos_reprogramacion": 0,
      "hora_limite_reprogramacion": "12:00:00",
      "costo_reprogramacion": "0.00",
      "activa": true,
      "condiciones_especiales": {
        "penalizacion_24h": 30.00
      }
    }
  ]
}
```

### Response Success (200)
```json
{
  "importadas": 2,
  "errores": 0,
  "omitidas": 0,
  "detalles": {
    "creadas": [
      {
        "nombre_regla": "Regla Importada 1",
        "id": 20
      },
      {
        "nombre_regla": "Regla Importada 2", 
        "id": 21
      }
    ],
    "errores": [],
    "omitidas": []
  }
}
```

### Response Con Errores (200)
```json
{
  "importadas": 1,
  "errores": 1,
  "omitidas": 0,
  "detalles": {
    "creadas": [
      {
        "nombre_regla": "Regla Importada 1",
        "id": 20
      }
    ],
    "errores": [
      {
        "nombre_regla": "Regla Importada 2",
        "errores": {
          "costo_reprogramacion": ["Formato decimal inválido"]
        }
      }
    ],
    "omitidas": []
  }
}
```

## 5. VALIDAR REGLAS

### Request URL
```
POST /api/reglamentos/validate/
```

### Payload - Validar Nueva Regla
```json
{
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Regla a Validar",
  "dias_minimos_reprogramacion": 3,
  "dias_maximos_reprogramacion": 15,
  "hora_limite_reprogramacion": "18:00:00",
  "costo_reprogramacion": "50.00",
  "fecha_inicio_vigencia": "2024-01-01",
  "fecha_fin_vigencia": "2024-12-31"
}
```

### Payload - Validar Reglas Existentes
```json
{
  "reglas_ids": [1, 2, 3, 4],
  "incluir_inactivas": false
}
```

### Response Success (200)
```json
{
  "valida": true,
  "errores": [],
  "advertencias": [],
  "conflictos": []
}
```

### Response Con Errores (200)
```json
{
  "valida": false,
  "errores": [
    "Los días mínimos no pueden ser mayores que los máximos",
    "El costo de reprogramación no puede ser negativo"
  ],
  "advertencias": [
    "La fecha de fin de vigencia está muy cerca",
    "Existe otra regla similar con mayor prioridad"
  ],
  "conflictos": [
    {
      "regla_id": 5,
      "nombre_regla": "Regla Conflictiva",
      "motivo": "Misma prioridad y tipo de regla"
    }
  ]
}
```

## 6. DUPLICAR REGLA

### Request URL
```
POST /api/reglamentos/{id}/duplicate/
```

### Payload - Duplicar con Modificaciones
```json
{
  "nombre_regla": "Copia de Regla Original",
  "descripcion": "Regla duplicada con modificaciones",
  "costo_reprogramacion": "75.00",
  "prioridad": 3,
  "fecha_inicio_vigencia": "2024-03-01",
  "condiciones_especiales": {
    "version": "duplicada",
    "fecha_creacion": "2024-01-20"
  }
}
```

### Response Success (201)
```json
{
  "id": 22,
  "original_id": 15,
  "tipo_regla": "reprogramacion",
  "nombre_regla": "Copia de Regla Original",
  "descripcion": "Regla duplicada con modificaciones",
  "dias_minimos_reprogramacion": 2,
  "dias_maximos_reprogramacion": 45,
  "hora_limite_reprogramacion": "20:00:00",
  "permite_cambio_servicio": true,
  "costo_reprogramacion": "75.00",
  "maximo_reprogramaciones": 1,
  "descuento_por_reprogramacion": "15.00",
  "activa": true,
  "fecha_inicio_vigencia": "2024-03-01",
  "fecha_fin_vigencia": "2024-12-31",
  "prioridad": 3,
  "condiciones_especiales": {
    "version": "duplicada",
    "fecha_creacion": "2024-01-20"
  },
  "created_at": "2024-01-20T15:30:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

## 7. EJEMPLOS DE CONDICIONES ESPECIALES

### Condiciones Temporales
```json
{
  "condiciones_especiales": {
    "temporada_alta": true,
    "fechas_especiales": ["2024-12-25", "2024-01-01", "2024-07-28"],
    "dias_semana": ["sabado", "domingo"],
    "horario_especial": {
      "inicio": "18:00",
      "fin": "06:00"
    }
  }
}
```

### Condiciones por Cliente
```json
{
  "condiciones_especiales": {
    "cliente_vip": true,
    "nivel_membresia": "oro",
    "descuento_cliente_frecuente": 25.00,
    "historial_cancelaciones_max": 2
  }
}
```

### Condiciones por Servicio
```json
{
  "condiciones_especiales": {
    "servicios_permitidos": ["hotel", "vuelo"],
    "servicios_excluidos": ["crucero"],
    "costo_adicional_por_servicio": {
      "hotel": 20.00,
      "vuelo": 50.00,
      "paquete_completo": 30.00
    }
  }
}
```

### Condiciones Financieras
```json
{
  "condiciones_especiales": {
    "monto_minimo_reserva": 500.00,
    "porcentaje_penalizacion": 15,
    "descuento_pago_anticipado": 10.00,
    "recargo_pago_tardio": 25.00,
    "moneda": "BOB"
  }
}
```

## 8. CÓDIGOS DE ERROR COMUNES

### Error 400 - Datos Inválidos
```json
{
  "error": "Datos inválidos",
  "codigo": "INVALID_DATA",
  "details": {
    "dias_minimos_reprogramacion": ["Debe ser un número positivo"],
    "fecha_fin_vigencia": ["No puede ser anterior a fecha de inicio"]
  }
}
```

### Error 409 - Conflicto de Reglas
```json
{
  "error": "Conflicto con regla existente",
  "codigo": "RULE_CONFLICT",
  "conflicto": {
    "regla_id": 8,
    "nombre_regla": "Regla Existente",
    "motivo": "Misma prioridad y fechas de vigencia"
  }
}
```

### Error 422 - Regla Inválida
```json
{
  "error": "Regla no puede ser procesada",
  "codigo": "UNPROCESSABLE_RULE",
  "razones": [
    "Los días máximos son menores que los mínimos",
    "La fecha de fin es anterior a la fecha de inicio"
  ]
}
```

## Notas Importantes

1. **Validación**: Todas las reglas son validadas antes de ser guardadas
2. **Prioridad**: Mayor número = mayor prioridad de aplicación
3. **Fechas**: Usar formato ISO (YYYY-MM-DD) para fechas
4. **Horarios**: Usar formato HH:MM:SS para horarios
5. **Decimales**: Usar string para valores monetarios (precisión)
6. **JSON**: Las condiciones especiales permiten estructura flexible
7. **Activación**: Solo reglas activas son aplicadas en el sistema
8. **Versionado**: El campo updated_at permite rastrear cambios