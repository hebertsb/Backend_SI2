# Reglas de Reprogramación de Reservas

## Descripción General

El sistema de reservas incluye un **motor de reglas dinámico** que permite configurar y aplicar automáticamente las políticas de reprogramación. Estas reglas son completamente configurables y se aplican según el rol del usuario y las condiciones específicas de cada reserva.

## Arquitectura del Sistema de Reglas

### Modelo Principal: `ReglasReprogramacion`

El sistema se basa en un modelo flexible que permite definir diferentes tipos de restricciones:

```python
class ReglasReprogramacion(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    tipo_regla = models.CharField(max_length=30, choices=TIPOS_REGLA)
    aplicable_a = models.CharField(max_length=20, choices=ROLES_APLICABLES)
    valor_numerico = models.IntegerField(null=True, blank=True)
    valor_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_texto = models.TextField(null=True, blank=True)
    valor_booleano = models.BooleanField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    prioridad = models.PositiveSmallIntegerField(default=1)
```

## Tipos de Reglas Disponibles

### 1. Restricciones de Tiempo

#### TIEMPO_MINIMO
**Descripción**: Tiempo mínimo de anticipación requerido para reprogramar
**Valor**: Horas antes de la fecha original
**Ejemplo**: `24` (24 horas de anticipación)

```json
{
    "nombre": "Anticipación mínima clientes",
    "tipo_regla": "TIEMPO_MINIMO",
    "aplicable_a": "CLIENTE",
    "valor_numerico": 24,
    "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación"
}
```

#### TIEMPO_MAXIMO
**Descripción**: Tiempo máximo permitido para reprogramar hacia el futuro
**Valor**: Horas hacia el futuro
**Ejemplo**: `8760` (1 año = 365 días × 24 horas)

```json
{
    "nombre": "Límite máximo futuro",
    "tipo_regla": "TIEMPO_MAXIMO", 
    "aplicable_a": "ALL",
    "valor_numerico": 8760,
    "mensaje_error": "No se puede reprogramar más de 1 año en el futuro"
}
```

### 2. Límites de Cantidad

#### LIMITE_REPROGRAMACIONES
**Descripción**: Número máximo de reprogramaciones por reserva
**Valor**: Cantidad numérica
**Ejemplo**: `3` (máximo 3 reprogramaciones)

```json
{
    "nombre": "Máximo 3 reprogramaciones",
    "tipo_regla": "LIMITE_REPROGRAMACIONES",
    "aplicable_a": "CLIENTE",
    "valor_numerico": 3,
    "mensaje_error": "Esta reserva ya alcanzó el límite de 3 reprogramaciones"
}
```

#### LIMITE_DIARIO
**Descripción**: Número máximo de reprogramaciones por día por usuario
**Valor**: Cantidad numérica

#### LIMITE_SEMANAL  
**Descripción**: Número máximo de reprogramaciones por semana por usuario
**Valor**: Cantidad numérica

#### LIMITE_MENSUAL
**Descripción**: Número máximo de reprogramaciones por mes por usuario
**Valor**: Cantidad numérica

### 3. Restricciones de Días y Horas

#### DIAS_BLACKOUT
**Descripción**: Días de la semana no permitidos para reprogramar
**Valor**: Lista de días en JSON
**Ejemplo**: `["sabado", "domingo"]`

```json
{
    "nombre": "Sin reprogramaciones fines de semana",
    "tipo_regla": "DIAS_BLACKOUT",
    "aplicable_a": "CLIENTE",
    "valor_texto": "[\"sabado\", \"domingo\"]",
    "mensaje_error": "No se puede reprogramar para fines de semana"
}
```

#### HORAS_BLACKOUT
**Descripción**: Horas del día no permitidas para reprogramar
**Valor**: Lista de horas en JSON (formato 24h)
**Ejemplo**: `[0, 1, 2, 3, 4, 5, 22, 23]` (madrugada y noche)

