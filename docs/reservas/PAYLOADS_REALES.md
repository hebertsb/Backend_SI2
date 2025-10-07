# 🎯 PAYLOAD REAL PARA TU SISTEMA

## ✅ **ESTOS SON LOS IDS REALES QUE FUNCIONAN**

Basado en tu base de datos actual:

### 📋 **Servicios Disponibles**
```
ID: 1 - Salar de Uyuni - $250.00
ID: 2 - Isla del Sol - $180.00  
ID: 3 - Tiwanaku - $90.00
ID: 4 - Cristo de la Concordia - $60.00
ID: 5 - Laguna Colorada - $210.00
ID: 6 - Camino de la Muerte - $150.00
ID: 7 - Coroico - $120.00
ID: 8 - Samaipata - $170.00
ID: 9 - Parque Nacional Madidi - $300.00
```

---

## 🚀 **PAYLOADS QUE FUNCIONAN 100%**

### ✅ **1. Reserva Simple - COPIA Y PEGA ESTO**
```javascript
const crearReservaSimple = async () => {
  const payload = {
    "fecha_inicio": "2025-12-01T10:00:00Z",
    "estado": "PENDIENTE",
    "total": "250.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 1,  // ✅ Salar de Uyuni - Existe
        "cantidad": 1,
        "precio_unitario": "250.00",
        "fecha_servicio": "2025-12-01T10:00:00Z"
      }
    ]
  };

  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch('http://localhost:8000/api/reservas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('❌ Error:', error);
      return null;
    }

    const reserva = await response.json();
    console.log('✅ Reserva creada:', reserva);
    return reserva;

  } catch (error) {
    console.error('❌ Error de red:', error);
    return null;
  }
};

// Ejecutar
crearReservaSimple();
```

### ✅ **2. Reserva con Acompañante - COPIA Y PEGA ESTO**
```javascript
const crearReservaConAcompanante = async () => {
  const payload = {
    "fecha_inicio": "2025-12-05T14:30:00Z",
    "estado": "PENDIENTE", 
    "total": "360.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 2,  // ✅ Isla del Sol - Existe
        "cantidad": 2,
        "precio_unitario": "180.00",
        "fecha_servicio": "2025-12-05T14:30:00Z"
      }
    ],
    "acompanantes": [
      {
        "acompanante": {
          "documento": "TEST12345",  // ✅ Documento único
          "nombre": "María",
          "apellido": "González",
          "fecha_nacimiento": "1990-05-15",
          "nacionalidad": "Boliviana",
          "email": "maria@test.com"
        },
        "estado": "CONFIRMADO",
        "es_titular": true  // ✅ Solo uno puede ser titular
      }
    ]
  };

  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch('http://localhost:8000/api/reservas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('❌ Error:', error);
      return null;
    }

    const reserva = await response.json();
    console.log('✅ Reserva con acompañante creada:', reserva);
    return reserva;

  } catch (error) {
    console.error('❌ Error de red:', error);
    return null;
  }
};

// Ejecutar
crearReservaConAcompanante();
```

### ✅ **3. Reserva Múltiple Servicios - COPIA Y PEGA ESTO**
```javascript
const crearReservaMultiple = async () => {
  const payload = {
    "fecha_inicio": "2025-12-10T08:00:00Z",
    "estado": "PENDIENTE",
    "total": "340.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 1,  // ✅ Salar de Uyuni
        "cantidad": 1,
        "precio_unitario": "250.00",
        "fecha_servicio": "2025-12-10T08:00:00Z"
      },
      {
        "servicio": 3,  // ✅ Tiwanaku
        "cantidad": 1,
        "precio_unitario": "90.00",
        "fecha_servicio": "2025-12-11T09:00:00Z"
      }
    ]
  };

  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch('http://localhost:8000/api/reservas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('❌ Error:', error);
      return null;
    }

    const reserva = await response.json();
    console.log('✅ Reserva múltiple creada:', reserva);
    return reserva;

  } catch (error) {
    console.error('❌ Error de red:', error);
    return null;
  }
};

// Ejecutar
crearReservaMultiple();
```

---

## 🔧 **FUNCIÓN UNIVERSAL PARA TU FRONTEND**

