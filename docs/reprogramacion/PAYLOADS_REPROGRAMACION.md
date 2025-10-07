# 📦 PAYLOADS DE REPROGRAMACIÓN - Ejemplos Completos

## 🎯 **PAYLOADS PARA REPROGRAMACIÓN**

Esta documentación contiene todos los payloads específicos para el sistema de reprogramación de reservas.

---

## 🔄 **1. REPROGRAMACIÓN BÁSICA DE CLIENTE**

### 📝 **Payload Mínimo**
```json
{
  "nueva_fecha": "2025-11-25T14:30:00Z",
  "motivo": "Cambio de planes por emergencia familiar"
}
```

### ✅ **Respuesta Exitosa (200)**
```json
{
  "id": 1015,
  "usuario": 14,
  "fecha_inicio": "2025-11-25T14:30:00Z",
  "estado": "REPROGRAMADA",
  "fecha_original": "2025-11-20T14:30:00Z",
  "fecha_reprogramacion": "2025-09-20T11:15:00Z",
  "motivo_reprogramacion": "Cambio de planes por emergencia familiar",
  "numero_reprogramaciones": 1,
  "reprogramado_por": 14,
  "total": "2400.00",
  "moneda": "BOB",
  "costo_reprogramacion": "0.00",
  "notificaciones": {
    "cliente_notificado": true,
    "soporte_notificado": true,
    "emails_enviados": 2,
    "notificacion_push": true
  },
  "validaciones_aplicadas": [
    {
      "regla": "TIEMPO_MINIMO",
      "resultado": "APROBADO",
      "detalle": "120 horas de anticipación (requerido: 24)"
    },
    {
      "regla": "LIMITE_REPROGRAMACIONES",
      "resultado": "APROBADO", 
      "detalle": "1 de 3 reprogramaciones utilizadas"
    }
  ]
}
```

---

## 👨‍💼 **2. REPROGRAMACIÓN DE OPERADOR**

### 📝 **Payload con Descuento**
```json
{
  "nueva_fecha": "2025-12-05T16:00:00Z",
  "motivo": "Problema técnico en el sistema original",
  "aplicar_descuento": true,
  "porcentaje_descuento": 5.0,
  "notificar_cliente": true,
  "prioridad": "MEDIA",
  "observaciones_internas": "Reprogramación por mantenimiento preventivo"
}
```

### ✅ **Respuesta con Descuento (200)**
```json
{
  "id": 1020,
  "fecha_inicio": "2025-12-05T16:00:00Z",
  "estado": "REPROGRAMADA",
  "numero_reprogramaciones": 2,
  "descuento_aplicado": {
    "porcentaje": 5.0,
    "monto_descuento": "120.00",
    "total_anterior": "2400.00",
    "total_nuevo": "2280.00",
    "razon": "Descuento por reprogramación técnica"
  },
  "notificaciones": {
    "cliente_notificado": true,
    "email_enviado": true,
    "sms_enviado": true,
    "template_usado": "reprogramacion_con_descuento"
  },
  "operador": {
    "id": 25,
    "nombre": "María Operadora",
    "departamento": "Atención al Cliente"
  }
}
```

---

## 🛡️ **3. REPROGRAMACIÓN ADMINISTRATIVA (ADMIN)**

### 📝 **Payload Completo con Bypass**
```json
{
  "reserva_id": 1025,
  "nueva_fecha": "2025-12-01T08:00:00Z",
  "motivo": "Reprogramación masiva por actualización de sistemas",
  "tipo_reprogramacion": "ADMINISTRATIVA",
  "bypass_reglas": [
    "TIEMPO_MINIMO",
    "DIA_BLACKOUT"
  ],
  "notificar_cliente": true,
  "aplicar_descuento": true,
  "porcentaje_descuento": 15.0,
  "compensacion_adicional": {
    "tipo": "CUPONES",
    "cantidad": 1,
    "valor": "100.00",
    "descripcion": "Cupón de disculpa por inconvenientes"
  },
  "aprobado_por": "admin@sistema.com",
  "prioridad": "ALTA",
  "categoria_reprogramacion": "MANTENIMIENTO_SISTEMA",
  "observaciones_internas": "Reprogramación masiva - Actualización crítica de seguridad",
  "observaciones_cliente": "Disculpe las molestias, hemos mejorado nuestros sistemas para brindarle mejor servicio"
}
```

