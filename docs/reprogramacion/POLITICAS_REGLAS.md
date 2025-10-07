# 📋 POLÍTICAS Y REGLAS DE REPROGRAMACIÓN

## 🎯 **OVERVIEW DE POLÍTICAS**

Sistema completo de reglas configurables que gobiernan las reprogramaciones de reservas según roles, tiempos y condiciones específicas.

---

## 🏗️ **ARQUITECTURA DE REGLAS**

### 📋 **Tipos de Reglas Disponibles**

| Tipo | Código | Descripción | Valor Usado |
|------|--------|-------------|-------------|
| **Tiempo Mínimo** | `TIEMPO_MINIMO` | Horas mínimas antes de la fecha original | `valor_numerico` |
| **Límite Reprogramaciones** | `LIMITE_REPROGRAMACIONES` | Máximo número de cambios permitidos | `valor_numerico` |
| **Días Prohibidos** | `DIA_BLACKOUT` | Días de la semana no permitidos | `valor_texto` |
| **Costo Reprogramación** | `COSTO_REPROGRAMACION` | Costo adicional por cambio | `valor_decimal` |
| **Horario Permitido** | `HORARIO_PERMITIDO` | Rango de horas permitidas | `valor_texto` |
| **Descuento Máximo** | `DESCUENTO_MAXIMO` | Límite de descuento por reprogramación | `valor_decimal` |
| **Fecha Límite** | `FECHA_LIMITE` | Fecha máxima para reprogramar | `valor_texto` |
| **Temporada Alta** | `TEMPORADA_ALTA` | Restricciones especiales en fechas específicas | `valor_texto` |

### 🎭 **Roles y Aplicabilidad**

| Rol | Código | Descripción |
|-----|--------|-------------|
| **Todos** | `TODOS` | Se aplica a todos los usuarios |
| **Cliente** | `CLIENTE` | Solo para usuarios con rol cliente |
| **Operador** | `OPERADOR` | Solo para operadores |
| **Admin** | `ADMIN` | Solo para administradores |
| **Cliente + Operador** | `CLIENTE_OPERADOR` | Para clientes y operadores |
| **Operador + Admin** | `OPERADOR_ADMIN` | Para operadores y administradores |

---

## ⚙️ **REGLAS POR DEFECTO DEL SISTEMA**

### 🕐 **1. Tiempo Mínimo de Anticipación**

```json
{
  "nombre": "Tiempo mínimo 24 horas",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 24,
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación"
}
```

**Lógica de Validación:**
- Calcula horas entre `fecha_actual` y `fecha_reserva`
- Si `horas_diferencia < valor_numerico` → Rechaza
- Admins pueden usar `bypass_reglas` para omitir

### 📊 **2. Límite de Reprogramaciones**

```json
{
  "nombre": "Máximo 3 reprogramaciones",
  "tipo_regla": "LIMITE_REPROGRAMACIONES", 
  "aplicable_a": "CLIENTE",
  "valor_numerico": 3,
  "activa": true,
  "prioridad": 2,
  "mensaje_error": "Ha alcanzado el límite máximo de reprogramaciones"
}
```

**Lógica de Validación:**
- Verifica `reserva.numero_reprogramaciones`
- Si `numero_reprogramaciones >= valor_numerico` → Rechaza
- Operadores tienen límite más alto (5)

### 📅 **3. Días No Permitidos**

```json
{
  "nombre": "Sin fines de semana",
  "tipo_regla": "DIA_BLACKOUT",
  "aplicable_a": "TODOS",
  "valor_texto": "SABADO,DOMINGO",
  "activa": true,
  "prioridad": 3,
  "mensaje_error": "No se permite reprogramar para fines de semana"
}
```

**Formato valor_texto:**
- Días separados por comas: `"LUNES,MARTES"`
- Fechas específicas: `"2025-12-25,2025-01-01"`
- Rangos: `"2025-12-20:2025-12-30"`

### 💰 **4. Costo de Reprogramación**

```json
{
  "nombre": "Costo adicional cliente",
  "tipo_regla": "COSTO_REPROGRAMACION",
  "aplicable_a": "CLIENTE", 
  "valor_decimal": "50.00",
  "activa": true,
  "prioridad": 4,
  "mensaje_error": "Reprogramación tiene costo adicional de 50 Bs"
}
```

