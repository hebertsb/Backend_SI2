# 🚫 CONDICIONES QUE IMPIDEN REPROGRAMAR UNA RESERVA

## 📋 RESUMEN EJECUTIVO
Una reserva **NO puede ser reprogramada** si cumple cualquiera de las siguientes condiciones:

---

## 🔴 1. ESTADO DE LA RESERVA

### ❌ Estados que impiden reprogramación:
- **CANCELADA** - Las reservas canceladas no pueden reprogramarse
- *(Los estados PENDIENTE, CONFIRMADA, PAGADA, REPROGRAMADA sí permiten reprogramación)*

---

## ⏰ 2. RESTRICCIONES DE TIEMPO

### 📅 Tiempo Mínimo de Anticipación:
- **Clientes regulares**: Mínimo 24 horas de anticipación
- **Administradores**: Mínimo 12 horas de anticipación
- **Fecha pasada**: Nunca se puede reprogramar a una fecha pasada

### 📅 Tiempo Máximo:
- **Límite general**: No más de 1 año en el futuro (365 días)

---

## 🔢 3. LÍMITES DE REPROGRAMACIONES

### 📊 Número máximo de reprogramaciones:
- **Por reserva**: Máximo 3 reprogramaciones por reserva
- **Por día**: Máximo 3 reprogramaciones por usuario por día
- **Por semana**: Límites semanales (si están configurados)
- **Por mes**: Límites mensuales (si están configurados)

---

## 📆 4. DÍAS Y HORARIOS BLACKOUT

### 🚫 Días no permitidos:
- **Domingos**: No se permite reprogramar para domingos
- *(Configurables según reglas del sistema)*

### 🕐 Horarios no permitidos:
- **Horarios nocturnos**: Según configuración del sistema
- *(Ejemplo: no reprogramar entre 00:00-06:00)*

---

## 👥 5. RESTRICCIONES POR USUARIO

### 🔐 Permisos:
- **Cliente**: Solo puede reprogramar sus propias reservas
- **Sin rol**: Usuarios sin rol ADMIN, OPERADOR o CLIENTE no pueden reprogramar
- **Reserva ajena**: Un cliente no puede reprogramar reservas de otros usuarios

---

## 📊 6. CAPACIDAD Y DISPONIBILIDAD

### 🏢 Límites de capacidad:
- **Capacidad máxima por fecha**: 50 reservas por fecha (configurable)
- **Fecha no disponible**: Si la nueva fecha ya está completa
- **Servicios no disponibles**: Si el servicio no está disponible en la nueva fecha

---

## 🎯 7. RESTRICCIONES DE SERVICIOS

### 🚫 Servicios con restricciones especiales:
- **Servicios premium**: Pueden requerir más tiempo de anticipación
- **Servicios restringidos**: Lista configurable de servicios con reglas especiales
- **Servicios estacionales**: No disponibles en ciertas fechas

---

## 🔍 8. VALIDACIONES TÉCNICAS

### ⚠️ Errores técnicos:
- **Misma fecha**: No se puede reprogramar a la misma fecha actual
- **Usuario sin roles**: Usuario no tiene roles válidos asignados
- **Base de datos**: Problemas de integridad de datos

---

## 💡 EJEMPLOS PRÁCTICOS

### ✅ PUEDE reprogramar:
```
ID: 1005 - Estado: PAGADA - Fecha: 2025-10-04 - Reprogramaciones: 0/3
ID: 1002 - Estado: REPROGRAMADA - Fecha: 2025-11-05 - Reprogramaciones: 0/3  
ID: 1004 - Estado: PENDIENTE - Fecha: 2025-09-26 - Reprogramaciones: 0/3
```

### ❌ NO puede reprogramar:
```
ID: 1001 - Estado: CANCELADA (estado inválido)
ID: 1003 - Estado: CANCELADA (estado inválido)  
ID: 1007 - Estado: PENDIENTE - Fecha: 2025-09-20 (muy próxima, menos de 24h)
```

---

## 🔧 CONFIGURACIÓN ACTUAL DEL SISTEMA

Según las reglas encontradas en `reglas_reprogramacion_inicial.json`:

1. **Tiempo mínimo estándar**: 24 horas
2. **Tiempo mínimo administradores**: 12 horas  
3. **Límite reprogramaciones**: 3 por reserva
4. **Días blackout**: Domingos prohibidos
5. **Límite diario**: 3 reprogramaciones por día
6. **Capacidad máxima**: 50 reservas por fecha

---

## 🛠️ CÓMO VERIFICAR EN POSTMAN

```bash
# Verificar si puede reprogramar
GET http://127.0.0.1:8000/api/reservas/{id}/puede-reprogramar/

# Respuesta exitosa:
{
  "puede_reprogramar": true/false,
  "numero_reprogramaciones": 0,
  "limite_reprogramaciones": 3,
  "estado_actual": "PAGADA",
  "fecha_actual": "2025-10-04T04:00:00Z"
}
```

---

Esta documentación refleja todas las condiciones implementadas en el sistema actual. Las reglas son dinámicas y configurables a través del modelo `ReglasReprogramacion`.