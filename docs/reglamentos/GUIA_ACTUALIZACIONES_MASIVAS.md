# GUÍA DE ACTUALIZACIONES MASIVAS Y MIGRACIÓN DE REGLAMENTOS

## Introducción

Esta guía describe los procesos para realizar actualizaciones masivas de reglamentos, migración de reglas entre ambientes y gestión de versiones del sistema de políticas.

## 1. FLUJOS DE ACTUALIZACIÓN MASIVA

### 1.1 Actualización por Filtros

```javascript
// Componente React para Actualización Masiva
import React, { useState } from 'react';
import { Card, Form, Button, Alert, Progress, Table } from 'antd';

const ActualizacionMasiva = () => {
  const [filtros, setFiltros] = useState({});
  const [cambios, setCambios] = useState({});
  const [progreso, setProgreso] = useState(0);
  const [resultados, setResultados] = useState(null);

  const aplicarCambiosMasivos = async () => {
    try {
      const response = await fetch('/api/reglamentos/bulk-update/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          filtros: filtros,
          cambios: cambios
        })
      });

      const resultado = await response.json();
      setResultados(resultado);
      
      if (resultado.actualizadas > 0) {
        message.success(`${resultado.actualizadas} reglas actualizadas`);
      }
    } catch (error) {
      message.error('Error en actualización masiva');
    }
  };

  return (
    <Card title="Actualización Masiva de Reglamentos">
      <Form layout="vertical">
        <Form.Item label="Filtros de Selección">
          <Select
            mode="multiple"
            placeholder="Seleccionar tipos de regla"
            onChange={(value) => setFiltros({...filtros, tipo_regla__in: value})}
          >
            <Option value="reprogramacion">Reprogramación</Option>
            <Option value="cancelacion">Cancelación</Option>
            <Option value="politica">Política</Option>
          </Select>
        </Form.Item>

        <Form.Item label="Cambios a Aplicar">
          <Input.Group>
            <Input
              placeholder="Costo reprogramación"
              onChange={(e) => setCambios({
                ...cambios, 
                costo_reprogramacion: e.target.value
              })}
            />
            <DatePicker
              placeholder="Nueva fecha fin vigencia"
              onChange={(date) => setCambios({
                ...cambios,
                fecha_fin_vigencia: date?.format('YYYY-MM-DD')
              })}
            />
          </Input.Group>
        </Form.Item>

        <Button 
          type="primary" 
          onClick={aplicarCambiosMasivos}
          loading={progreso > 0}
        >
          Aplicar Cambios
        </Button>
      </Form>

      {resultados && (
        <Alert
          message={`Proceso completado: ${resultados.actualizadas} actualizadas`}
          type="success"
          style={{ marginTop: 16 }}
        />
      )}
    </Card>
  );
};
```

### 1.2 Actualización por Lotes

```javascript
// Payload para actualización por lotes
const actualizarPorLotes = async (reglasIds, cambios) => {
  const reglas = reglasIds.map(id => ({
    id: id,
    ...cambios
  }));

  const response = await fetch('/api/reglamentos/bulk-update/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ reglas })
  });

  return await response.json();
};

// Ejemplo de uso
const actualizarCostosTemporadaAlta = async () => {
  const reglasTemporadaAlta = [1, 3, 5, 7, 9];
  const nuevosParametros = {
    costo_reprogramacion: "100.00",
    condiciones_especiales: {
      temporada_alta: true,
      recargo_fin_semana: 25.00
    }
  };

  const resultado = await actualizarPorLotes(
    reglasTemporadaAlta, 
    nuevosParametros
  );
  
  console.log(`${resultado.actualizadas} reglas actualizadas`);
};
```

## 2. MIGRACIÓN ENTRE AMBIENTES

### 2.1 Exportar Configuración Completa

```bash
# Endpoint para exportar todas las reglas
GET /api/reglamentos/export/?formato=json&incluir_inactivas=true
```