```json
{
    "nombre": "Sin horarios nocturnos",
    "tipo_regla": "HORAS_BLACKOUT",
    "aplicable_a": "ALL",
    "valor_texto": "[0, 1, 2, 3, 4, 5, 22, 23]",
    "mensaje_error": "No se puede reprogramar en horarios nocturnos (10pm - 6am)"
}
```

### 4. Restricciones por Capacidad

#### CAPACIDAD_MAXIMA
**Descripción**: Capacidad máxima de reservas por fecha
**Valor**: Número máximo de reservas

### 5. Penalizaciones Económicas

#### DESCUENTO_PENALIZACION
**Descripción**: Porcentaje de descuento por reprogramar
**Valor**: Porcentaje decimal (ej: 0.10 = 10%)

### 6. Restricciones por Servicios

#### SERVICIOS_RESTRINGIDOS
**Descripción**: Servicios que tienen restricciones especiales para reprogramar
**Valor**: Lista de nombres de servicios en JSON

```json
{
    "nombre": "Servicios premium restringidos",
    "tipo_regla": "SERVICIOS_RESTRINGIDOS", 
    "aplicable_a": "CLIENTE",
    "valor_texto": "[\"Tour Premium Salar\", \"Excursión VIP\"]",
    "mensaje_error": "Los servicios premium requieren aprobación especial para reprogramar"
}
```

### 7. Excepciones por Rol

#### ROLES_EXCLUIDOS
**Descripción**: Roles que están excluidos de ciertas restricciones
**Valor**: Lista de roles en JSON

## Aplicabilidad por Roles

Las reglas pueden aplicarse a diferentes roles de usuario:

| Valor | Descripción | Aplica a |
|-------|-------------|----------|
| `ALL` | Todos los roles | Clientes, Operadores, Administradores |
| `CLIENTE` | Solo clientes | Usuarios finales |
| `OPERADOR` | Solo operadores | Personal de soporte |
| `ADMIN` | Solo administradores | Administradores del sistema |
| `CLIENTE_OPERADOR` | Clientes y operadores | Excluye solo admins |
| `OPERADOR_ADMIN` | Operadores y admins | Excluye solo clientes |

## Sistema de Prioridades

Las reglas tienen un campo `prioridad` (1 = máxima prioridad):

1. **Prioridad 1**: Reglas críticas de seguridad/negocio
2. **Prioridad 2**: Reglas de calidad de servicio  
3. **Prioridad 3**: Reglas de conveniencia/optimización

## Validaciones Automáticas

### En el Serializer `ReprogramacionReservaSerializer`

El sistema aplica automáticamente las reglas durante la validación:

```python
def validate_nueva_fecha(self, value):
    # 1. Verificar tiempo mínimo
    regla = ReglasReprogramacion.obtener_regla_activa('TIEMPO_MINIMO', rol)
    if regla and value <= timezone.now() + timedelta(hours=regla.obtener_valor()):
        raise ValidationError(regla.mensaje_error)
    
    # 2. Verificar tiempo máximo  
    regla = ReglasReprogramacion.obtener_regla_activa('TIEMPO_MAXIMO', rol)
    if regla and value > timezone.now() + timedelta(hours=regla.obtener_valor()):
        raise ValidationError(regla.mensaje_error)
        
    # 3. Verificar días blackout
    # 4. Verificar horas blackout
    # ...
```

### En las Validaciones Generales

```python
def validate(self, attrs):
    # Verificar límite de reprogramaciones
    regla = ReglasReprogramacion.obtener_regla_activa('LIMITE_REPROGRAMACIONES', rol)
    if regla and reserva.numero_reprogramaciones >= regla.obtener_valor():
        raise ValidationError(regla.mensaje_error)
    
    # Verificar servicios restringidos
    # ...
```

## API de Gestión de Reglas

### Endpoints Disponibles

#### 1. Listar Reglas
```http
GET /api/reglas-reprogramacion/
```