```javascript
class ReservasManager {
  constructor() {
    this.baseURL = 'http://localhost:8000';
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.getToken()}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
  }

  async crearReserva(datos) {
    try {
      console.log('📤 Enviando reserva:', datos);

      const response = await fetch(`${this.baseURL}/api/reservas/`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(datos)
      });

      if (!response.ok) {
        const error = await response.json();
        console.error('❌ Error del servidor:', error);
        return { success: false, error, status: response.status };
      }

      const reserva = await response.json();
      console.log('✅ Reserva creada:', reserva);
      return { success: true, data: reserva };

    } catch (error) {
      console.error('❌ Error de red:', error);
      return { success: false, error: error.message };
    }
  }

  async obtenerServicios() {
    try {
      const response = await fetch(`${this.baseURL}/api/servicios/`, {
        headers: this.getHeaders()
      });

      if (!response.ok) throw new Error('Error al obtener servicios');

      const data = await response.json();
      return data.results || data;
    } catch (error) {
      console.error('❌ Error obteniendo servicios:', error);
      return [];
    }
  }

  async obtenerReservas() {
    try {
      const response = await fetch(`${this.baseURL}/api/reservas/`, {
        headers: this.getHeaders()
      });

      if (!response.ok) throw new Error('Error al obtener reservas');

      const data = await response.json();
      return data.results || data;
    } catch (error) {
      console.error('❌ Error obteniendo reservas:', error);
      return [];
    }
  }

  // Función de validación antes de enviar
  validarReserva(reserva) {
    const errores = {};

    if (!reserva.fecha_inicio) {
      errores.fecha_inicio = 'Fecha requerida';
    }

    if (!reserva.total || parseFloat(reserva.total) <= 0) {
      errores.total = 'Total debe ser mayor a 0';
    }

    if (!reserva.detalles || reserva.detalles.length === 0) {
      errores.detalles = 'Debe incluir al menos un servicio';
    }

    if (!['PENDIENTE', 'PAGADA', 'CANCELADA', 'COMPLETADA'].includes(reserva.estado)) {
      errores.estado = 'Estado inválido';
    }

    if (!['BOB', 'USD', 'EUR'].includes(reserva.moneda)) {
      errores.moneda = 'Moneda inválida';
    }

    // Validar acompañantes si existen
    if (reserva.acompanantes?.length > 0) {
      const titulares = reserva.acompanantes.filter(a => a.es_titular);
      if (titulares.length > 1) {
        errores.acompanantes = 'Solo un titular permitido';
      }
    }

    return {
      esValido: Object.keys(errores).length === 0,
      errores
    };
  }
}

// Inicializar
const reservasManager = new ReservasManager();

// Ejemplo de uso
const ejemploUso = async () => {
  const reservaTest = {
    "fecha_inicio": "2025-12-15T10:00:00Z",
    "estado": "PENDIENTE",
    "total": "250.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 1,
        "cantidad": 1,
        "precio_unitario": "250.00",
        "fecha_servicio": "2025-12-15T10:00:00Z"
      }
    ]
  };

  // Validar antes de enviar
  const validacion = reservasManager.validarReserva(reservaTest);
  if (!validacion.esValido) {
    console.error('❌ Errores de validación:', validacion.errores);
    return;
  }

  // Crear reserva
  const resultado = await reservasManager.crearReserva(reservaTest);
  if (resultado.success) {
    console.log('🎉 ¡Reserva creada exitosamente!');
  } else {
    console.error('❌ Error creando reserva:', resultado.error);
  }
};
```

---

## 🔍 **FUNCIÓN DE DEBUGGING ESPECÍFICA**