### ✅ **Respuesta Administrativa (200)**
```json
{
  "reprogramacion_exitosa": true,
  "reserva": {
    "id": 1025,
    "fecha_inicio": "2025-12-01T08:00:00Z",
    "estado": "REPROGRAMADA",
    "tipo_reprogramacion": "ADMINISTRATIVA",
    "numero_reprogramaciones": 1
  },
  "beneficios_aplicados": {
    "descuento": {
      "porcentaje": 15.0,
      "monto": "360.00",
      "total_anterior": "2400.00",
      "total_nuevo": "2040.00"
    },
    "compensacion": {
      "cupon_generado": {
        "codigo": "DISCULPA2025",
        "valor": "100.00",
        "valido_hasta": "2026-12-31T23:59:59Z",
        "descripcion": "Cupón de disculpa por inconvenientes"
      }
    }
  },
  "reglas_bypass": [
    {
      "regla": "TIEMPO_MINIMO",
      "bypass_aplicado": true,
      "razon": "Reprogramación administrativa urgente",
      "autorizado_por": "admin@sistema.com"
    },
    {
      "regla": "DIA_BLACKOUT", 
      "bypass_aplicado": true,
      "razon": "Fecha única disponible por mantenimiento",
      "autorizado_por": "admin@sistema.com"
    }
  ],
  "notificaciones": {
    "cliente_notificado": true,
    "template_especial": "reprogramacion_administrativa",
    "canales_utilizados": ["email", "sms", "push"],
    "mensaje_personalizado": true
  }
}
```

---

## 🔍 **4. VERIFICACIÓN PREVIA**

### 📝 **Request de Verificación**
```
GET /api/reservas/1015/puede-reprogramar/
```

### ✅ **Respuesta: Puede Reprogramar**
```json
{
  "puede_reprogramar": true,
  "razon": "Cumple todas las condiciones para reprogramar",
  "reprogramaciones_restantes": 2,
  "tiempo_minimo_requerido_horas": 24,
  "tiempo_actual_hasta_reserva_horas": 120,
  "reglas_evaluadas": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "tipo_regla": "TIEMPO_MINIMO",
      "cumple": true,
      "detalle": "Faltan 120 horas, requerido: 24",
      "valor_actual": 120,
      "valor_requerido": 24
    },
    {
      "id": 2,
      "nombre": "Máximo 3 reprogramaciones",
      "tipo_regla": "LIMITE_REPROGRAMACIONES",
      "cumple": true,
      "detalle": "Ha usado 1 de 3 reprogramaciones permitidas",
      "valor_actual": 1,
      "valor_requerido": 3
    },
    {
      "id": 3,
      "nombre": "Sin fines de semana",
      "tipo_regla": "DIA_BLACKOUT",
      "cumple": true,
      "detalle": "Fecha actual es día laborable",
      "dia_actual": "JUEVES",
      "dias_no_permitidos": ["SABADO", "DOMINGO"]
    }
  ],
  "costos_estimados": {
    "costo_reprogramacion": "0.00",
    "aplica_descuento": false,
    "total_estimado": "2400.00"
  }
}
```

### ❌ **Respuesta: No Puede Reprogramar**
```json
{
  "puede_reprogramar": false,
  "razon": "Múltiples reglas violadas",
  "reglas_violadas": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "tipo_regla": "TIEMPO_MINIMO",
      "cumple": false,
      "detalle": "Solo faltan 12 horas, se requieren 24",
      "valor_actual": 12,
      "valor_requerido": 24,
      "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación",
      "tiempo_restante_para_cumplir": "12 horas"
    },
    {
      "id": 2,
      "nombre": "Máximo 3 reprogramaciones",
      "tipo_regla": "LIMITE_REPROGRAMACIONES",
      "cumple": false,
      "detalle": "Ha alcanzado el límite máximo",
      "valor_actual": 3,
      "valor_requerido": 3,
      "mensaje_error": "Ha alcanzado el límite máximo de reprogramaciones",
      "proxima_disponibilidad": "Solo disponible para administradores"
    }
  ],
  "alternativas_sugeridas": [
    {
      "opcion": "Cancelación con reembolso parcial",
      "descripcion": "Puede cancelar y recibir 70% de reembolso",
      "porcentaje_reembolso": 70
    },
    {
      "opcion": "Transferir a otro usuario",
      "descripcion": "Puede transferir la reserva a otra persona",
      "costo_transferencia": "25.00"
    }
  ]
}
```

---

## 📚 **5. HISTORIAL DE REPROGRAMACIONES**

### 📝 **Request Historial**
```
GET /api/reservas/1015/historial-reprogramacion/
```