**Lógica de Aplicación:**
- Se suma al total de la reserva
- Operadores pueden exonerar con justificación
- Admins sin costo adicional

### 🕒 **5. Horarios Permitidos**

```json
{
  "nombre": "Horario comercial",
  "tipo_regla": "HORARIO_PERMITIDO",
  "aplicable_a": "TODOS",
  "valor_texto": "08:00-18:00",
  "activa": true,
  "prioridad": 5,
  "mensaje_error": "Solo se permiten reservas en horario comercial (8:00-18:00)"
}
```

**Formato valor_texto:**
- Rango simple: `"08:00-18:00"`
- Múltiples rangos: `"08:00-12:00,14:00-18:00"`
- Diferentes por día: `"L-V:08:00-18:00,S:09:00-15:00"`

---

## 🚀 **REGLAS AVANZADAS**

### 🏖️ **6. Temporada Alta**

```json
{
  "nombre": "Restricciones temporada alta",
  "tipo_regla": "TEMPORADA_ALTA",
  "aplicable_a": "CLIENTE",
  "valor_texto": "2025-12-15:2026-01-15",
  "valor_numerico": 72,
  "activa": true,
  "prioridad": 6,
  "mensaje_error": "En temporada alta requiere 72 horas de anticipación",
  "condiciones_extras": {
    "costo_adicional": 100.00,
    "descuento_maximo": 5.0,
    "requiere_aprobacion": true
  }
}
```

### 🎯 **7. Reglas VIP**

```json
{
  "nombre": "Privilegios VIP",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 12,
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "Clientes VIP pueden reprogramar con solo 12 horas",
  "condiciones_extras": {
    "solo_clientes_vip": true,
    "nivel_minimo": "GOLD",
    "descuento_automatico": 5.0
  }
}
```

### 🏢 **8. Reglas Corporativas**

```json
{
  "nombre": "Clientes corporativos",
  "tipo_regla": "LIMITE_REPROGRAMACIONES",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 10,
  "activa": true,
  "prioridad": 2,
  "mensaje_error": "Límite especial para clientes corporativos",
  "condiciones_extras": {
    "solo_corporativos": true,
    "contrato_activo": true,
    "sin_costo_adicional": true
  }
}
```

---

## 🔧 **CONFIGURACIÓN DINÁMICA**

### 📋 **Crear Regla via API**

```javascript
const crearRegla = async (reglaData) => {
  const response = await fetch('/api/reglas-reprogramacion/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      nombre: reglaData.nombre,
      tipo_regla: reglaData.tipo,
      aplicable_a: reglaData.rol,
      valor_numerico: reglaData.valorNumerico,
      valor_decimal: reglaData.valorDecimal,
      valor_texto: reglaData.valorTexto,
      activa: true,
      prioridad: reglaData.prioridad,
      mensaje_error: reglaData.mensaje,
      fecha_inicio_vigencia: reglaData.fechaInicio,
      fecha_fin_vigencia: reglaData.fechaFin,
      condiciones_extras: reglaData.condicionesExtras
    })
  });
  
  return await response.json();
};
```

### 🔄 **Actualizar Regla Existente**

```javascript
const actualizarRegla = async (reglaId, cambios) => {
  const response = await fetch(`/api/reglas-reprogramacion/${reglaId}/`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(cambios)
  });
  
  return await response.json();
};
```

### ❌ **Desactivar Regla**

```javascript
const desactivarRegla = async (reglaId) => {
  return await actualizarRegla(reglaId, { activa: false });
};
```

---

## 🎯 **VALIDACIÓN DE REGLAS**

### 🔍 **Proceso de Evaluación**

