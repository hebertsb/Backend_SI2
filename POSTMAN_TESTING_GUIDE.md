# 📋 Ejemplos de Postman - Testing de Reservas y Reprogramación

## 🔧 Configuración Inicial de Postman

### Variables de Entorno
Crear un **Environment** en Postman con estas variables:

```json
{
  "base_url": "http://localhost:8000",
  "api_prefix": "/api",
  "token": "{{tu_token_jwt}}",
  "user_id": "{{id_usuario_logueado}}"
}
```

### Headers Globales
Configurar estos headers para todas las requests:

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{token}}
```

## 🎯 1. Verificar Reservas por Estado

### 1.1 Listar TODAS las Reservas
```http
GET {{base_url}}{{api_prefix}}/reservas/
```

**Parámetros opcionales**:
- `?limit=10` - Limitar resultados
- `?offset=0` - Paginación
- `?ordering=-created_at` - Ordenar por fecha

### 1.2 Filtrar Reservas por Estado

#### Reservas PAGADAS
```http
GET {{base_url}}{{api_prefix}}/reservas/?estado=PAGADA
```

#### Reservas PENDIENTES
```http
GET {{base_url}}{{api_prefix}}/reservas/?estado=PENDIENTE
```

#### Reservas CONFIRMADAS
```http
GET {{base_url}}{{api_prefix}}/reservas/?estado=CONFIRMADA
```

#### Reservas CANCELADAS
```http
GET {{base_url}}{{api_prefix}}/reservas/?estado=CANCELADA
```

### 1.3 Filtrar por Usuario Específico
```http
GET {{base_url}}{{api_prefix}}/reservas/?usuario={{user_id}}
```

### 1.4 Filtrar por Rango de Fechas
```http
GET {{base_url}}{{api_prefix}}/reservas/?fecha_inicio__gte=2024-01-01&fecha_inicio__lte=2024-12-31
```

### 1.5 Consulta Avanzada - Reservas Reprogramables
```http
GET {{base_url}}{{api_prefix}}/reservas/?estado__in=CONFIRMADA,PAGADA&fecha_inicio__gte={{fecha_hoy}}
```

## 🔍 2. Verificar Detalles de Reserva Específica

### 2.1 Obtener Reserva Completa
```http
GET {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/
```

**Respuesta esperada**:
```json
{
    "id": 1,
    "usuario": {
        "id": 1,
        "nombres": "Juan",
        "apellidos": "Pérez",
        "email": "juan@email.com"
    },
    "estado": "CONFIRMADA",
    "fecha_inicio": "2024-02-15T10:00:00Z",
    "fecha_fin": "2024-02-15T18:00:00Z",
    "total": 150.00,
    "moneda": "BOB",
    "numero_reprogramaciones": 0,
    "puede_reprogramar": true,
    "detalles": [
        {
            "servicio": {
                "id": 1,
                "titulo": "Tour Samaipata",
                "precio_base": 75.00
            },
            "cantidad": 2,
            "precio_unitario": 75.00
        }
    ],
    "historial_reprogramaciones": []
}
```

### 2.2 Verificar si Puede Reprogramar
```http
GET {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/puede-reprogramar/
```

**Respuesta**:
```json
{
    "puede_reprogramar": true,
    "razon": "La reserva cumple todos los requisitos",
    "reglas_aplicadas": [
        {
            "tipo": "TIEMPO_MINIMO",
            "cumple": true,
            "valor_requerido": "24 horas"
        },
        {
            "tipo": "LIMITE_REPROGRAMACIONES", 
            "cumple": true,
            "valor_actual": "0/3"
        }
    ]
}
```

## 🎮 3. Testing de Reprogramación

### 3.1 Reprogramar Reserva (Éxito)
```http
POST {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/reprogramar/
```

**Body (JSON)**:
```json
{
    "fecha_inicio": "2024-03-15T14:00:00Z",
    "fecha_fin": "2024-03-15T22:00:00Z",
    "motivo": "Cliente solicitó cambio por compromisos laborales"
}
```

**Respuesta exitosa**:
```json
{
    "mensaje": "Reserva reprogramada exitosamente",
    "reserva": {
        "id": 1,
        "fecha_inicio": "2024-03-15T14:00:00Z",
        "fecha_fin": "2024-03-15T22:00:00Z",
        "estado": "CONFIRMADA",
        "numero_reprogramaciones": 1
    },
    "notificaciones": {
        "cliente_notificado": true,
        "admin_notificado": true
    },
    "historial": {
        "id": 5,
        "fecha_anterior": "2024-02-15T10:00:00Z",
        "fecha_nueva": "2024-03-15T14:00:00Z",
        "motivo": "Cliente solicitó cambio por compromisos laborales",
        "fecha_reprogramacion": "2024-01-20T15:45:00Z"
    }
}
```

### 3.2 Reprogramar con Error (Violación de Reglas)
```http
POST {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/reprogramar/
```

**Body (fecha muy próxima - viola tiempo mínimo)**:
```json
{
    "fecha_inicio": "2024-01-21T10:00:00Z",
    "motivo": "Cambio urgente"
}
```

**Respuesta de error**:
```json
{
    "error": "Reprogramación no permitida",
    "detalles": {
        "fecha_inicio": [
            "La reprogramación debe hacerse con al menos 24 horas de anticipación."
        ]
    },
    "reglas_violadas": [
        {
            "tipo": "TIEMPO_MINIMO",
            "valor_requerido": 24,
            "valor_proporcionado": 12,
            "mensaje": "Debe reprogramar con al menos 24 horas de anticipación"
        }
    ]
}
```

## 📊 4. Consultas de Estados y Estadísticas

### 4.1 Resumen de Estados
```http
GET {{base_url}}{{api_prefix}}/reservas/resumen-estados/
```

**Respuesta**:
```json
{
    "total_reservas": 150,
    "por_estado": {
        "PENDIENTE": 15,
        "CONFIRMADA": 80,
        "PAGADA": 45,
        "CANCELADA": 10
    },
    "reprogramaciones_mes": 12,
    "proximas_24h": 8
}
```

### 4.2 Reservas del Usuario Actual
```http
GET {{base_url}}{{api_prefix}}/reservas/mis-reservas/
```

### 4.3 Historial de Reprogramaciones
```http
GET {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/historial/
```

## 🔧 5. Gestión de Reglas (Solo Admins)

### 5.1 Listar Reglas Activas
```http
GET {{base_url}}{{api_prefix}}/reglas-reprogramacion/activas/
```

### 5.2 Crear Nueva Regla
```http
POST {{base_url}}{{api_prefix}}/reglas-reprogramacion/
```

**Body**:
```json
{
    "nombre": "Tiempo mínimo 48h para servicios premium",
    "tipo_regla": "TIEMPO_MINIMO",
    "aplicable_a": "CLIENTE",
    "valor_numerico": 48,
    "activa": true,
    "prioridad": 1,
    "mensaje_error": "Los servicios premium requieren 48 horas de anticipación"
}
```

## 🧪 6. Scripts de Testing Automático

### 6.1 Test Suite Básico (Collection de Postman)

```javascript
// Pre-request Script para obtener token
pm.test("Obtener token de autenticación", function () {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/auth/login/",
        method: 'POST',
        header: {
            'Content-Type': 'application/json',
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                email: "admin@test.com",
                password: "admin123"
            })
        }
    }, function (err, response) {
        if (response.json().access) {
            pm.environment.set("token", response.json().access);
        }
    });
});

// Test para verificar respuesta
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has reservas", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('results');
    pm.expect(responseJson.results).to.be.an('array');
});
```

### 6.2 Test de Flujo Completo

```javascript
// 1. Listar reservas
// 2. Seleccionar una reprogramable
// 3. Verificar reglas
// 4. Reprogramar
// 5. Verificar notificaciones