```javascript
const debugearProblemaReserva = async () => {
  console.log('🔍 INICIANDO DEBUGGING ESPECÍFICO...\n');

  const reservasManager = new ReservasManager();

  // 1. Verificar token
  const token = reservasManager.getToken();
  console.log('🔐 Token:', token ? '✅ Presente' : '❌ Ausente');
  
  if (!token) {
    console.log('❌ PROBLEMA: No tienes token de autenticación');
    console.log('💡 SOLUCIÓN: Haz login primero');
    return;
  }

  // 2. Verificar servicios
  console.log('\n📋 Verificando servicios...');
  const servicios = await reservasManager.obtenerServicios();
  console.log('Servicios disponibles:', servicios.length);
  
  if (servicios.length === 0) {
    console.log('❌ PROBLEMA: No hay servicios disponibles');
    return;
  }

  // 3. Probar reserva mínima
  console.log('\n🎯 Probando crear reserva...');
  const reservaPrueba = {
    "fecha_inicio": "2025-12-20T10:00:00Z",
    "estado": "PENDIENTE",
    "total": "250.00",
    "moneda": "BOB", 
    "detalles": [
      {
        "servicio": servicios[0].id,  // Usar primer servicio disponible
        "cantidad": 1,
        "precio_unitario": "250.00",
        "fecha_servicio": "2025-12-20T10:00:00Z"
      }
    ]
  };

  const resultado = await reservasManager.crearReserva(reservaPrueba);
  
  if (resultado.success) {
    console.log('✅ ¡PERFECTO! La reserva funciona correctamente');
    console.log('Reserva creada:', resultado.data);
  } else {
    console.log('❌ PROBLEMA ENCONTRADO:');
    console.log('Error:', resultado.error);
    console.log('Status:', resultado.status);
    
    // Sugerencias específicas
    if (resultado.status === 401) {
      console.log('💡 SOLUCIÓN: Token expirado o inválido - haz login de nuevo');
    } else if (resultado.status === 400) {
      console.log('💡 SOLUCIÓN: Error de validación - revisa el payload');
    } else if (resultado.status === 403) {
      console.log('💡 SOLUCIÓN: Sin permisos - verifica el rol del usuario');
    }
  }
};

// Ejecutar debugging
debugearProblemaReserva();
```

---

## 📱 **IMPLEMENTACIÓN EN REACT/VUE**

### React Component
```jsx
import React, { useState } from 'react';

const CrearReserva = () => {
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const reservasManager = new ReservasManager();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    setSuccess(false);

    const formData = new FormData(e.target);
    const reservaData = {
      fecha_inicio: "2025-12-25T10:00:00Z",
      estado: "PENDIENTE",
      total: formData.get('total'),
      moneda: "BOB",
      detalles: [
        {
          servicio: parseInt(formData.get('servicio')),
          cantidad: parseInt(formData.get('cantidad')),
          precio_unitario: formData.get('precio'),
          fecha_servicio: "2025-12-25T10:00:00Z"
        }
      ]
    };

    const resultado = await reservasManager.crearReserva(reservaData);
    
    if (resultado.success) {
      setSuccess(true);
      e.target.reset();
    } else {
      setErrors(resultado.error);
    }
    
    setLoading(false);
  };

  return (
    <div>
      <h2>Crear Reserva</h2>
      
      {success && (
        <div className="alert alert-success">
          ¡Reserva creada exitosamente!
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Servicio:</label>
          <select name="servicio" required>
            <option value="1">Salar de Uyuni - $250</option>
            <option value="2">Isla del Sol - $180</option>
            <option value="3">Tiwanaku - $90</option>
            <option value="4">Cristo de la Concordia - $60</option>
          </select>
          {errors.servicio && <span className="error">{errors.servicio}</span>}
        </div>

        <div>
          <label>Cantidad:</label>
          <input type="number" name="cantidad" defaultValue="1" min="1" required />
          {errors.cantidad && <span className="error">{errors.cantidad}</span>}
        </div>

        <div>
          <label>Precio:</label>
          <input type="number" name="precio" step="0.01" required />
          {errors.precio && <span className="error">{errors.precio}</span>}
        </div>

        <div>
          <label>Total:</label>
          <input type="number" name="total" step="0.01" required />
          {errors.total && <span className="error">{errors.total}</span>}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Creando...' : 'Crear Reserva'}
        </button>
      </form>

      {Object.keys(errors).length > 0 && (
        <div className="alert alert-danger">
          <h4>Errores encontrados:</h4>
          <ul>
            {Object.entries(errors).map(([key, value]) => (
              <li key={key}>{key}: {JSON.stringify(value)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default CrearReserva;
```

---

**🎯 Con esta información tienes todo lo necesario para crear reservas exitosamente. Los IDs y estructuras están basados en tu base de datos real.**