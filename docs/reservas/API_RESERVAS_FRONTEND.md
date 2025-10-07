# 📋 API RESERVAS - Guía Completa para Frontend

## 🎯 **INFORMACIÓN GENERAL**

Esta documentación cubre todo el sistema de reservas incluyendo acompañantes, servicios y gestión completa. El sistema maneja reservas con múltiples servicios y acompañantes asociados.

### 🗂️ **MODELOS PRINCIPALES**

1. **Reserva** - Reserva principal
2. **ReservaServicio** - Servicios incluidos en la reserva
3. **Acompañante** - Datos personales de acompañantes
4. **ReservaAcompañante** - Relación entre reserva y acompañantes

---

## 📊 **ENDPOINTS DISPONIBLES**

### 🏠 **Base URL:** `http://localhost:8000/api/reservas/`

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/reservas/` | GET, POST | Listar y crear reservas |
| `/reservas/{id}/` | GET, PUT, PATCH, DELETE | CRUD de reserva específica |
| `/reservas/{id}/reprogramar/` | POST | Reprogramar reserva |
| `/acompanantes/` | GET, POST | CRUD de acompañantes |
| `/acompanantes/{id}/` | GET, PUT, PATCH, DELETE | CRUD de acompañante específico |
| `/reserva-acompanantes/` | GET, POST | Asociar acompañantes a reservas |

---

## 🔐 **AUTENTICACIÓN**

Todos los endpoints requieren autenticación Bearer Token:

```javascript
headers: {
  'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'Content-Type': 'application/json'
}
```

---

## 📝 **ESQUEMAS DE DATOS**

### 1️⃣ **Reserva**

```json
{
  "id": 1,
  "usuario": 14,
  "fecha_inicio": "2025-09-25T14:30:00Z",
  "estado": "PENDIENTE",
  "cupon": null,
  "total": "1500.00",
  "moneda": "BOB",
  "fecha_original": null,
  "fecha_reprogramacion": null,
  "motivo_reprogramacion": null,
  "numero_reprogramaciones": 0,
  "reprogramado_por": null,
  "created_at": "2025-09-20T10:00:00Z",
  "updated_at": "2025-09-20T10:00:00Z",
  "detalles": [
    {
      "id": 1,
      "servicio": 5,
      "cantidad": 2,
      "precio_unitario": "750.00",
      "fecha_servicio": "2025-09-25T14:30:00Z"
    }
  ],
  "acompanantes": [
    {
      "id": 1,
      "acompanante": {
        "id": 10,
        "documento": "12345678",
        "nombre": "Juan",
        "apellido": "Pérez",
        "fecha_nacimiento": "1990-05-15",
        "nacionalidad": "Boliviana",
        "email": "juan@email.com",
        "telefono": "+591 70123456"
      },
      "estado": "CONFIRMADO",
      "es_titular": true
    }
  ]
}
```

### 2️⃣ **Acompañante**

```json
{
  "id": 1,
  "documento": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "fecha_nacimiento": "1990-05-15",
  "nacionalidad": "Boliviana",
  "email": "juan@email.com",
  "telefono": "+591 70123456",
  "created_at": "2025-09-20T10:00:00Z",
  "updated_at": "2025-09-20T10:00:00Z"
}
```

### 3️⃣ **Estados de Reserva**

- `PENDIENTE` - Reserva creada, pendiente de pago
- `PAGADA` - Reserva confirmada y pagada
- `CANCELADA` - Reserva cancelada
- `REPROGRAMADA` - Reserva reprogramada

---

## 🚀 **EJEMPLOS DE USO**

### 📋 **1. LISTAR RESERVAS**

```javascript
// GET /api/reservas/
const response = await fetch('http://localhost:8000/api/reservas/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

const reservas = await response.json();
```

**Respuesta:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/reservas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "usuario": 14,
      "fecha_inicio": "2025-09-25T14:30:00Z",
      "estado": "PENDIENTE",
      "total": "1500.00",
      "moneda": "BOB",
      "numero_reprogramaciones": 0,
      "created_at": "2025-09-20T10:00:00Z"
    }
  ]
}
```

### ➕ **2. CREAR RESERVA COMPLETA CON ACOMPAÑANTES**

```javascript
// POST /api/reservas/
const nuevaReserva = {
  "fecha_inicio": "2025-10-15T09:00:00Z",
  "estado": "PENDIENTE",
  "cupon": null,
  "total": "2400.00",
  "moneda": "BOB",
  "detalles": [
    {
      "servicio": 3,
      "cantidad": 2,
      "precio_unitario": "800.00",
      "fecha_servicio": "2025-10-15T09:00:00Z"
    },
    {
      "servicio": 7,
      "cantidad": 1,
      "precio_unitario": "800.00",
      "fecha_servicio": "2025-10-15T14:00:00Z"
    }
  ],
  "acompanantes": [
    {
      "acompanante": {
        "documento": "87654321",
        "nombre": "María",
        "apellido": "González",
        "fecha_nacimiento": "1985-03-20",
        "nacionalidad": "Boliviana",
        "email": "maria@email.com",
        "telefono": "+591 78901234"
      },
      "estado": "CONFIRMADO",
      "es_titular": true
    },
    {
      "acompanante": {
        "documento": "11223344",
        "nombre": "Carlos",
        "apellido": "Ramírez",
        "fecha_nacimiento": "1992-08-10",
        "nacionalidad": "Boliviana",
        "email": "carlos@email.com",
        "telefono": "+591 65432109"
      },
      "estado": "CONFIRMADO",
      "es_titular": false
    }
  ]
};

const response = await fetch('http://localhost:8000/api/reservas/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(nuevaReserva)
});

const reservaCreada = await response.json();
```

### 📄 **3. OBTENER RESERVA ESPECÍFICA**

```javascript
// GET /api/reservas/1/
const response = await fetch('http://localhost:8000/api/reservas/1/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

const reserva = await response.json();
```

### ✏️ **4. ACTUALIZAR RESERVA**

```javascript
// PATCH /api/reservas/1/
const datosActualizar = {
  "estado": "PAGADA",
  "total": "2500.00"
};

const response = await fetch('http://localhost:8000/api/reservas/1/', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(datosActualizar)
});

const reservaActualizada = await response.json();
```

### 🗑️ **5. ELIMINAR RESERVA**

```javascript
// DELETE /api/reservas/1/
const response = await fetch('http://localhost:8000/api/reservas/1/', {
  method: 'DELETE',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

// Respuesta: 204 No Content
```

---

## 👥 **GESTIÓN DE ACOMPAÑANTES**

### ➕ **CREAR ACOMPAÑANTE**

```javascript
// POST /api/acompanantes/
const nuevoAcompanante = {
  "documento": "98765432",
  "nombre": "Ana",
  "apellido": "López",
  "fecha_nacimiento": "1988-12-05",
  "nacionalidad": "Peruana",
  "email": "ana@email.com",
  "telefono": "+591 76543210"
};

const response = await fetch('http://localhost:8000/api/acompanantes/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(nuevoAcompanante)
});

const acompananteCreado = await response.json();
```

### 🔗 **ASOCIAR ACOMPAÑANTE A RESERVA**

```javascript
// POST /api/reserva-acompanantes/
const asociacion = {
  "reserva": 1,
  "acompanante": 5,
  "estado": "CONFIRMADO",
  "es_titular": false
};

const response = await fetch('http://localhost:8000/api/reserva-acompanantes/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(asociacion)
});
```

---

## 🔍 **FILTROS Y BÚSQUEDAS**

### 🎯 **Filtros Disponibles**

```javascript
// Filtrar por estado
GET /api/reservas/?estado=PENDIENTE

// Filtrar por fecha
GET /api/reservas/?fecha_inicio__gte=2025-09-20

// Filtrar por usuario
GET /api/reservas/?usuario=14

// Buscar por múltiples criterios
GET /api/reservas/?estado=PAGADA&fecha_inicio__gte=2025-09-01&fecha_inicio__lte=2025-12-31

// Ordenar resultados
GET /api/reservas/?ordering=-created_at

// Buscar acompañantes por documento
GET /api/acompanantes/?documento=12345678
```

---

## ⚠️ **VALIDACIONES Y REGLAS**

### 📋 **Validaciones Automáticas**

1. **Documento único** - Cada acompañante debe tener documento único
2. **Un titular por reserva** - Solo puede haber un titular por reserva
3. **Fechas válidas** - fecha_inicio no puede ser en el pasado
4. **Total positivo** - El total debe ser mayor a 0
5. **Servicios válidos** - Los servicios deben existir y estar activos

### 🚫 **Errores Comunes**

```json
{
  "error": "ValidationError",
  "details": {
    "documento": ["Acompañante con este documento ya existe."],
    "fecha_inicio": ["La fecha no puede ser en el pasado."],
    "total": ["El total debe ser mayor a 0."]
  }
}
```

---

## 📱 **CÓDIGOS DE RESPUESTA**

| Código | Descripción |
|--------|-------------|
| 200 | Éxito - Operación completada |
| 201 | Creado - Recurso creado exitosamente |
| 204 | Sin contenido - Eliminación exitosa |
| 400 | Error de validación |
| 401 | No autorizado - Token inválido |
| 404 | No encontrado - Recurso no existe |
| 500 | Error del servidor |

---

## 💡 **CONSEJOS PARA EL FRONTEND**

### 🎨 **Mejores Prácticas**

1. **Manejo de Estados:**
```javascript
const [reservas, setReservas] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
```

2. **Validación en Frontend:**
```javascript
const validarReserva = (reserva) => {
  const errores = {};
  
  if (!reserva.fecha_inicio) {
    errores.fecha_inicio = 'Fecha de inicio requerida';
  }
  
  if (reserva.total <= 0) {
    errores.total = 'El total debe ser mayor a 0';
  }
  
  return errores;
};
```

3. **Formateo de Fechas:**
```javascript
const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleString('es-BO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
```

### 🎯 **Componentes Sugeridos**

1. **ListaReservas** - Tabla con paginación
2. **FormularioReserva** - Formulario de creación/edición
3. **DetalleReserva** - Vista detallada de reserva
4. **GestionAcompanantes** - Gestión de acompañantes
5. **FiltroBusqueda** - Componente de filtros

---

## 🧪 **EJEMPLOS DE TESTING**

### ✅ **Testing con Jest/React Testing Library**

```javascript
describe('Reservas API', () => {
  test('debe crear una reserva correctamente', async () => {
    const nuevaReserva = {
      fecha_inicio: '2025-10-15T09:00:00Z',
      total: '1500.00',
      moneda: 'BOB'
    };
    
    const response = await crearReserva(nuevaReserva);
    
    expect(response.status).toBe(201);
    expect(response.data.total).toBe('1500.00');
  });
  
  test('debe validar campos requeridos', async () => {
    const reservaInvalida = {};
    
    try {
      await crearReserva(reservaInvalida);
    } catch (error) {
      expect(error.response.status).toBe(400);
      expect(error.response.data.fecha_inicio).toBeDefined();
    }
  });
});
```

---

## 📞 **CONTACTO Y SOPORTE**

Para dudas sobre esta API:
- **Email:** soporte@reservas.com
- **Documentación adicional:** `/docs/reservas/`
- **Swagger:** `http://localhost:8000/swagger/`

---

**✨ ¡Sistema de Reservas listo para integración con Frontend! ✨**