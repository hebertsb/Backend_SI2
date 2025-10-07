# 🛠️ DEBUGGING: PROBLEMAS DE RESERVAS

## 🔍 **DIAGNÓSTICO PASO A PASO**

Esta guía te ayuda a identificar exactamente qué está fallando cuando intentas crear una reserva.

---

## 📋 **CHECKLIST RÁPIDO**

### ✅ **Verificaciones Básicas**
```javascript
const verificacionesBasicas = () => {
  // 1. ¿Tienes token de autenticación?
  const token = localStorage.getItem('access_token');
  console.log('🔐 Token:', token ? 'SÍ' : '❌ NO');
  
  // 2. ¿El servidor está corriendo?
  fetch('http://localhost:8000/api/')
    .then(r => console.log('🌐 Servidor:', r.ok ? 'SÍ' : '❌ NO'))
    .catch(() => console.log('🌐 Servidor: ❌ NO'));
  
  // 3. ¿Puedes acceder a otros endpoints?
  fetch('http://localhost:8000/api/servicios/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
    .then(r => console.log('📋 Servicios:', r.ok ? 'SÍ' : '❌ NO'))
    .catch(() => console.log('📋 Servicios: ❌ NO'));
};

verificacionesBasicas();
```

---

## 🔍 **MÉTODO 1: DEBUGGING CON CURL**

### 🖥️ **Prueba desde Terminal**
```bash
# 1. Obtener token (si no lo tienes)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tu_usuario","password":"tu_password"}'

# 2. Probar crear reserva mínima
curl -X POST http://localhost:8000/api/reservas/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio": "2025-12-01T10:00:00Z",
    "estado": "PENDIENTE", 
    "total": "500.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 1,
        "cantidad": 1,
        "precio_unitario": "500.00",
        "fecha_servicio": "2025-12-01T10:00:00Z"
      }
    ]
  }'

# 3. Verificar servicios disponibles
curl -X GET http://localhost:8000/api/servicios/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## 🔍 **MÉTODO 2: DEBUGGING EN NAVEGADOR**

### 🌐 **Consola del Navegador**
```javascript
// PEGA ESTO EN LA CONSOLA DEL NAVEGADOR

// 1. Verificar token
const token = localStorage.getItem('access_token');
console.log('🔐 Token disponible:', !!token);
if (token) {
  console.log('Token:', token.substring(0, 20) + '...');
}

// 2. Probar servicios
const probarServicios = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/servicios/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    console.log('📋 Servicios Status:', response.status);
    const servicios = await response.json();
    console.log('📋 Servicios:', servicios);
    return servicios;
  } catch (error) {
    console.error('❌ Error servicios:', error);
  }
};

probarServicios();

// 3. Probar reserva mínima
const probarReservaMinima = async () => {
  const payload = {
    "fecha_inicio": "2025-12-01T10:00:00Z",
    "estado": "PENDIENTE",
    "total": "500.00", 
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": 1,  // ⚠️ Cambiar por ID real
        "cantidad": 1,
        "precio_unitario": "500.00",
        "fecha_servicio": "2025-12-01T10:00:00Z"
      }
    ]
  };

  try {
    console.log('📤 Enviando payload:', payload);
    
    const response = await fetch('http://localhost:8000/api/reservas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    console.log('📥 Response Status:', response.status);
    console.log('📥 Response Headers:', [...response.headers.entries()]);
    
    const data = await response.json();
    console.log('📥 Response Data:', data);
    
    return { response, data };
  } catch (error) {
    console.error('❌ Error en petición:', error);
  }
};

probarReservaMinima();
```

---

## 🔍 **MÉTODO 3: DEBUGGING DEL BACKEND**

### 🐍 **En tu Terminal Django**
```bash
# Verificar desde Django shell
python manage.py shell

# En la shell de Django:
```

```python
# Verificar modelos
from reservas.models import Reserva, ReservaDetalle
from catalogo.models import Servicio
from authz.models import Usuario

# 1. Verificar servicios disponibles
servicios = Servicio.objects.all()
print("Servicios disponibles:")
for s in servicios:
    print(f"- ID: {s.id}, Nombre: {s.nombre}, Precio: {s.precio}")

# 2. Verificar usuarios
usuarios = Usuario.objects.all()
print(f"\nUsuarios: {usuarios.count()}")

# 3. Crear reserva manualmente para probar
usuario = Usuario.objects.first()
servicio = Servicio.objects.first()

if usuario and servicio:
    reserva = Reserva.objects.create(
        usuario=usuario,
        fecha_inicio="2025-12-01 10:00:00",
        estado="PENDIENTE",
        total=500.00,
        moneda="BOB"
    )
    
    detalle = ReservaDetalle.objects.create(
        reserva=reserva,
        servicio=servicio,
        cantidad=1,
        precio_unitario=500.00,
        fecha_servicio="2025-12-01 10:00:00"
    )
    
    print(f"✅ Reserva creada: {reserva.id}")
else:
    print("❌ No hay usuarios o servicios")
```

---

## 🔍 **MÉTODO 4: VERIFICAR LOGS DEL SERVIDOR**

### 📝 **En la consola donde corre Django**
```bash
# Correr Django con debug detallado
python manage.py runserver --verbosity=2

# O con logging específico en settings.py:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 🔍 **MÉTODO 5: PAYLOADS DE PRUEBA GARANTIZADOS**