### ✅ **Respuesta Historial Completo**
```json
[
  {
    "id": 1,
    "fecha_anterior": "2025-11-15T09:00:00Z",
    "fecha_nueva": "2025-11-20T14:30:00Z",
    "motivo": "Conflicto de horarios en el trabajo",
    "tipo_reprogramacion": "CLIENTE",
    "costo_aplicado": "0.00",
    "descuento_aplicado": null,
    "reprogramado_por": {
      "id": 14,
      "username": "cliente@email.com",
      "first_name": "Juan",
      "last_name": "Pérez",
      "rol": "CLIENTE"
    },
    "fecha_reprogramacion": "2025-09-18T10:20:00Z",
    "estado_notificacion": {
      "cliente_notificado": true,
      "email_enviado": true,
      "fecha_notificacion": "2025-09-18T10:21:00Z"
    },
    "reglas_aplicadas": [
      "TIEMPO_MINIMO",
      "LIMITE_REPROGRAMACIONES"
    ]
  },
  {
    "id": 2,
    "fecha_anterior": "2025-11-20T14:30:00Z",
    "fecha_nueva": "2025-11-25T14:30:00Z",
    "motivo": "Cliente solicitó cambio por viaje de emergencia",
    "tipo_reprogramacion": "OPERADOR_ASISTIDO",
    "costo_aplicado": "0.00",
    "descuento_aplicado": {
      "porcentaje": 5.0,
      "monto": "120.00",
      "razon": "Disculpa por inconvenientes"
    },
    "reprogramado_por": {
      "id": 25,
      "username": "operador@sistema.com",
      "first_name": "María",
      "last_name": "Operadora",
      "rol": "OPERADOR"
    },
    "fecha_reprogramacion": "2025-09-20T11:15:00Z",
    "estado_notificacion": {
      "cliente_notificado": true,
      "email_enviado": true,
      "sms_enviado": true,
      "push_enviado": true,
      "fecha_notificacion": "2025-09-20T11:16:00Z"
    },
    "observaciones_internas": "Cliente llamó preocupado, se aplicó descuento como gesto de buena voluntad",
    "reglas_aplicadas": [
      "TIEMPO_MINIMO",
      "LIMITE_REPROGRAMACIONES"
    ]
  }
]
```

---

## ⚙️ **6. GESTIÓN DE REGLAS**

### 📝 **Crear Nueva Regla**
```json
{
  "nombre": "Tiempo mínimo VIP",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 12,
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "Clientes VIP pueden reprogramar con 12 horas de anticipación",
  "fecha_inicio_vigencia": "2025-10-01T00:00:00Z",
  "fecha_fin_vigencia": "2026-12-31T23:59:59Z",
  "condiciones_extras": {
    "solo_clientes_vip": true,
    "nivel_minimo": "GOLD",
    "excluir_feriados": false
  }
}
```

### 📝 **Actualizar Regla Existente**
```json
{
  "id": 3,
  "nombre": "Sin fines de semana - Actualizado",
  "valor_texto": "SABADO,DOMINGO,FERIADOS",
  "activa": true,
  "mensaje_error": "No se permite reprogramar para fines de semana ni feriados",
  "condiciones_extras": {
    "excluir_feriados_nacionales": true,
    "incluir_feriados_locales": ["2025-12-25", "2026-01-01"],
    "excepciones_emergencia": true
  }
}
```

### ✅ **Respuesta Regla Creada/Actualizada**
```json
{
  "id": 6,
  "nombre": "Tiempo mínimo VIP",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 12,
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "Clientes VIP pueden reprogramar con 12 horas de anticipación",
  "fecha_inicio_vigencia": "2025-10-01T00:00:00Z",
  "fecha_fin_vigencia": "2026-12-31T23:59:59Z",
  "condiciones_extras": {
    "solo_clientes_vip": true,
    "nivel_minimo": "GOLD",
    "excluir_feriados": false
  },
  "created_at": "2025-09-20T12:00:00Z",
  "updated_at": "2025-09-20T12:00:00Z",
  "creado_por": {
    "id": 1,
    "username": "admin@sistema.com",
    "first_name": "Admin",
    "last_name": "Sistema"
  }
}
```

---

## 🚫 **7. EJEMPLOS DE ERRORES ESPECÍFICOS**

