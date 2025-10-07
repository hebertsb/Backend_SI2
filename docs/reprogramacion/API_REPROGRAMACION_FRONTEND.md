# 🔄 SISTEMA DE REPROGRAMACIÓN - Guía Completa para Frontend

## 🎯 **OVERVIEW DEL SISTEMA**

El sistema de reprogramación permite cambiar fechas de reservas con validaciones automáticas, historial completo y notificaciones integradas.

---

## 🔗 **ENDPOINTS PRINCIPALES**

### 📋 **BASE URL**
```
http://localhost:8000/api/
```

### 🌐 **ENDPOINTS DISPONIBLES**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/reservas/{id}/reprogramar/` | Reprogramar reserva específica |
| `GET` | `/reservas/{id}/puede-reprogramar/` | Verificar si se puede reprogramar |
| `GET` | `/reservas/{id}/historial-reprogramacion/` | Ver historial de cambios |
| `POST` | `/gestion-reprogramacion/` | Reprogramación avanzada (admin) |
| `GET` | `/reglas-reprogramacion/` | Obtener reglas de negocio |
| `POST` | `/reglas-reprogramacion/` | Crear nueva regla (admin) |
| `PUT` | `/reglas-reprogramacion/{id}/` | Actualizar regla (admin) |
| `DELETE` | `/reglas-reprogramacion/{id}/` | Eliminar regla (admin) |

---

## 🔐 **AUTENTICACIÓN**