```javascript
// Función para exportar reglas
const exportarReglamentos = async (filtros = {}) => {
  const params = new URLSearchParams({
    formato: 'json',
    incluir_inactivas: filtros.incluir_inactivas || 'false',
    tipo_regla: filtros.tipo_regla || '',
    fecha_desde: filtros.fecha_desde || '',
    fecha_hasta: filtros.fecha_hasta || ''
  });

  const response = await fetch(`/api/reglamentos/export/?${params}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reglamentos_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
  }
};
```

### 2.2 Estructura de Archivo de Migración

```json
{
  "metadata": {
    "version": "1.0",
    "exported_at": "2024-01-20T10:30:00Z",
    "exported_by": "admin@empresa.com",
    "total_rules": 25,
    "ambiente_origen": "desarrollo"
  },
  "reglas": [
    {
      "id_temporal": "REG_001",
      "tipo_regla": "reprogramacion",
      "nombre_regla": "Reprogramación Estándar",
      "descripcion": "Regla base para reprogramaciones",
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
      "condiciones_especiales": {
        "aplicable_hoteles": true,
        "aplicable_vuelos": false
      },
      "dependencias": [],
      "tags": ["estandar", "hoteles"]
    }
  ],
  "relaciones": [
    {
      "regla_padre": "REG_001",
      "reglas_hijas": ["REG_002", "REG_003"],
      "tipo_relacion": "herencia"
    }
  ]
}
```

### 2.3 Importar con Validación

```javascript
// Componente para migración de reglas
const MigracionReglamentos = () => {
  const [archivo, setArchivo] = useState(null);
  const [validacion, setValidacion] = useState(null);
  const [configuracion, setConfiguracion] = useState({
    sobrescribir: false,
    validar_antes: true,
    crear_respaldo: true,
    mapear_usuarios: true
  });

  const validarArchivo = async (archivo) => {
    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('solo_validar', 'true');

    const response = await fetch('/api/reglamentos/import/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const resultado = await response.json();
    setValidacion(resultado);
  };

  const ejecutarMigracion = async () => {
    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('configuracion', JSON.stringify(configuracion));

    const response = await fetch('/api/reglamentos/import/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const resultado = await response.json();
    
    if (resultado.success) {
      message.success(`Migración completada: ${resultado.importadas} reglas`);
    } else {
      message.error(`Errores en migración: ${resultado.errores.length}`);
    }
  };

  return (
    <Card title="Migración de Reglamentos">
      <Steps current={archivo ? (validacion ? 2 : 1) : 0}>
        <Step title="Cargar Archivo" />
        <Step title="Validar" />
        <Step title="Migrar" />
      </Steps>

      <Upload
        beforeUpload={(file) => {
          setArchivo(file);
          validarArchivo(file);
          return false;
        }}
        accept=".json"
      >
        <Button icon={<UploadOutlined />}>
          Seleccionar Archivo de Migración
        </Button>
      </Upload>

      {validacion && (
        <Alert
          message={`Validación: ${validacion.validas} válidas, ${validacion.errores} errores`}
          type={validacion.errores > 0 ? "warning" : "success"}
          style={{ margin: '16px 0' }}
        />
      )}

      <Form layout="vertical">
        <Form.Item label="Configuración de Migración">
          <Checkbox.Group
            value={Object.keys(configuracion).filter(k => configuracion[k])}
            onChange={(values) => {
              const newConfig = {};
              Object.keys(configuracion).forEach(key => {
                newConfig[key] = values.includes(key);
              });
              setConfiguracion(newConfig);
            }}
          >
            <Checkbox value="sobrescribir">Sobrescribir existentes</Checkbox>
            <Checkbox value="validar_antes">Validar antes de importar</Checkbox>
            <Checkbox value="crear_respaldo">Crear respaldo</Checkbox>
            <Checkbox value="mapear_usuarios">Mapear usuarios</Checkbox>
          </Checkbox.Group>
        </Form.Item>

        <Button
          type="primary"
          onClick={ejecutarMigracion}
          disabled={!validacion || validacion.errores > 0}
        >
          Ejecutar Migración
        </Button>
      </Form>
    </Card>
  );
};
```

## 3. VERSIONADO Y CONTROL DE CAMBIOS

### 3.1 Sistema de Versiones

```javascript
// Modelo de versión de reglamentos
const versionSchema = {
  version: "string - Número de versión (ej: 1.2.3)",
  fecha_version: "datetime - Fecha de la versión",
  descripcion: "string - Descripción de cambios",
  usuario_creador: "string - Usuario que creó la versión",
  reglas_incluidas: "array - IDs de reglas en esta versión",
  reglas_modificadas: "array - Reglas que cambiaron",
  reglas_eliminadas: "array - Reglas eliminadas",
  reglas_nuevas: "array - Reglas nuevas",
  activa: "boolean - Si esta versión está activa",
  respaldo_datos: "json - Respaldo de datos anteriores"
};

// API para manejo de versiones
const crearVersion = async (descripcion, reglas_incluidas) => {
  const response = await fetch('/api/reglamentos/versions/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      descripcion,
      reglas_incluidas,
      crear_respaldo: true
    })
  });

  return await response.json();
};
```

### 3.2 Rollback de Cambios

```javascript
// Función para revertir a versión anterior
const revertirVersion = async (versionId) => {
  const response = await fetch(`/api/reglamentos/versions/${versionId}/restore/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      confirmar_rollback: true,
      crear_respaldo_actual: true
    })
  });

  const resultado = await response.json();
  
  if (resultado.success) {
    message.success(`Versión ${resultado.version} restaurada exitosamente`);
  }
  
  return resultado;
};

// Componente para gestión de versiones
const GestionVersiones = () => {
  const [versiones, setVersiones] = useState([]);
  const [versionActiva, setVersionActiva] = useState(null);

  const columnas = [
    {
      title: 'Versión',
      dataIndex: 'version',
      key: 'version'
    },
    {
      title: 'Fecha',
      dataIndex: 'fecha_version',
      key: 'fecha_version',
      render: (fecha) => new Date(fecha).toLocaleDateString()
    },
    {
      title: 'Descripción',
      dataIndex: 'descripcion',
      key: 'descripcion'
    },
    {
      title: 'Reglas',
      dataIndex: 'reglas_incluidas',
      key: 'reglas_incluidas',
      render: (reglas) => reglas.length
    },
    {
      title: 'Estado',
      dataIndex: 'activa',
      key: 'activa',
      render: (activa) => (
        <Tag color={activa ? 'green' : 'default'}>
          {activa ? 'Activa' : 'Inactiva'}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space>
          <Button
            size="small"
            onClick={() => revertirVersion(record.id)}
            disabled={record.activa}
          >
            Revertir
          </Button>
          <Button
            size="small"
            onClick={() => descargarVersion(record.id)}
          >
            Descargar
          </Button>
        </Space>
      )
    }
  ];

  return (
    <Card title="Gestión de Versiones">
      <Table
        dataSource={versiones}
        columns={columnas}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
    </Card>
  );
};
```

## 4. AUTOMATIZACIÓN DE ACTUALIZACIONES

### 4.1 Scripts de Actualización Programada

```python
# Script Python para actualización automática
import requests
import schedule
import time
from datetime import datetime, timedelta

class ActualizadorAutomatico:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def actualizar_costos_temporada_alta(self):
        """Actualiza costos para temporada alta automáticamente"""
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(days=90)
        
        payload = {
            'filtros': {
                'tipo_regla': 'reprogramacion',
                'activa': True
            },
            'cambios': {
                'costo_reprogramacion': '75.00',
                'condiciones_especiales': {
                    'temporada_alta': True,
                    'fecha_inicio_temporada': fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin_temporada': fecha_fin.strftime('%Y-%m-%d')
                }
            }
        }
        
        response = requests.post(
            f'{self.base_url}/api/reglamentos/bulk-update/',
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"Actualización automática: {resultado['actualizadas']} reglas")
        else:
            print(f"Error en actualización: {response.status_code}")

    def revisar_vigencias(self):
        """Revisa y actualiza reglas próximas a vencer"""
        response = requests.get(
            f'{self.base_url}/api/reglamentos/expiring/',
            headers=self.headers,
            params={'dias': 30}
        )
        
        if response.status_code == 200:
            reglas_expirando = response.json()
            
            for regla in reglas_expirando:
                # Extender vigencia automáticamente
                nueva_fecha = datetime.now() + timedelta(days=365)
                
                requests.patch(
                    f'{self.base_url}/api/reglamentos/{regla["id"]}/',
                    headers=self.headers,
                    json={
                        'fecha_fin_vigencia': nueva_fecha.strftime('%Y-%m-%d')
                    }
                )
                
                print(f"Extendida vigencia de regla {regla['nombre_regla']}")

# Configurar tareas programadas
actualizador = ActualizadorAutomatico('http://localhost:8000', 'token_aqui')

# Ejecutar cada primer día del mes
schedule.every().month.do(actualizador.actualizar_costos_temporada_alta)

# Revisar vigencias semanalmente
schedule.every().week.do(actualizador.revisar_vigencias)

# Mantener el script corriendo
while True:
    schedule.run_pending()
    time.sleep(3600)  # Revisar cada hora
```

### 4.2 Triggers de Base de Datos

```sql
-- Trigger para auditoría automática de cambios
CREATE TRIGGER trigger_auditoria_reglamentos
AFTER UPDATE ON reservas_reglasreprogramacion
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_reglamentos (
        regla_id,
        accion,
        datos_anteriores,
        datos_nuevos,
        usuario,
        fecha_cambio
    ) VALUES (
        NEW.id,
        'UPDATE',
        JSON_OBJECT(
            'costo_reprogramacion', OLD.costo_reprogramacion,
            'maximo_reprogramaciones', OLD.maximo_reprogramaciones,
            'activa', OLD.activa
        ),
        JSON_OBJECT(
            'costo_reprogramacion', NEW.costo_reprogramacion,
            'maximo_reprogramaciones', NEW.maximo_reprogramaciones,
            'activa', NEW.activa
        ),
        USER(),
        NOW()
    );
END;

-- Trigger para validación automática
CREATE TRIGGER trigger_validacion_reglamentos
BEFORE INSERT OR UPDATE ON reservas_reglasreprogramacion
FOR EACH ROW
BEGIN
    -- Validar que días mínimos <= máximos
    IF NEW.dias_minimos_reprogramacion > NEW.dias_maximos_reprogramacion THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Días mínimos no pueden ser mayores que máximos';
    END IF;
    
    -- Validar que fecha fin >= fecha inicio
    IF NEW.fecha_fin_vigencia IS NOT NULL AND NEW.fecha_fin_vigencia < NEW.fecha_inicio_vigencia THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Fecha fin no puede ser anterior a fecha inicio';
    END IF;
    
    -- Actualizar timestamp
    SET NEW.updated_at = NOW();
END;
```

## 5. MONITOREO Y ALERTAS

### 5.1 Dashboard de Monitoreo

```javascript
// Componente para monitoreo de reglamentos
const MonitoreoReglamentos = () => {
  const [estadisticas, setEstadisticas] = useState({});
  const [alertas, setAlertas] = useState([]);

  const obtenerEstadisticas = async () => {
    const response = await fetch('/api/reglamentos/statistics/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const datos = await response.json();
    setEstadisticas(datos);
  };

  const obtenerAlertas = async () => {
    const response = await fetch('/api/reglamentos/alerts/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const alertas = await response.json();
    setAlertas(alertas);
  };

  return (
    <Row gutter={16}>
      <Col span={8}>
        <Card title="Reglas Activas" bordered={false}>
          <Statistic value={estadisticas.activas || 0} />
        </Card>
      </Col>
      <Col span={8}>
        <Card title="Próximas a Vencer" bordered={false}>
          <Statistic
            value={estadisticas.expirando || 0}
            valueStyle={{ color: '#faad14' }}
          />
        </Card>
      </Col>
      <Col span={8}>
        <Card title="Con Conflictos" bordered={false}>
          <Statistic
            value={estadisticas.conflictos || 0}
            valueStyle={{ color: '#ff4d4f' }}
          />
        </Card>
      </Col>
      
      <Col span={24} style={{ marginTop: 16 }}>
        <Card title="Alertas del Sistema">
          <List
            dataSource={alertas}
            renderItem={(alerta) => (
              <List.Item>
                <Alert
                  message={alerta.titulo}
                  description={alerta.descripcion}
                  type={alerta.tipo}
                  showIcon
                />
              </List.Item>
            )}
          />
        </Card>
      </Col>
    </Row>
  );
};
```

## 6. MEJORES PRÁCTICAS

### 6.1 Flujo de Actualización Recomendado

1. **Planificación**
   - Identificar reglas a actualizar
   - Validar impacto en reservas existentes
   - Crear plan de rollback

2. **Validación**
   - Probar cambios en ambiente de desarrollo
   - Ejecutar validaciones automáticas
   - Revisar conflictos potenciales

3. **Ejecución**
   - Crear respaldo antes de cambios
   - Aplicar actualizaciones en horario de menor tráfico
   - Monitorear resultados en tiempo real

4. **Verificación**
   - Validar que cambios se aplicaron correctamente
   - Verificar funcionamiento del sistema
   - Documentar cambios realizados

### 6.2 Checklist de Migración

- [ ] Respaldo de base de datos actual
- [ ] Validación de archivo de migración
- [ ] Verificación de dependencias
- [ ] Mapeo de usuarios y permisos
- [ ] Prueba en ambiente de staging
- [ ] Plan de rollback preparado
- [ ] Notificación a usuarios afectados
- [ ] Documentación actualizada

### 6.3 Alertas Automáticas

```javascript
// Configuración de alertas
const alertas = {
  reglas_expirando: {
    dias_anticipacion: 30,
    destinatarios: ['admin@empresa.com'],
    frecuencia: 'semanal'
  },
  conflictos_detectados: {
    severidad: 'alta',
    notificacion_inmediata: true
  },
  uso_excesivo_cpu: {
    umbral: 80,
    accion: 'optimizar_consultas'
  }
};
```

Esta guía proporciona un marco completo para la gestión avanzada de reglamentos, incluyendo automatización, monitoreo y mejores prácticas para mantener un sistema robusto y eficiente.