```javascript
const evaluarReglas = async (reserva, nuevaFecha, usuario) => {
  // 1. Obtener reglas aplicables
  const reglas = await obtenerReglasAplicables(usuario.rol);
  
  // 2. Filtrar por vigencia
  const reglasVigentes = reglas.filter(regla => 
    esReglaVigente(regla, new Date())
  );
  
  // 3. Ordenar por prioridad
  const reglasOrdenadas = reglasVigentes.sort((a, b) => 
    a.prioridad - b.prioridad
  );
  
  // 4. Evaluar cada regla
  const resultados = [];
  for (const regla of reglasOrdenadas) {
    const resultado = await evaluarReglaIndividual(
      regla, reserva, nuevaFecha, usuario
    );
    resultados.push(resultado);
    
    // Si una regla crítica falla, detener evaluación
    if (!resultado.cumple && regla.prioridad <= 3) {
      break;
    }
  }
  
  return {
    todas_cumplen: resultados.every(r => r.cumple),
    reglas_evaluadas: resultados,
    reglas_violadas: resultados.filter(r => !r.cumple),
    puede_continuar: resultados.filter(r => !r.cumple).length === 0
  };
};
```

### ⚡ **Evaluación de Regla Individual**

```javascript
const evaluarReglaIndividual = (regla, reserva, nuevaFecha, usuario) => {
  switch (regla.tipo_regla) {
    case 'TIEMPO_MINIMO':
      return evaluarTiempoMinimo(regla, reserva, nuevaFecha);
      
    case 'LIMITE_REPROGRAMACIONES':
      return evaluarLimiteReprogramaciones(regla, reserva);
      
    case 'DIA_BLACKOUT':
      return evaluarDiaBlackout(regla, nuevaFecha);
      
    case 'COSTO_REPROGRAMACION':
      return evaluarCostoReprogramacion(regla, usuario);
      
    case 'HORARIO_PERMITIDO':
      return evaluarHorarioPermitido(regla, nuevaFecha);
      
    case 'TEMPORADA_ALTA':
      return evaluarTemporadaAlta(regla, nuevaFecha, reserva);
      
    default:
      return {
        cumple: true,
        mensaje: 'Regla no implementada'
      };
  }
};
```

---

## 🛡️ **BYPASS DE REGLAS**

### 👨‍💼 **Autorización de Bypass**

```javascript
const aplicarBypass = async (reservaId, reglasABypassear, justificacion, autorizado_por) => {
  const payload = {
    reserva_id: reservaId,
    nueva_fecha: "2025-12-01T10:00:00Z",
    motivo: "Reprogramación con bypass autorizado",
    bypass_reglas: reglasABypassear,
    justificacion_bypass: justificacion,
    autorizado_por: autorizado_por,
    tipo_reprogramacion: "ADMINISTRATIVA"
  };
  
  const response = await fetch('/api/gestion-reprogramacion/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload)
  });
  
  return await response.json();
};
```

### 📋 **Reglas que Permiten Bypass**

| Regla | Admin | Operador | Cliente |
|-------|-------|----------|---------|
| `TIEMPO_MINIMO` | ✅ | ✅* | ❌ |
| `LIMITE_REPROGRAMACIONES` | ✅ | ✅* | ❌ |
| `DIA_BLACKOUT` | ✅ | ❌ | ❌ |
| `COSTO_REPROGRAMACION` | ✅ | ✅* | ❌ |
| `HORARIO_PERMITIDO` | ✅ | ❌ | ❌ |

*Operador requiere justificación y aprobación posterior

---

## 📊 **MÉTRICAS Y ANÁLISIS**

### 📈 **Tracking de Reglas**

```javascript
const obtenerMetricasReglas = async (fechaInicio, fechaFin) => {
  const response = await fetch(
    `/api/reglas-reprogramacion/metricas/?inicio=${fechaInicio}&fin=${fechaFin}`
  );
  
  return await response.json();
  // Retorna:
  // {
  //   reglas_mas_violadas: [...],
  //   bypass_mas_utilizados: [...],
  //   eficiencia_por_regla: {...},
  //   sugerencias_optimizacion: [...]
  // }
};
```

### 🔍 **Análisis de Efectividad**

```json
{
  "periodo": "2025-09-01 a 2025-09-30",
  "total_reprogramaciones": 245,
  "reglas_violadas": {
    "TIEMPO_MINIMO": {
      "violaciones": 89,
      "porcentaje": 36.3,
      "impacto": "ALTO"
    },
    "LIMITE_REPROGRAMACIONES": {
      "violaciones": 34,
      "porcentaje": 13.9,
      "impacto": "MEDIO"
    },
    "DIA_BLACKOUT": {
      "violaciones": 22,
      "porcentaje": 9.0,
      "impacto": "BAJO"
    }
  },
  "bypass_utilizados": {
    "ADMIN": 15,
    "OPERADOR": 8,
    "TOTAL": 23
  },
  "sugerencias": [
    {
      "tipo": "AJUSTE_VALOR",
      "regla": "TIEMPO_MINIMO",
      "sugerencia": "Reducir a 18 horas para clientes VIP",
      "impacto_estimado": "Reducción del 25% en violaciones"
    }
  ]
}
```