**Respuesta**:
```json
{
    "results": [
        {
            "id": 1,
            "nombre": "Anticipación mínima clientes",
            "tipo_regla": "TIEMPO_MINIMO",
            "aplicable_a": "CLIENTE", 
            "valor_numerico": 24,
            "activa": true,
            "prioridad": 1,
            "mensaje_error": "Debe reprogramar con al menos 24 horas de anticipación"
        }
    ]
}
```

#### 2. Obtener Reglas Activas
```http
GET /api/reglas-reprogramacion/activas/
```

#### 3. Agrupar Reglas por Tipo
```http
GET /api/reglas-reprogramacion/por-tipo/
```

#### 4. Crear Nueva Regla
```http
POST /api/reglas-reprogramacion/
```

**Payload**:
```json
{
    "nombre": "Límite fin de semana",
    "tipo_regla": "DIAS_BLACKOUT",
    "aplicable_a": "CLIENTE",
    "valor_texto": "[\"sabado\", \"domingo\"]",
    "activa": true,
    "prioridad": 2,
    "mensaje_error": "No se permite reprogramar para fines de semana"
}
```

#### 5. Actualizar Regla
```http
PUT /api/reglas-reprogramacion/{id}/
```

#### 6. Eliminar Regla
```http
DELETE /api/reglas-reprogramacion/{id}/
```

## Configuración de Reglas Típicas

### Configuración para Agencia Turística

```sql
-- Tiempo mínimo para clientes: 24 horas
INSERT INTO reservas_reglasreprogramacion 
(nombre, tipo_regla, aplicable_a, valor_numerico, activa, prioridad, mensaje_error)
VALUES 
('Anticipación 24h clientes', 'TIEMPO_MINIMO', 'CLIENTE', 24, true, 1, 
 'Debe reprogramar con al menos 24 horas de anticipación');

-- Tiempo mínimo para operadores: 4 horas  
INSERT INTO reservas_reglasreprogramacion 
(nombre, tipo_regla, aplicable_a, valor_numerico, activa, prioridad, mensaje_error)
VALUES 
('Anticipación 4h operadores', 'TIEMPO_MINIMO', 'OPERADOR', 4, true, 1,
 'Los operadores deben reprogramar con al menos 4 horas de anticipación');

-- Límite de reprogramaciones por reserva
INSERT INTO reservas_reglasreprogramacion 
(nombre, tipo_regla, aplicable_a, valor_numerico, activa, prioridad, mensaje_error)
VALUES 
('Máximo 3 reprogramaciones', 'LIMITE_REPROGRAMACIONES', 'CLIENTE', 3, true, 1,
 'Esta reserva ya alcanzó el límite máximo de 3 reprogramaciones');

-- Sin reprogramaciones en fines de semana para ciertos servicios
INSERT INTO reservas_reglasreprogramacion 
(nombre, tipo_regla, aplicable_a, valor_texto, activa, prioridad, mensaje_error)
VALUES 
('Sin fines de semana', 'DIAS_BLACKOUT', 'CLIENTE', '["sabado", "domingo"]', true, 2,
 'No se puede reprogramar para fines de semana');

-- Sin horarios nocturnos
INSERT INTO reservas_reglasreprogramacion 
(nombre, tipo_regla, aplicable_a, valor_texto, activa, prioridad, mensaje_error)
VALUES 
('Sin horarios nocturnos', 'HORAS_BLACKOUT', 'ALL', '[22, 23, 0, 1, 2, 3, 4, 5]', true, 2,
 'No se puede reprogramar en horarios nocturnos (10pm - 6am)');
```

## Integración con Notificaciones

Las reglas se integran con el sistema de notificaciones:

1. **Validación previa**: Las reglas se verifican antes de permitir la reprogramación
2. **Mensajes personalizados**: Los errores incluyen mensajes específicos de cada regla
3. **Logs de violaciones**: Se registran intentos de violar reglas para auditoría
4. **Notificaciones especiales**: Se pueden configurar alertas cuando se violan reglas críticas

## Monitoreo y Auditoría

### Métricas de Reglas