### 📋 **Headers Requeridos**
```javascript
{
  "Authorization": "Bearer YOUR_JWT_TOKEN",
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

### 🎭 **Roles y Permisos**

| Rol | Puede Reprogramar | Limitaciones |
|-----|------------------|--------------|
| **CLIENTE** | ✅ Sus propias reservas | Reglas estrictas de tiempo |
| **OPERADOR** | ✅ Cualquier reserva | Reglas medias |
| **ADMIN** | ✅ Cualquier reserva | Sin restricciones especiales |

---

## 📦 **1. REPROGRAMAR RESERVA**

### 🎯 **Endpoint**
```
POST /api/reservas/{reserva_id}/reprogramar/
```

### 📝 **Payload Básico**
```json
{
  "nueva_fecha": "2025-11-25T14:30:00Z",
  "motivo": "Cliente solicitó cambio por viaje de emergencia"
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
  "motivo_reprogramacion": "Cliente solicitó cambio por viaje de emergencia",
  "numero_reprogramaciones": 1,
  "reprogramado_por": 14,
  "total": "2400.00",
  "moneda": "BOB",
  "notificaciones": {
    "cliente_notificado": true,
    "soporte_notificado": true,
    "emails_enviados": 2
  },
  "historial_reprogramacion": [
    {
      "id": 1,
      "fecha_anterior": "2025-11-20T14:30:00Z",
      "fecha_nueva": "2025-11-25T14:30:00Z",
      "motivo": "Cliente solicitó cambio por viaje de emergencia",
      "reprogramado_por": {
        "id": 14,
        "username": "cliente@email.com",
        "first_name": "Juan",
        "last_name": "Pérez"
      },
      "fecha_reprogramacion": "2025-09-20T11:15:00Z"
    }
  ]
}
```

### ❌ **Errores Comunes**

#### 🚫 **Error: Muy Cerca de la Fecha (400)**
```json
{
  "detail": "Debe reprogramar con al menos 24 horas de anticipación",
  "error_code": "TIEMPO_MINIMO_VIOLADO",
  "regla_violada": "Tiempo mínimo 24 horas",
  "tiempo_restante_horas": 12
}
```

#### 🚫 **Error: Límite de Reprogramaciones (400)**
```json
{
  "detail": "Ha alcanzado el límite máximo de reprogramaciones",
  "error_code": "LIMITE_REPROGRAMACIONES_EXCEDIDO",
  "reprogramaciones_actuales": 3,
  "limite_maximo": 3
}
```

#### 🚫 **Error: Día No Permitido (400)**
```json
{
  "detail": "No se permite reprogramar para fines de semana",
  "error_code": "DIA_BLACKOUT",
  "fecha_solicitada": "2025-11-23T14:30:00Z",
  "dia_semana": "DOMINGO",
  "dias_no_permitidos": ["SABADO", "DOMINGO"]
}
```

---

## 🔍 **2. VERIFICAR SI PUEDE REPROGRAMAR**

### 🎯 **Endpoint**
```
GET /api/reservas/{reserva_id}/puede-reprogramar/
```

### ✅ **Respuesta: Puede Reprogramar**
```json
{
  "puede_reprogramar": true,
  "razon": "Cumple todas las condiciones",
  "reprogramaciones_restantes": 2,
  "tiempo_minimo_horas": 24,
  "reglas_aplicables": [
    {
      "nombre": "Tiempo mínimo 24 horas",
      "cumple": true,
      "detalle": "Faltan 72 horas para la reserva"
    },
    {
      "nombre": "Máximo 3 reprogramaciones",
      "cumple": true,
      "detalle": "Ha usado 1 de 3 reprogramaciones"
    }
  ]
}
```

### ❌ **Respuesta: No Puede Reprogramar**
```json
{
  "puede_reprogramar": false,
  "razon": "Límite de reprogramaciones excedido",
  "reprogramaciones_restantes": 0,
  "reglas_violadas": [
    {
      "nombre": "Máximo 3 reprogramaciones",
      "cumple": false,
      "detalle": "Ha alcanzado el límite de 3 reprogramaciones",
      "mensaje_error": "Ha alcanzado el límite máximo de reprogramaciones"
    }
  ]
}
```

---

## 📚 **3. HISTORIAL DE REPROGRAMACIONES**

### 🎯 **Endpoint**
```
GET /api/reservas/{reserva_id}/historial-reprogramacion/
```

### ✅ **Respuesta Completa**
```json
[
  {
    "id": 1,
    "fecha_anterior": "2025-11-15T09:00:00Z",
    "fecha_nueva": "2025-11-20T14:30:00Z",
    "motivo": "Conflicto de horarios en el trabajo",
    "reprogramado_por": {
      "id": 14,
      "username": "cliente@email.com",
      "first_name": "Juan",
      "last_name": "Pérez"
    },
    "fecha_reprogramacion": "2025-09-18T10:20:00Z"
  },
  {
    "id": 2,
    "fecha_anterior": "2025-11-20T14:30:00Z",
    "fecha_nueva": "2025-11-25T14:30:00Z",
    "motivo": "Cliente solicitó cambio por viaje de emergencia",
    "reprogramado_por": {
      "id": 14,
      "username": "cliente@email.com",
      "first_name": "Juan",
      "last_name": "Pérez"
    },
    "fecha_reprogramacion": "2025-09-20T11:15:00Z"
  }
]
```

---

## ⚙️ **4. GESTIÓN AVANZADA (ADMIN/OPERADOR)**

### 🎯 **Endpoint**
```
POST /api/gestion-reprogramacion/
```

### 📝 **Payload Avanzado**
```json
{
  "reserva_id": 1015,
  "nueva_fecha": "2025-12-01T10:00:00Z",
  "motivo": "Reprogramación por mantenimiento de sistema",
  "tipo_reprogramacion": "ADMINISTRATIVA",
  "notificar_cliente": true,
  "aplicar_descuento": true,
  "porcentaje_descuento": 10.0,
  "observaciones_internas": "Reprogramación masiva por actualización de sistemas",
  "prioridad": "ALTA",
  "bypass_reglas": ["TIEMPO_MINIMO"],
  "aprobado_por": "admin@sistema.com"
}
```

### ✅ **Respuesta Exitosa (200)**
```json
{
  "reserva_reprogramada": {
    "id": 1015,
    "nueva_fecha": "2025-12-01T10:00:00Z",
    "estado": "REPROGRAMADA",
    "descuento_aplicado": {
      "porcentaje": 10.0,
      "monto_descuento": "240.00",
      "total_anterior": "2400.00",
      "total_nuevo": "2160.00"
    }
  },
  "notificaciones": {
    "cliente_notificado": true,
    "email_enviado": true,
    "sms_enviado": false,
    "notificacion_push": true
  },
  "reglas_bypass": [
    {
      "regla": "TIEMPO_MINIMO",
      "razon": "Reprogramación administrativa autorizada",
      "autorizado_por": "admin@sistema.com"
    }
  ],
  "historial_creado": true
}
```

---

## 📋 **5. REGLAS DE REPROGRAMACIÓN**

### 🎯 **Obtener Reglas**
```
GET /api/reglas-reprogramacion/
```

### ✅ **Respuesta de Reglas**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "tipo_regla": "TIEMPO_MINIMO",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 24,
      "activa": true,
      "prioridad": 1,
      "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación"
    },
    {
      "id": 2,
      "nombre": "Máximo 3 reprogramaciones",
      "tipo_regla": "LIMITE_REPROGRAMACIONES",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 3,
      "activa": true,
      "prioridad": 2,
      "mensaje_error": "Ha alcanzado el límite máximo de reprogramaciones"
    },
    {
      "id": 3,
      "nombre": "Sin fines de semana",
      "tipo_regla": "DIA_BLACKOUT",
      "aplicable_a": "TODOS",
      "valor_texto": "SABADO,DOMINGO",
      "activa": true,
      "prioridad": 3,
      "mensaje_error": "No se permite reprogramar para fines de semana"
    },
    {
      "id": 4,
      "nombre": "Costo adicional cliente",
      "tipo_regla": "COSTO_REPROGRAMACION",
      "aplicable_a": "CLIENTE",
      "valor_decimal": "50.00",
      "activa": true,
      "prioridad": 4,
      "mensaje_error": "Reprogramación tiene costo adicional de 50 Bs"
    },
    {
      "id": 5,
      "nombre": "Horario comercial",
      "tipo_regla": "HORARIO_PERMITIDO",
      "aplicable_a": "TODOS",
      "valor_texto": "08:00-18:00",
      "activa": true,
      "prioridad": 5,
      "mensaje_error": "Solo se permiten reservas en horario comercial (8:00-18:00)"
    }
  ]
}
```

