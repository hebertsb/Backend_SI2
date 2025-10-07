# 📋 GESTIÓN DE REGLAMENTOS - Sistema de Administración

## 🎯 **OVERVIEW SISTEMA DE REGLAMENTOS**

Sistema completo para administrar, actualizar y mantener todas las reglas y políticas del sistema de reservas de forma dinámica y sin interrupciones.

---

## 🔗 **ENDPOINTS DE ADMINISTRACIÓN**

### 📋 **BASE URL**
```
http://localhost:8000/api/
```

### 🌐 **ENDPOINTS PRINCIPALES**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| `GET` | `/reglas-reprogramacion/` | Listar todas las reglas | Admin, Operador |
| `POST` | `/reglas-reprogramacion/` | Crear nueva regla | Admin |
| `GET` | `/reglas-reprogramacion/{id}/` | Obtener regla específica | Admin, Operador |
| `PUT` | `/reglas-reprogramacion/{id}/` | Actualizar regla completa | Admin |
| `PATCH` | `/reglas-reprogramacion/{id}/` | Actualización parcial | Admin |
| `DELETE` | `/reglas-reprogramacion/{id}/` | Eliminar regla | Admin |
| `POST` | `/reglas-reprogramacion/bulk-update/` | Actualización masiva | Admin |
| `POST` | `/reglas-reprogramacion/import/` | Importar reglas | Admin |
| `GET` | `/reglas-reprogramacion/export/` | Exportar reglas | Admin |
| `POST` | `/reglas-reprogramacion/activate-batch/` | Activar múltiples | Admin |
| `POST` | `/reglas-reprogramacion/validate/` | Validar regla antes de crear | Admin |

---

## 🔐 **AUTENTICACIÓN Y PERMISOS**

### 📋 **Headers Requeridos**
```javascript
{
  "Authorization": "Bearer JWT_TOKEN_ADMIN",
  "Content-Type": "application/json",
  "Accept": "application/json",
  "X-Admin-Role": "ADMIN" // Verificación adicional
}
```

### 🎭 **Matriz de Permisos**

| Acción | Admin | Operador | Cliente |
|--------|-------|----------|---------|
| **Ver reglas** | ✅ | ✅ | ❌ |
| **Crear reglas** | ✅ | ❌ | ❌ |
| **Editar reglas** | ✅ | ❌ | ❌ |
| **Eliminar reglas** | ✅ | ❌ | ❌ |
| **Activar/Desactivar** | ✅ | ❌ | ❌ |
| **Actualización masiva** | ✅ | ❌ | ❌ |
| **Import/Export** | ✅ | ❌ | ❌ |

---

## 📋 **1. GESTIÓN BÁSICA DE REGLAS**

### 🔍 **Listar Todas las Reglas**
```
GET /api/reglas-reprogramacion/
```

### ✅ **Respuesta Completa**
```json
{
  "count": 12,
  "next": "http://localhost:8000/api/reglas-reprogramacion/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "tipo_regla": "TIEMPO_MINIMO",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 24,
      "valor_decimal": null,
      "valor_texto": null,
      "valor_booleano": null,
      "activa": true,
      "prioridad": 1,
      "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación",
      "fecha_inicio_vigencia": "2025-01-01T00:00:00Z",
      "fecha_fin_vigencia": null,
      "condiciones_extras": {
        "solo_dias_laborales": false,
        "excluir_feriados": true
      },
      "created_at": "2025-09-01T00:00:00Z",
      "updated_at": "2025-09-15T10:30:00Z",
      "creado_por": {
        "id": 1,
        "username": "admin@sistema.com",
        "first_name": "Admin",
        "last_name": "Sistema"
      },
      "estadisticas_uso": {
        "total_aplicaciones": 245,
        "violaciones_mes_actual": 34,
        "eficiencia_porcentaje": 86.1
      }
    },
    {
      "id": 2,
      "nombre": "Máximo reprogramaciones VIP",
      "tipo_regla": "LIMITE_REPROGRAMACIONES",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 5,
      "activa": true,
      "prioridad": 2,
      "mensaje_error": "Clientes VIP pueden realizar hasta 5 reprogramaciones",
      "condiciones_extras": {
        "solo_clientes_vip": true,
        "nivel_minimo": "GOLD"
      },
      "created_at": "2025-09-10T14:20:00Z",
      "updated_at": "2025-09-10T14:20:00Z"
    }
  ]
}
```