```python
# Endpoint para métricas de reglas
@api_view(['GET'])
def metricas_reglas(request):
    return Response({
        'reglas_activas': ReglasReprogramacion.objects.filter(activa=True).count(),
        'violaciones_ultimo_mes': HistorialViolacionReglas.objects.filter(
            fecha__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'reglas_por_tipo': ReglasReprogramacion.objects.values('tipo_regla').annotate(
            cantidad=Count('id')
        )
    })
```

### Dashboard de Administración

El admin de Django incluye interfaces para:

- ✅ Gestionar reglas de forma visual
- ✅ Activar/desactivar reglas temporalmente
- ✅ Ver violaciones de reglas
- ✅ Configurar mensajes de error personalizados
- ✅ Establecer vigencias temporales

## Ejemplos de Casos de Uso

### Caso 1: Restricciones por Temporada Alta

```python
# Crear regla temporal para temporada alta
regla_temporada = ReglasReprogramacion.objects.create(
    nombre="Restricción temporada alta",
    tipo_regla="TIEMPO_MINIMO",
    aplicable_a="CLIENTE",
    valor_numerico=72,  # 72 horas
    fecha_inicio_vigencia=datetime(2025, 12, 15),
    fecha_fin_vigencia=datetime(2025, 1, 19),
    activa=True,
    prioridad=1,
    mensaje_error="Durante temporada alta se requieren 72 horas de anticipación"
)
```

### Caso 2: Servicios VIP con Reglas Especiales

```python
# Regla para servicios premium
regla_vip = ReglasReprogramacion.objects.create(
    nombre="Servicios VIP - Sin reprogramación",
    tipo_regla="SERVICIOS_RESTRINGIDOS",
    aplicable_a="CLIENTE",
    valor_texto='["Tour Premium Salar", "Expedición VIP Madidi"]',
    activa=True,
    prioridad=1,
    mensaje_error="Los servicios VIP no permiten reprogramación. Contacte a soporte."
)
```

### Caso 3: Horarios de Oficina

```python
# Solo reprogramar en horarios de oficina
regla_oficina = ReglasReprogramacion.objects.create(
    nombre="Solo horarios de oficina",
    tipo_regla="HORAS_BLACKOUT", 
    aplicable_a="CLIENTE",
    valor_texto='[0,1,2,3,4,5,6,7,18,19,20,21,22,23]',  # Solo 8am-6pm
    activa=True,
    prioridad=2,
    mensaje_error="Solo se puede reprogramar en horarios de oficina (8am - 6pm)"
)
```

## Testing de Reglas

### Tests Unitarios

```python
class TestReglasReprogramacion(TestCase):
    def test_tiempo_minimo_cliente(self):
        # Crear regla de 24 horas
        regla = ReglasReprogramacion.objects.create(
            tipo_regla='TIEMPO_MINIMO',
            aplicable_a='CLIENTE', 
            valor_numerico=24,
            activa=True
        )
        
        # Intentar reprogramar con 12 horas
        nueva_fecha = timezone.now() + timedelta(hours=12)
        serializer = ReprogramacionReservaSerializer(
            data={'nueva_fecha': nueva_fecha}
        )
        
        # Debe fallar la validación
        self.assertFalse(serializer.is_valid())
        self.assertIn('nueva_fecha', serializer.errors)
```

## Mejores Prácticas

### Configuración Recomendada

1. **Empezar simple**: Implementar reglas básicas primero
2. **Roles específicos**: Configurar reglas diferentes por rol
3. **Mensajes claros**: Usar mensajes de error descriptivos
4. **Prioridades lógicas**: Asignar prioridades según criticidad
5. **Testing exhaustivo**: Probar todas las combinaciones de reglas

### Mantenimiento

1. **Revisar periódicamente**: Evaluar efectividad de las reglas
2. **Actualizar según feedback**: Ajustar basado en quejas de usuarios
3. **Monitorear violaciones**: Identificar reglas problemáticas
4. **Documentar cambios**: Mantener historial de modificaciones

Este sistema de reglas dinámico permite una gestión flexible y potente de las políticas de reprogramación, adaptándose a diferentes necesidades de negocio y tipos de usuarios.