### ✅ **Estos SIEMPRE funcionan (si el backend está bien)**

```javascript
// RESERVA ULTRA MÍNIMA
const payloadMinimo = {
  "fecha_inicio": "2025-12-01T10:00:00Z",
  "estado": "PENDIENTE",
  "total": "100.00",
  "moneda": "BOB",
  "detalles": [
    {
      "servicio": 1,
      "cantidad": 1, 
      "precio_unitario": "100.00",
      "fecha_servicio": "2025-12-01T10:00:00Z"
    }
  ]
};

// RESERVA CON ACOMPAÑANTE SIMPLE
const payloadConAcompanante = {
  "fecha_inicio": "2025-12-01T10:00:00Z",
  "estado": "PENDIENTE",
  "total": "200.00",
  "moneda": "BOB",
  "detalles": [
    {
      "servicio": 1,
      "cantidad": 1,
      "precio_unitario": "200.00", 
      "fecha_servicio": "2025-12-01T10:00:00Z"
    }
  ],
  "acompanantes": [
    {
      "acompanante": {
        "documento": "TEST123",
        "nombre": "Test",
        "apellido": "Usuario",
        "fecha_nacimiento": "1990-01-01",
        "nacionalidad": "Boliviana",
        "email": "test@test.com"
      },
      "estado": "CONFIRMADO",
      "es_titular": true
    }
  ]
};
```

---

## 🚨 **ERRORES COMUNES Y SOLUCIONES**

### ❌ **Error: "servicio matching query does not exist"**
**Causa:** El ID del servicio no existe
**Solución:**
```javascript
// Obtener IDs reales
fetch('http://localhost:8000/api/servicios/')
  .then(r => r.json())
  .then(data => {
    console.log('IDs disponibles:', data.results?.map(s => s.id));
  });
```

### ❌ **Error: "fecha_inicio - Este campo es requerido"**
**Causa:** Formato de fecha incorrecto
**Solución:**
```javascript
// Formato correcto ISO 8601
const fecha = new Date();
fecha.setDate(fecha.getDate() + 7); // 7 días en el futuro
const fechaISO = fecha.toISOString();
console.log('Fecha correcta:', fechaISO);
```

### ❌ **Error: "Usuario no encontrado" o 401 Unauthorized**
**Causa:** Token inválido o expirado
**Solución:**
```javascript
// Renovar token
const renovarToken = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh })
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
};
```

### ❌ **Error: "Total debe ser mayor a 0"**
**Causa:** Formato numérico incorrecto
**Solución:**
```javascript
// Siempre como string con decimales
const total = parseFloat(totalCalculado).toFixed(2);
payload.total = total;
```

---

## 🎯 **HERRAMIENTA DE DIAGNÓSTICO AUTOMÁTICO**

```javascript
const diagnosticoCompleto = async () => {
  console.log('🔍 INICIANDO DIAGNÓSTICO COMPLETO...\n');
  
  // 1. Token
  const token = localStorage.getItem('access_token');
  console.log('🔐 Token:', token ? '✅ Presente' : '❌ Ausente');
  
  // 2. Conectividad
  try {
    const pingResponse = await fetch('http://localhost:8000/api/');
    console.log('🌐 Servidor:', pingResponse.ok ? '✅ Activo' : '❌ Error');
  } catch {
    console.log('🌐 Servidor: ❌ No responde');
    return;
  }
  
  // 3. Autenticación
  try {
    const authResponse = await fetch('http://localhost:8000/api/servicios/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    console.log('🔐 Auth:', authResponse.ok ? '✅ Válida' : '❌ Inválida');
  } catch {
    console.log('🔐 Auth: ❌ Error');
  }
  
  // 4. Servicios disponibles
  try {
    const serviciosResponse = await fetch('http://localhost:8000/api/servicios/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const servicios = await serviciosResponse.json();
    const ids = servicios.results?.map(s => s.id) || [];
    console.log('📋 Servicios disponibles:', ids.length > 0 ? `✅ ${ids}` : '❌ Ninguno');
  } catch {
    console.log('📋 Servicios: ❌ Error');
  }
  
  // 5. Prueba de reserva
  const servicioTest = 1; // Cambiar por ID real
  const payloadTest = {
    "fecha_inicio": "2025-12-01T10:00:00Z",
    "estado": "PENDIENTE",
    "total": "100.00",
    "moneda": "BOB",
    "detalles": [
      {
        "servicio": servicioTest,
        "cantidad": 1,
        "precio_unitario": "100.00",
        "fecha_servicio": "2025-12-01T10:00:00Z"
      }
    ]
  };
  
  try {
    const reservaResponse = await fetch('http://localhost:8000/api/reservas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payloadTest)
    });
    
    console.log('🎯 Reserva test:', reservaResponse.ok ? '✅ Funciona' : `❌ Error ${reservaResponse.status}`);
    
    if (!reservaResponse.ok) {
      const error = await reservaResponse.json();
      console.log('❌ Detalles del error:', error);
    }
  } catch (error) {
    console.log('🎯 Reserva test: ❌ Error de red');
  }
  
  console.log('\n🔍 DIAGNÓSTICO COMPLETADO');
};

// Ejecutar diagnóstico
diagnosticoCompleto();
```

---

**🎯 Ejecuta estas herramientas de debugging y comparte los resultados para ayudarte a solucionar el problema específico.**