### 🔍 **Filtros Avanzados**
```
GET /api/reglas-reprogramacion/?activa=true&tipo_regla=TIEMPO_MINIMO&aplicable_a=CLIENTE&ordering=-prioridad
```

### 🔍 **Búsqueda por Texto**
```
GET /api/reglas-reprogramacion/?search=tiempo minimo&activa=true
```

---

## ➕ **2. CREAR NUEVA REGLA**

### 🎯 **Endpoint**
```
POST /api/reglas-reprogramacion/
```

### 📝 **Payload Básico**
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
    "excluir_feriados": true,
    "requiere_justificacion": false
  }
}
```

### 📝 **Payload Avanzado con Condiciones**
```json
{
  "nombre": "Regla temporada navideña",
  "tipo_regla": "TEMPORADA_ESPECIAL",
  "aplicable_a": "TODOS",
  "valor_texto": "2025-12-15:2026-01-15",
  "valor_numerico": 72,
  "valor_decimal": "25.00",
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "En temporada navideña se requiere 72 horas de anticipación",
  "fecha_inicio_vigencia": "2025-12-01T00:00:00Z",
  "fecha_fin_vigencia": "2026-01-31T23:59:59Z",
  "condiciones_extras": {
    "costo_adicional": 25.00,
    "descuento_maximo": 10.0,
    "requiere_aprobacion_gerencia": true,
    "notificacion_especial": true,
    "dias_especiales": ["2025-12-24", "2025-12-25", "2025-12-31", "2026-01-01"],
    "horarios_restringidos": "09:00-17:00",
    "capacidad_reducida": 0.7
  }
}
```

### ✅ **Respuesta Exitosa (201)**
```json
{
  "id": 13,
  "nombre": "Regla temporada navideña",
  "tipo_regla": "TEMPORADA_ESPECIAL",
  "aplicable_a": "TODOS",
  "valor_texto": "2025-12-15:2026-01-15",
  "valor_numerico": 72,
  "valor_decimal": "25.00",
  "activa": true,
  "prioridad": 1,
  "mensaje_error": "En temporada navideña se requiere 72 horas de anticipación",
  "fecha_inicio_vigencia": "2025-12-01T00:00:00Z",
  "fecha_fin_vigencia": "2026-01-31T23:59:59Z",
  "condiciones_extras": {
    "costo_adicional": 25.00,
    "descuento_maximo": 10.0,
    "requiere_aprobacion_gerencia": true,
    "notificacion_especial": true,
    "dias_especiales": ["2025-12-24", "2025-12-25", "2025-12-31", "2026-01-01"],
    "horarios_restringidos": "09:00-17:00",
    "capacidad_reducida": 0.7
  },
  "created_at": "2025-09-20T15:30:00Z",
  "updated_at": "2025-09-20T15:30:00Z",
  "creado_por": {
    "id": 1,
    "username": "admin@sistema.com",
    "first_name": "Admin",
    "last_name": "Sistema"
  },
  "validacion_resultado": {
    "conflictos_encontrados": false,
    "reglas_similares": [],
    "impacto_estimado": "MEDIO",
    "reservas_afectadas": 0
  }
}
```

---

## ✏️ **3. ACTUALIZAR REGLAS**

### 🎯 **Actualización Parcial (PATCH)**
```
PATCH /api/reglas-reprogramacion/1/
```

### 📝 **Payload Actualización Simple**
```json
{
  "valor_numerico": 18,
  "mensaje_error": "Tiempo mínimo actualizado a 18 horas",
  "updated_reason": "Optimización basada en métricas de septiembre"
}
```

### 🎯 **Actualización Completa (PUT)**
```
PUT /api/reglas-reprogramacion/2/
```

### 📝 **Payload Completo**
```json
{
  "nombre": "Límite reprogramaciones clientes premium actualizado",
  "tipo_regla": "LIMITE_REPROGRAMACIONES",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 7,
  "activa": true,
  "prioridad": 2,
  "mensaje_error": "Clientes premium pueden realizar hasta 7 reprogramaciones",
  "condiciones_extras": {
    "solo_clientes_premium": true,
    "nivel_minimo": "PLATINUM",
    "incluye_corporativos": true,
    "sin_costo_adicional": true
  },
  "updated_reason": "Ampliación de beneficios para clientes premium"
}
```

### ✅ **Respuesta Actualización (200)**
```json
{
  "id": 2,
  "nombre": "Límite reprogramaciones clientes premium actualizado",
  "tipo_regla": "LIMITE_REPROGRAMACIONES",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 7,
  "activa": true,
  "prioridad": 2,
  "mensaje_error": "Clientes premium pueden realizar hasta 7 reprogramaciones",
  "condiciones_extras": {
    "solo_clientes_premium": true,
    "nivel_minimo": "PLATINUM", 
    "incluye_corporativos": true,
    "sin_costo_adicional": true
  },
  "created_at": "2025-09-10T14:20:00Z",
  "updated_at": "2025-09-20T16:45:00Z",
  "historial_cambios": [
    {
      "fecha": "2025-09-20T16:45:00Z",
      "usuario": "admin@sistema.com",
      "cambios": {
        "valor_numerico": {"anterior": 5, "nuevo": 7},
        "nombre": {"anterior": "Máximo reprogramaciones VIP", "nuevo": "Límite reprogramaciones clientes premium actualizado"}
      },
      "razon": "Ampliación de beneficios para clientes premium"
    }
  ],
  "impacto_cambio": {
    "reservas_afectadas": 156,
    "usuarios_beneficiados": 89,
    "efectivo_desde": "2025-09-20T16:45:00Z"
  }
}
```

---

## 🔄 **4. ACTUALIZACIÓN MASIVA**

### 🎯 **Endpoint**
```
POST /api/reglas-reprogramacion/bulk-update/
```

### 📝 **Payload Actualización Masiva**
```json
{
  "operacion": "update_multiple",
  "filtros": {
    "tipo_regla": "TIEMPO_MINIMO",
    "aplicable_a": "CLIENTE"
  },
  "cambios": {
    "activa": true,
    "updated_reason": "Reactivación masiva post-mantenimiento"
  },
  "aplicar_a_ids": [1, 3, 5, 7],
  "confirmar_cambios": true
}
```

### 📝 **Payload Creación Masiva**
```json
{
  "operacion": "create_multiple",
  "reglas": [
    {
      "nombre": "Tiempo mínimo sucursal norte",
      "tipo_regla": "TIEMPO_MINIMO",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 24,
      "activa": true,
      "prioridad": 10,
      "condiciones_extras": {
        "sucursal": "NORTE",
        "zona": "URBANA"
      }
    },
    {
      "nombre": "Tiempo mínimo sucursal sur",
      "tipo_regla": "TIEMPO_MINIMO",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 48,
      "activa": true,
      "prioridad": 10,
      "condiciones_extras": {
        "sucursal": "SUR",
        "zona": "RURAL"
      }
    }
  ],
  "confirmar_creacion": true
}
```

### ✅ **Respuesta Actualización Masiva (200)**
```json
{
  "operacion_exitosa": true,
  "tipo_operacion": "update_multiple",
  "total_procesadas": 4,
  "exitosas": 4,
  "fallidas": 0,
  "resultados": [
    {
      "id": 1,
      "status": "updated",
      "cambios_aplicados": ["activa"],
      "valores_anteriores": {"activa": false},
      "valores_nuevos": {"activa": true}
    },
    {
      "id": 3,
      "status": "updated",
      "cambios_aplicados": ["activa"],
      "valores_anteriores": {"activa": false},
      "valores_nuevos": {"activa": true}
    },
    {
      "id": 5,
      "status": "updated", 
      "cambios_aplicados": ["activa"],
      "valores_anteriores": {"activa": false},
      "valores_nuevos": {"activa": true}
    },
    {
      "id": 7,
      "status": "updated",
      "cambios_aplicados": ["activa"],
      "valores_anteriores": {"activa": false},
      "valores_nuevos": {"activa": true}
    }
  ],
  "tiempo_procesamiento": "0.234 segundos",
  "impacto_sistema": {
    "cache_invalidated": true,
    "notificaciones_enviadas": 2,
    "usuarios_afectados": 234
  }
}
```

---

## 📥📤 **5. IMPORT/EXPORT MASIVO**

### 📤 **Exportar Reglas**
```
GET /api/reglas-reprogramacion/export/?format=json&include_stats=true
```

### ✅ **Respuesta Export JSON**
```json
{
  "metadata": {
    "export_date": "2025-09-20T17:00:00Z",
    "total_reglas": 12,
    "reglas_activas": 10,
    "reglas_inactivas": 2,
    "exported_by": "admin@sistema.com",
    "version_sistema": "2.1.0"
  },
  "reglas": [
    {
      "nombre": "Tiempo mínimo 24 horas",
      "tipo_regla": "TIEMPO_MINIMO",
      "aplicable_a": "CLIENTE",
      "valor_numerico": 24,
      "activa": true,
      "prioridad": 1,
      "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación",
      "condiciones_extras": {},
      "estadisticas": {
        "total_aplicaciones": 245,
        "violaciones_mes": 34,
        "eficiencia": 86.1
      }
    }
  ]
}
```

### 📤 **Export CSV**
```
GET /api/reglas-reprogramacion/export/?format=csv
```

### 📥 **Importar Reglas**
```
POST /api/reglas-reprogramacion/import/
Content-Type: multipart/form-data
```

### 📝 **Payload Import**
```json
{
  "archivo": "reglas_nuevas.json",
  "modo_importacion": "merge", // "merge", "replace", "append"
  "validar_antes_importar": true,
  "backup_antes_importar": true,
  "notificar_cambios": true
}
```

### ✅ **Respuesta Import (200)**
```json
{
  "importacion_exitosa": true,
  "modo_utilizado": "merge",
  "estadisticas": {
    "total_procesadas": 15,
    "nuevas_creadas": 8,
    "existentes_actualizadas": 5,
    "ignoradas_duplicadas": 2,
    "errores": 0
  },
  "backup_creado": {
    "archivo": "backup_reglas_20250920_170000.json",
    "ubicacion": "/backups/reglas/",
    "tamaño": "2.4 KB"
  },
  "validaciones": {
    "conflictos_detectados": 0,
    "warnings": [
      "Regla 'Tiempo mínimo VIP' tiene prioridad duplicada con regla existente"
    ]
  },
  "tiempo_procesamiento": "1.567 segundos"
}
```

---

## ✅ **6. VALIDACIÓN DE REGLAS**

### 🎯 **Validar Antes de Crear**
```
POST /api/reglas-reprogramacion/validate/
```

### 📝 **Payload Validación**
```json
{
  "nombre": "Nueva regla temporal",
  "tipo_regla": "TIEMPO_MINIMO",
  "aplicable_a": "CLIENTE",
  "valor_numerico": 24,
  "prioridad": 1,
  "activa": true
}
```

### ✅ **Respuesta Validación Exitosa**
```json
{
  "validacion_exitosa": true,
  "regla_valida": true,
  "conflictos": [],
  "warnings": [],
  "impacto_estimado": {
    "reservas_futuras_afectadas": 45,
    "usuarios_impactados": 23,
    "nivel_impacto": "BAJO"
  },
  "recomendaciones": [
    "La regla es similar a 'Tiempo mínimo 24 horas' existente",
    "Considere unificar ambas reglas para simplificar gestión"
  ]
}
```

### ❌ **Respuesta Validación con Errores**
```json
{
  "validacion_exitosa": false,
  "regla_valida": false,
  "errores": [
    {
      "campo": "prioridad",
      "mensaje": "Ya existe una regla con prioridad 1 para el mismo tipo y rol",
      "codigo": "PRIORIDAD_DUPLICADA"
    },
    {
      "campo": "valor_numerico",
      "mensaje": "El valor debe ser mayor a 0",
      "codigo": "VALOR_INVALIDO"
    }
  ],
  "conflictos": [
    {
      "regla_conflictiva": {
        "id": 1,
        "nombre": "Tiempo mínimo 24 horas",
        "tipo_regla": "TIEMPO_MINIMO"
      },
      "tipo_conflicto": "PRIORIDAD_DUPLICADA",
      "resolucion_sugerida": "Cambie la prioridad a 2 o superior"
    }
  ]
}
```

---

## 🔄 **7. ACTIVACIÓN/DESACTIVACIÓN MASIVA**

### 🎯 **Activar Múltiples Reglas**
```
POST /api/reglas-reprogramacion/activate-batch/
```

### 📝 **Payload Activación**
```json
{
  "accion": "activate",
  "reglas_ids": [1, 3, 5, 7, 9],
  "programar_activacion": "2025-10-01T00:00:00Z",
  "notificar_usuarios": true,
  "mensaje_notificacion": "Nuevas reglas de reprogramación activadas para mejorar el servicio"
}
```

### 📝 **Payload Desactivación**
```json
{
  "accion": "deactivate",
  "filtros": {
    "tipo_regla": "TEMPORADA_ESPECIAL",
    "fecha_fin_vigencia__lt": "2025-09-20T00:00:00Z"
  },
  "razon": "Fin de temporada especial",
  "crear_backup": true
}
```

### ✅ **Respuesta Activación Masiva**
```json
{
  "operacion_exitosa": true,
  "accion_realizada": "activate",
  "reglas_procesadas": 5,
  "exitosas": 5,
  "fallidas": 0,
  "detalles": [
    {
      "regla_id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "status": "activated",
      "activa_desde": "2025-09-20T17:30:00Z"
    },
    {
      "regla_id": 3,
      "nombre": "Sin fines de semana",
      "status": "activated",
      "activa_desde": "2025-09-20T17:30:00Z"
    }
  ],
  "programacion": {
    "activacion_diferida": false,
    "fecha_programada": null,
    "ejecutado_inmediatamente": true
  },
  "notificaciones": {
    "usuarios_notificados": 45,
    "emails_enviados": 45,
    "notificaciones_push": 23
  }
}
```

---

## 📊 **8. MONITOREO Y ESTADÍSTICAS**

### 🎯 **Estadísticas de Reglas**
```
GET /api/reglas-reprogramacion/stats/?periodo=30_dias
```

### ✅ **Respuesta Estadísticas**
```json
{
  "periodo": "últimos 30 días",
  "fecha_inicio": "2025-08-21T00:00:00Z",
  "fecha_fin": "2025-09-20T23:59:59Z",
  "resumen_general": {
    "total_reglas": 12,
    "reglas_activas": 10,
    "reglas_inactivas": 2,
    "total_aplicaciones": 1247,
    "total_violaciones": 156,
    "eficiencia_promedio": 87.5
  },
  "reglas_mas_utilizadas": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "aplicaciones": 445,
      "violaciones": 67,
      "eficiencia": 84.9
    },
    {
      "id": 2,
      "nombre": "Máximo 3 reprogramaciones",
      "aplicaciones": 234,
      "violaciones": 23,
      "eficiencia": 90.2
    }
  ],
  "reglas_mas_violadas": [
    {
      "id": 1,
      "nombre": "Tiempo mínimo 24 horas",
      "violaciones": 67,
      "porcentaje_violacion": 15.1,
      "tendencia": "estable"
    }
  ],
  "recomendaciones": [
    {
      "tipo": "OPTIMIZACION",
      "regla_id": 1,
      "sugerencia": "Considere reducir tiempo mínimo de 24 a 18 horas para clientes VIP",
      "impacto_estimado": "Reducción del 25% en violaciones"
    }
  ]
}
```

### 🎯 **Historial de Cambios**
```
GET /api/reglas-reprogramacion/1/historial/
```

### ✅ **Respuesta Historial**
```json
{
  "regla_id": 1,
  "nombre_actual": "Tiempo mínimo 24 horas",
  "total_cambios": 5,
  "historial": [
    {
      "fecha": "2025-09-20T16:45:00Z",
      "usuario": {
        "id": 1,
        "username": "admin@sistema.com",
        "nombre_completo": "Admin Sistema"
      },
      "accion": "UPDATE",
      "cambios": {
        "valor_numerico": {"anterior": 18, "nuevo": 24},
        "mensaje_error": {
          "anterior": "Debe reprogramar con al menos 18 horas",
          "nuevo": "Debe reprogramar con al menos 24 horas de anticipación"
        }
      },
      "razon": "Incremento basado en análisis de satisfacción del cliente",
      "impacto": {
        "reservas_afectadas": 67,
        "usuarios_notificados": 234
      }
    },
    {
      "fecha": "2025-09-15T10:30:00Z",
      "usuario": {
        "id": 1,
        "username": "admin@sistema.com",
        "nombre_completo": "Admin Sistema"
      },
      "accion": "UPDATE",
      "cambios": {
        "condiciones_extras": {
          "anterior": {},
          "nuevo": {"excluir_feriados": true}
        }
      },
      "razon": "Agregar excepción para feriados nacionales"
    }
  ]
}
```

---

## 🛠️ **HERRAMIENTAS DE GESTIÓN**

### 🎨 **Panel de Administración React**

```javascript
const PanelGestionReglamentos = () => {
  const [reglas, setReglas] = useState([]);
  const [filtros, setFiltros] = useState({});
  const [modoEdicion, setModoEdicion] = useState(null);
  const [estadisticas, setEstadisticas] = useState({});
  
  const cargarReglas = async () => {
    try {
      const response = await fetch('/api/reglas-reprogramacion/', {
        headers: getAuthHeaders()
      });
      const data = await response.json();
      setReglas(data.results);
    } catch (error) {
      console.error('Error cargando reglas:', error);
    }
  };
  
  const actualizarRegla = async (reglaId, cambios) => {
    try {
      const response = await fetch(`/api/reglas-reprogramacion/${reglaId}/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(cambios)
      });
      
      if (response.ok) {
        await cargarReglas();
        mostrarNotificacion('Regla actualizada exitosamente', 'success');
      }
    } catch (error) {
      mostrarNotificacion('Error actualizando regla', 'error');
    }
  };
  
  const exportarReglas = async (formato = 'json') => {
    try {
      const response = await fetch(`/api/reglas-reprogramacion/export/?format=${formato}`, {
        headers: getAuthHeaders()
      });
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reglas_${new Date().toISOString().split('T')[0]}.${formato}`;
      a.click();
    } catch (error) {
      console.error('Error exportando reglas:', error);
    }
  };
  
  return (
    <div className="panel-gestion-reglamentos">
      <h1>Gestión de Reglamentos</h1>
      
      <div className="panel-estadisticas">
        <div className="stat-card">
          <h3>Reglas Activas</h3>
          <div className="stat-number">{estadisticas.reglas_activas}</div>
        </div>
        <div className="stat-card">
          <h3>Eficiencia Promedio</h3>
          <div className="stat-number">{estadisticas.eficiencia_promedio}%</div>
        </div>
        <div className="stat-card">
          <h3>Violaciones Mes</h3>
          <div className="stat-number">{estadisticas.violaciones_mes}</div>
        </div>
      </div>
      
      <div className="panel-acciones">
        <button 
          className="btn-primary"
          onClick={() => setModoEdicion('nueva')}
        >
          + Nueva Regla
        </button>
        <button 
          className="btn-secondary"
          onClick={() => exportarReglas('json')}
        >
          📤 Exportar JSON
        </button>
        <button 
          className="btn-secondary"
          onClick={() => exportarReglas('csv')}
        >
          📊 Exportar CSV
        </button>
      </div>
      
      <div className="tabla-reglas">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Aplicable A</th>
              <th>Valor</th>
              <th>Estado</th>
              <th>Prioridad</th>
              <th>Eficiencia</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {reglas.map(regla => (
              <FilaRegla 
                key={regla.id}
                regla={regla}
                onActualizar={actualizarRegla}
                onEditar={() => setModoEdicion(regla.id)}
              />
            ))}
          </tbody>
        </table>
      </div>
      
      {modoEdicion && (
        <ModalEdicionRegla 
          reglaId={modoEdicion}
          onGuardar={() => {
            setModoEdicion(null);
            cargarReglas();
          }}
          onCancelar={() => setModoEdicion(null)}
        />
      )}
    </div>
  );
};

const FilaRegla = ({ regla, onActualizar, onEditar }) => {
  const toggleActivo = () => {
    onActualizar(regla.id, { activa: !regla.activa });
  };
  
  return (
    <tr className={regla.activa ? 'regla-activa' : 'regla-inactiva'}>
      <td>{regla.nombre}</td>
      <td>{regla.tipo_regla}</td>
      <td>{regla.aplicable_a}</td>
      <td>
        {regla.valor_numerico || regla.valor_decimal || regla.valor_texto}
      </td>
      <td>
        <button 
          className={`toggle-btn ${regla.activa ? 'active' : 'inactive'}`}
          onClick={toggleActivo}
        >
          {regla.activa ? 'Activa' : 'Inactiva'}
        </button>
      </td>
      <td>{regla.prioridad}</td>
      <td>
        {regla.estadisticas_uso?.eficiencia_porcentaje?.toFixed(1)}%
      </td>
      <td>
        <button onClick={onEditar}>✏️</button>
        <button onClick={() => verHistorial(regla.id)}>📋</button>
        <button onClick={() => duplicarRegla(regla)}>📋</button>
      </td>
    </tr>
  );
};
```

### 🔄 **Utilitarios de Actualización**

```javascript
// Utilidad para actualización masiva
const actualizacionMasiva = async (filtros, cambios) => {
  const payload = {
    operacion: 'update_multiple',
    filtros: filtros,
    cambios: cambios,
    confirmar_cambios: true
  };
  
  const response = await fetch('/api/reglas-reprogramacion/bulk-update/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload)
  });
  
  return await response.json();
};

// Validador de reglas
const validarRegla = async (reglaData) => {
  const response = await fetch('/api/reglas-reprogramacion/validate/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(reglaData)
  });
  
  return await response.json();
};

// Importador de reglas
const importarReglas = async (archivo, modo = 'merge') => {
  const formData = new FormData();
  formData.append('archivo', archivo);
  formData.append('modo_importacion', modo);
  formData.append('validar_antes_importar', 'true');
  
  const response = await fetch('/api/reglas-reprogramacion/import/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${getToken()}`
    },
    body: formData
  });
  
  return await response.json();
};
```

---

**✨ ¡Sistema completo de Gestión de Reglamentos documentado! ✨**

Esta documentación proporciona todas las herramientas necesarias para administrar el sistema de reglas de forma eficiente y sin interrupciones del servicio.