### ❌ **Error: Tiempo Insuficiente**
```json
{
  "detail": "Debe reprogramar con al menos 24 horas de anticipación",
  "error_code": "TIEMPO_MINIMO_VIOLADO",
  "regla_violada": {
    "id": 1,
    "nombre": "Tiempo mínimo 24 horas",
    "tipo_regla": "TIEMPO_MINIMO"
  },
  "tiempo_restante_horas": 12,
  "tiempo_requerido_horas": 24,
  "diferencia_horas": -12,
  "fecha_limite_reprogramacion": "2025-09-21T14:30:00Z",
  "alternativas": [
    {
      "opcion": "Cancelación",
      "reembolso_porcentaje": 50,
      "descripcion": "Cancelación tardía con reembolso del 50%"
    }
  ]
}
```

### ❌ **Error: Límite Excedido**
```json
{
  "detail": "Ha alcanzado el límite máximo de reprogramaciones",
  "error_code": "LIMITE_REPROGRAMACIONES_EXCEDIDO",
  "regla_violada": {
    "id": 2,
    "nombre": "Máximo 3 reprogramaciones",
    "tipo_regla": "LIMITE_REPROGRAMACIONES"
  },
  "reprogramaciones_actuales": 3,
  "limite_maximo": 3,
  "historial_reprogramaciones": [
    {
      "fecha": "2025-09-15T10:00:00Z",
      "motivo": "Primera reprogramación"
    },
    {
      "fecha": "2025-09-18T14:00:00Z", 
      "motivo": "Segunda reprogramación"
    },
    {
      "fecha": "2025-09-20T11:00:00Z",
      "motivo": "Tercera reprogramación"
    }
  ],
  "opciones_admin": {
    "puede_autorizar_admin": true,
    "requiere_justificacion": true,
    "contacto_soporte": "soporte@sistema.com"
  }
}
```

### ❌ **Error: Día No Permitido**
```json
{
  "detail": "No se permite reprogramar para fines de semana",
  "error_code": "DIA_BLACKOUT",
  "regla_violada": {
    "id": 3,
    "nombre": "Sin fines de semana",
    "tipo_regla": "DIA_BLACKOUT"
  },
  "fecha_solicitada": "2025-11-23T14:30:00Z",
  "dia_semana": "DOMINGO",
  "dias_no_permitidos": ["SABADO", "DOMINGO"],
  "sugerencias_fechas": [
    {
      "fecha": "2025-11-21T14:30:00Z",
      "dia": "VIERNES",
      "disponible": true
    },
    {
      "fecha": "2025-11-24T14:30:00Z",
      "dia": "LUNES",
      "disponible": true
    },
    {
      "fecha": "2025-11-25T14:30:00Z",
      "dia": "MARTES",
      "disponible": true
    }
  ]
}
```

### ❌ **Error: Fecha No Disponible**
```json
{
  "detail": "La fecha solicitada no está disponible",
  "error_code": "FECHA_NO_DISPONIBLE",
  "fecha_solicitada": "2025-12-25T10:00:00Z",
  "razon": "Fecha completamente reservada",
  "disponibilidad": {
    "reservas_existentes": 15,
    "capacidad_maxima": 15,
    "lista_espera_disponible": true
  },
  "fechas_alternativas": [
    {
      "fecha": "2025-12-24T10:00:00Z",
      "disponibilidad": "ALTA",
      "espacios_libres": 8
    },
    {
      "fecha": "2025-12-26T10:00:00Z",
      "disponibilidad": "MEDIA",
      "espacios_libres": 3
    },
    {
      "fecha": "2025-12-27T10:00:00Z",
      "disponibilidad": "ALTA",
      "espacios_libres": 12
    }
  ]
}
```

---

## 🧪 **8. PAYLOADS PARA TESTING**

### 🔬 **Dataset de Pruebas Completo**
```json
{
  "reprogramacion_valida_cliente": {
    "nueva_fecha": "2025-12-01T10:00:00Z",
    "motivo": "Cambio de horario laboral"
  },
  "reprogramacion_urgente_operador": {
    "nueva_fecha": "2025-11-30T15:00:00Z",
    "motivo": "Emergencia técnica resuelta",
    "aplicar_descuento": true,
    "porcentaje_descuento": 10.0,
    "prioridad": "ALTA"
  },
  "reprogramacion_masiva_admin": {
    "reserva_id": 1030,
    "nueva_fecha": "2025-12-15T09:00:00Z",
    "motivo": "Actualización de infraestructura",
    "tipo_reprogramacion": "ADMINISTRATIVA",
    "bypass_reglas": ["TIEMPO_MINIMO", "DIA_BLACKOUT"],
    "aplicar_descuento": true,
    "porcentaje_descuento": 20.0,
    "compensacion_adicional": {
      "tipo": "CUPONES",
      "valor": "150.00"
    },
    "aprobado_por": "admin@sistema.com"
  },
  "reprogramacion_con_error_tiempo": {
    "nueva_fecha": "2025-09-21T10:00:00Z",
    "motivo": "Muy tarde para reprogramar"
  },
  "reprogramacion_limite_excedido": {
    "nueva_fecha": "2025-12-20T10:00:00Z",
    "motivo": "Cuarta reprogramación (debe fallar)"
  },
  "reprogramacion_fin_semana": {
    "nueva_fecha": "2025-11-23T10:00:00Z",
    "motivo": "Domingo no permitido"
  }
}
```