---

## 🎨 **INTERFAZ DE GESTIÓN**

### 🛠️ **Panel de Administración**

```javascript
const PanelReglasAdmin = () => {
  const [reglas, setReglas] = useState([]);
  const [editando, setEditando] = useState(null);
  
  const cargarReglas = async () => {
    const response = await fetch('/api/reglas-reprogramacion/');
    const data = await response.json();
    setReglas(data.results);
  };
  
  const toggleRegla = async (reglaId, activa) => {
    await actualizarRegla(reglaId, { activa: !activa });
    cargarReglas();
  };
  
  return (
    <div className="panel-reglas">
      <h2>Gestión de Reglas de Reprogramación</h2>
      
      <div className="acciones">
        <button onClick={() => setEditando('nuevo')}>
          + Nueva Regla
        </button>
      </div>
      
      <table className="tabla-reglas">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Aplicable A</th>
            <th>Valor</th>
            <th>Prioridad</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {reglas.map(regla => (
            <tr key={regla.id}>
              <td>{regla.nombre}</td>
              <td>{regla.tipo_regla}</td>
              <td>{regla.aplicable_a}</td>
              <td>
                {regla.valor_numerico || regla.valor_decimal || regla.valor_texto}
              </td>
              <td>{regla.prioridad}</td>
              <td>
                <button 
                  className={regla.activa ? 'activa' : 'inactiva'}
                  onClick={() => toggleRegla(regla.id, regla.activa)}
                >
                  {regla.activa ? 'Activa' : 'Inactiva'}
                </button>
              </td>
              <td>
                <button onClick={() => setEditando(regla.id)}>
                  Editar
                </button>
                <button onClick={() => duplicarRegla(regla)}>
                  Duplicar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {editando && (
        <ModalEditarRegla 
          reglaId={editando}
          onGuardar={() => {
            setEditando(null);
            cargarReglas();
          }}
          onCancelar={() => setEditando(null)}
        />
      )}
    </div>
  );
};
```

---

## 🔬 **TESTING DE REGLAS**

### 🧪 **Suite de Pruebas**

```javascript
describe('Validación de Reglas de Reprogramación', () => {
  
  test('Regla tiempo mínimo - Cliente', async () => {
    const regla = crearReglaTiempoMinimo(24, 'CLIENTE');
    const fechaCercana = new Date(Date.now() + 12 * 60 * 60 * 1000); // 12 horas
    
    const resultado = await evaluarReglaIndividual(regla, reserva, fechaCercana, clienteUser);
    
    expect(resultado.cumple).toBe(false);
    expect(resultado.mensaje).toContain('24 horas');
  });
  
  test('Bypass de regla - Admin', async () => {
    const payload = {
      nueva_fecha: fechaCercana,
      bypass_reglas: ['TIEMPO_MINIMO'],
      autorizado_por: 'admin@test.com'
    };
    
    const resultado = await reprogramarConBypass(reservaId, payload);
    
    expect(resultado.exito).toBe(true);
    expect(resultado.reglas_bypass).toContain('TIEMPO_MINIMO');
  });
  
  test('Límite reprogramaciones excedido', async () => {
    // Simular reserva con 3 reprogramaciones
    const reservaConLimite = { ...reserva, numero_reprogramaciones: 3 };
    const reglaLimite = crearReglaLimite(3, 'CLIENTE');
    
    const resultado = await evaluarReglaIndividual(reglaLimite, reservaConLimite);
    
    expect(resultado.cumple).toBe(false);
    expect(resultado.mensaje).toContain('límite máximo');
  });
  
});
```

---

**✨ ¡Sistema completo de Políticas y Reglas documentado! ✨**

Esta documentación proporciona una guía completa para entender, configurar y mantener el sistema de reglas de reprogramación con todas sus funcionalidades avanzadas.