pm.test("Flujo completo de reprogramación", function () {
    // Obtener primera reserva reprogramable
    const reservas = pm.response.json().results;
    const reprogramable = reservas.find(r => r.puede_reprogramar === true);
    
    if (reprogramable) {
        pm.environment.set("reserva_test_id", reprogramable.id);
        console.log("Reserva seleccionada para test:", reprogramable.id);
    } else {
        console.log("No hay reservas reprogramables para testing");
    }
});
```

## 🎯 7. Casos de Prueba Específicos

### 7.1 Caso: Cliente con Múltiples Reservas
```http
GET {{base_url}}{{api_prefix}}/reservas/?usuario=5&ordering=-fecha_inicio
```

### 7.2 Caso: Reservas que Vencen Pronto
```http
GET {{base_url}}{{api_prefix}}/reservas/?fecha_inicio__gte={{fecha_hoy}}&fecha_inicio__lte={{fecha_manana}}
```

### 7.3 Caso: Reservas con Máximas Reprogramaciones
```http
GET {{base_url}}{{api_prefix}}/reservas/?numero_reprogramaciones__gte=3
```

### 7.4 Caso: Testing de Límites de Tiempo
```http
POST {{base_url}}{{api_prefix}}/reservas/{{reserva_id}}/reprogramar/
```

**Diferentes escenarios de fecha**:
```json
// Muy próxima (debe fallar)
{"fecha_inicio": "{{fecha_en_12_horas}}"}

// Muy lejana (debe fallar si hay límite máximo)  
{"fecha_inicio": "{{fecha_en_2_anos}}"}

// Fin de semana (puede fallar si hay blackout)
{"fecha_inicio": "{{proximo_sabado}}"}

// Horario nocturno (puede fallar)
{"fecha_inicio": "{{fecha_2am}}"}
```

## 🔍 8. Debugging y Troubleshooting

### 8.1 Verificar Configuración del Sistema
```http
GET {{base_url}}{{api_prefix}}/system/health/
```

### 8.2 Logs de Notificaciones
```http
GET {{base_url}}{{api_prefix}}/reservas/logs/notificaciones/?limit=10
```

### 8.3 Métricas de Reprogramación
```http
GET {{base_url}}{{api_prefix}}/reservas/metricas/reprogramaciones/
```

## 📝 9. Notas para Testing

### Estados de Reserva Válidos:
- `PENDIENTE` - Recién creada, esperando confirmación
- `CONFIRMADA` - Confirmada, puede ser reprogramada
- `PAGADA` - Pagada, puede ser reprogramada
- `CANCELADA` - Cancelada, NO puede reprogramarse

### Reglas Típicas a Probar:
1. **Tiempo mínimo**: 24 horas de anticipación
2. **Límite reprogramaciones**: Máximo 3 veces
3. **Días blackout**: Sin fines de semana
4. **Horas blackout**: Sin horarios nocturnos

### Variables Dinámicas para Tests:
```javascript
// En Pre-request Script
const now = new Date();
const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
const nextWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);

pm.environment.set("fecha_hoy", now.toISOString());
pm.environment.set("fecha_manana", tomorrow.toISOString());  
pm.environment.set("fecha_proxima_semana", nextWeek.toISOString());
```

¡Ahora puedes importar estos ejemplos en Postman y empezar a probar todo el sistema de reprogramación!