---

## 💡 **9. UTILIDADES DE VALIDACIÓN**

### 🔍 **Función de Validación Frontend**
```javascript
const validarPayloadReprogramacion = (payload, reserva, reglas) => {
  const errores = {};
  const warnings = [];
  
  // Validar fecha requerida
  if (!payload.nueva_fecha) {
    errores.nueva_fecha = 'Nueva fecha es requerida';
  } else {
    const nuevaFecha = new Date(payload.nueva_fecha);
    const ahora = new Date();
    
    // Validar fecha futura
    if (nuevaFecha <= ahora) {
      errores.nueva_fecha = 'La nueva fecha debe ser en el futuro';
    }
    
    // Validar tiempo mínimo
    const reglaTimepo = reglas.find(r => r.tipo_regla === 'TIEMPO_MINIMO');
    if (reglaTimepo) {
      const horasHasta = (nuevaFecha - ahora) / (1000 * 60 * 60);
      if (horasHasta < reglaTimepo.valor_numerico) {
        errores.nueva_fecha = `Debe reprogramar con al menos ${reglaTimepo.valor_numerico} horas de anticipación`;
      }
    }
    
    // Validar días no permitidos
    const reglaDias = reglas.find(r => r.tipo_regla === 'DIA_BLACKOUT');
    if (reglaDias) {
      const diaSemana = nuevaFecha.toLocaleDateString('es', { weekday: 'long' }).toUpperCase();
      const diasProhibidos = reglaDias.valor_texto.split(',');
      if (diasProhibidos.includes(diaSemana)) {
        errores.nueva_fecha = reglaDias.mensaje_error;
      }
    }
  }
  
  // Validar motivo
  if (!payload.motivo || payload.motivo.trim().length < 10) {
    errores.motivo = 'El motivo debe tener al menos 10 caracteres';
  }
  
  // Validar límite de reprogramaciones
  const reglaLimite = reglas.find(r => r.tipo_regla === 'LIMITE_REPROGRAMACIONES');
  if (reglaLimite && reserva.numero_reprogramaciones >= reglaLimite.valor_numerico) {
    errores.limite = 'Ha alcanzado el límite máximo de reprogramaciones';
  }
  
  // Validar descuentos (solo para operadores/admin)
  if (payload.aplicar_descuento) {
    if (!payload.porcentaje_descuento || payload.porcentaje_descuento <= 0) {
      warnings.push('Descuento solicitado pero porcentaje no válido');
    }
    if (payload.porcentaje_descuento > 50) {
      warnings.push('Descuento superior al 50% requiere aprobación especial');
    }
  }
  
  return {
    valido: Object.keys(errores).length === 0,
    errores: errores,
    warnings: warnings
  };
};
```

### 🔄 **Función de Retry con Backoff**
```javascript
const reprogramarConRetry = async (reservaId, payload, maxIntentos = 3) => {
  for (let intento = 1; intento <= maxIntentos; intento++) {
    try {
      const response = await fetch(`/api/reservas/${reservaId}/reprogramar/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        return await response.json();
      }
      
      // Errores que no deben reintentarse
      if (response.status === 400 || response.status === 403) {
        const error = await response.json();
        throw new Error(error.detail);
      }
      
      // Error de servidor, reintentar
      if (response.status >= 500 && intento < maxIntentos) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, intento) * 1000)
        );
        continue;
      }
      
      throw new Error(`Error ${response.status}: ${response.statusText}`);
      
    } catch (error) {
      if (intento === maxIntentos) throw error;
      
      // Solo reintentar errores de red
      if (error.name === 'TypeError' || error.message.includes('Failed to fetch')) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, intento) * 1000)
        );
      } else {
        throw error;
      }
    }
  }
};
```

---

**✨ ¡Payloads de Reprogramación completamente documentados! ✨**

Esta documentación proporciona todos los ejemplos de payloads necesarios para implementar el sistema de reprogramación con validaciones completas y manejo de errores robusto.