### 📝 **Crear Nueva Regla (Admin)**
```json
{
  "nombre": "Tiempo mínimo operadores",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "OPERADOR",
  "valor_numerico": 12,
  "activa": true,
  "prioridad": 6,
  "mensaje_error": "Operadores deben reprogramar con al menos 12 horas de anticipación",
  "fecha_inicio_vigencia": "2025-10-01T00:00:00Z",
  "condiciones_extras": {
    "solo_dias_laborales": true,
    "excluir_feriados": true
  }
}
```

---

## 🔄 **FLUJOS DE TRABAJO**

### 🎯 **Flujo 1: Cliente Reprograma**
```javascript
// 1. Verificar si puede reprogramar
const verificacion = await fetch(`/api/reservas/${reservaId}/puede-reprogramar/`, {
  headers: getAuthHeaders()
});
const puedeReprogramar = await verificacion.json();

if (!puedeReprogramar.puede_reprogramar) {
  mostrarError(puedeReprogramar.razon);
  return;
}

// 2. Reprogramar
const payload = {
  nueva_fecha: "2025-11-25T14:30:00Z",
  motivo: "Motivo del cliente"
};

const reprogramacion = await fetch(`/api/reservas/${reservaId}/reprogramar/`, {
  method: 'POST',
  headers: getAuthHeaders(),
  body: JSON.stringify(payload)
});

if (reprogramacion.ok) {
  const resultado = await reprogramacion.json();
  mostrarExito("Reserva reprogramada exitosamente");
  actualizarUI(resultado);
}
```

### 🎯 **Flujo 2: Validación Previa**
```javascript
const validarReprogramacion = async (reservaId, nuevaFecha) => {
  try {
    // Obtener reglas aplicables
    const reglas = await fetch('/api/reglas-reprogramacion/?activa=true');
    const reglasData = await reglas.json();
    
    // Verificar disponibilidad
    const verificacion = await fetch(`/api/reservas/${reservaId}/puede-reprogramar/`);
    const verificacionData = await verificacion.json();
    
    // Validar en frontend antes de enviar
    const errores = [];
    
    // Validar tiempo mínimo
    const tiempoMinimo = reglasData.results.find(r => r.tipo_regla === 'TIEMPO_MINIMO');
    if (tiempoMinimo) {
      const horasHastaNuevaFecha = (new Date(nuevaFecha) - new Date()) / (1000 * 60 * 60);
      if (horasHastaNuevaFecha < tiempoMinimo.valor_numerico) {
        errores.push(`Debe reprogramar con al menos ${tiempoMinimo.valor_numerico} horas de anticipación`);
      }
    }
    
    // Validar día de la semana
    const diaBlackout = reglasData.results.find(r => r.tipo_regla === 'DIA_BLACKOUT');
    if (diaBlackout) {
      const diaSemana = new Date(nuevaFecha).toLocaleDateString('es', { weekday: 'long' }).toUpperCase();
      const diasNoPermitidos = diaBlackout.valor_texto.split(',');
      if (diasNoPermitidos.includes(diaSemana)) {
        errores.push(diaBlackout.mensaje_error);
      }
    }
    
    return {
      valido: errores.length === 0,
      errores: errores,
      reglas_aplicadas: reglasData.results.filter(r => r.activa)
    };
    
  } catch (error) {
    return {
      valido: false,
      errores: ['Error al validar reprogramación'],
      error: error.message
    };
  }
};
```

---

## 🎨 **COMPONENTES UI RECOMENDADOS**

### 📅 **Selector de Fecha con Validación**
```javascript
const ReprogramacionForm = ({ reserva, onSuccess }) => {
  const [nuevaFecha, setNuevaFecha] = useState('');
  const [motivo, setMotivo] = useState('');
  const [validacion, setValidacion] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const validarFecha = async (fecha) => {
    if (!fecha) return;
    
    setLoading(true);
    const resultado = await validarReprogramacion(reserva.id, fecha);
    setValidacion(resultado);
    setLoading(false);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validacion?.valido) {
      return;
    }
    
    try {
      const response = await fetch(`/api/reservas/${reserva.id}/reprogramar/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          nueva_fecha: nuevaFecha,
          motivo: motivo
        })
      });
      
      if (response.ok) {
        const resultado = await response.json();
        onSuccess(resultado);
      } else {
        const error = await response.json();
        setValidacion({
          valido: false,
          errores: [error.detail || 'Error al reprogramar']
        });
      }
    } catch (error) {
      setValidacion({
        valido: false,
        errores: ['Error de conexión']
      });
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Nueva Fecha:</label>
        <input
          type="datetime-local"
          value={nuevaFecha}
          onChange={(e) => {
            setNuevaFecha(e.target.value);
            validarFecha(e.target.value);
          }}
          required
        />
      </div>
      
      <div>
        <label>Motivo:</label>
        <textarea
          value={motivo}
          onChange={(e) => setMotivo(e.target.value)}
          placeholder="Explique el motivo de la reprogramación"
          required
        />
      </div>
      
      {loading && <div>Validando...</div>}
      
      {validacion && !validacion.valido && (
        <div className="errores">
          {validacion.errores.map((error, index) => (
            <div key={index} className="error">{error}</div>
          ))}
        </div>
      )}
      
      {validacion && validacion.valido && (
        <div className="success">
          ✅ La fecha seleccionada es válida
        </div>
      )}
      
      <button 
        type="submit" 
        disabled={!validacion?.valido || loading}
      >
        Reprogramar Reserva
      </button>
    </form>
  );
};
```

### 📊 **Historial de Reprogramaciones**
```javascript
const HistorialReprogramacion = ({ reservaId }) => {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const cargarHistorial = async () => {
      try {
        const response = await fetch(`/api/reservas/${reservaId}/historial-reprogramacion/`);
        const data = await response.json();
        setHistorial(data);
      } catch (error) {
        console.error('Error cargando historial:', error);
      } finally {
        setLoading(false);
      }
    };
    
    cargarHistorial();
  }, [reservaId]);
  
  if (loading) return <div>Cargando historial...</div>;
  
  return (
    <div className="historial-reprogramacion">
      <h3>Historial de Reprogramaciones</h3>
      {historial.length === 0 ? (
        <p>No hay reprogramaciones para esta reserva.</p>
      ) : (
        <div className="timeline">
          {historial.map((entrada, index) => (
            <div key={entrada.id} className="timeline-item">
              <div className="fecha">
                {new Date(entrada.fecha_reprogramacion).toLocaleString()}
              </div>
              <div className="cambio">
                <strong>De:</strong> {new Date(entrada.fecha_anterior).toLocaleString()}
                <br />
                <strong>A:</strong> {new Date(entrada.fecha_nueva).toLocaleString()}
              </div>
              <div className="motivo">
                <strong>Motivo:</strong> {entrada.motivo}
              </div>
              <div className="usuario">
                <strong>Por:</strong> {entrada.reprogramado_por.first_name} {entrada.reprogramado_por.last_name}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## 🚀 **TESTING Y DEPURACIÓN**

### 🧪 **Casos de Prueba**
```javascript
// Test 1: Reprogramación válida
test('Reprogramación válida de cliente', async () => {
  const payload = {
    nueva_fecha: "2025-12-15T10:00:00Z",
    motivo: "Cambio de planes familiares"
  };
  
  const response = await reprogramarReserva(reservaId, payload);
  expect(response.status).toBe(200);
  expect(response.data.estado).toBe('REPROGRAMADA');
});

// Test 2: Error de tiempo mínimo
test('Error por tiempo mínimo insuficiente', async () => {
  const mañana = new Date();
  mañana.setHours(mañana.getHours() + 12);
  
  const payload = {
    nueva_fecha: mañana.toISOString(),
    motivo: "Urgente"
  };
  
  const response = await reprogramarReserva(reservaId, payload);
  expect(response.status).toBe(400);
  expect(response.data.error_code).toBe('TIEMPO_MINIMO_VIOLADO');
});

// Test 3: Límite de reprogramaciones
test('Error por límite de reprogramaciones excedido', async () => {
  // Crear 3 reprogramaciones previas
  for (let i = 0; i < 3; i++) {
    await reprogramarReserva(reservaId, {
      nueva_fecha: new Date(Date.now() + (i + 1) * 24 * 60 * 60 * 1000).toISOString(),
      motivo: `Reprogramación ${i + 1}`
    });
  }
  
  // Intentar una cuarta reprogramación
  const response = await reprogramarReserva(reservaId, {
    nueva_fecha: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(),
    motivo: "Cuarta reprogramación"
  });
  
  expect(response.status).toBe(400);
  expect(response.data.error_code).toBe('LIMITE_REPROGRAMACIONES_EXCEDIDO');
});
```

---

**✨ ¡Sistema de Reprogramación completamente documentado! ✨**

Esta guía proporciona toda la información necesaria para implementar reprogramaciones en el frontend con validaciones completas, manejo de errores y experiencia de usuario optimizada.