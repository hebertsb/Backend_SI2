# 📋 Documentación del Sistema de Reprogramación de Reservas

Este directorio contiene la documentación completa del sistema de reprogramación de reservas, incluyendo las reglas de negocio y el sistema de notificaciones.

## 📁 Documentos Disponibles

### 🔧 [Reglas de Reprogramación](./REGLAS_REPROGRAMACION_RESERVAS.md)
**Descripción**: Sistema completo de reglas configurables que controlan cuándo y cómo se pueden reprogramar las reservas.

**Incluye**:
- ✅ 12 tipos de reglas diferentes (tiempo, cantidad, días, servicios, etc.)
- ✅ Aplicabilidad por roles (cliente, operador, admin)
- ✅ Sistema de prioridades
- ✅ API para gestión de reglas
- ✅ Configuraciones típicas para agencias turísticas
- ✅ Validaciones automáticas
- ✅ Ejemplos de implementación

### 📧 [Sistema de Notificaciones](./NOTIFICACIONES_REPROGRAMACION.md)
**Descripción**: API y configuración para envío automático de notificaciones por email cuando se realizan reprogramaciones.

**Incluye**:
- ✅ Clase `NotificacionReprogramacion` completa
- ✅ Configuración SMTP para Gmail
- ✅ Templates HTML profesionales
- ✅ Integración con endpoints de reprogramación
- ✅ Sistema de logging y monitoreo
- ✅ Manejo de errores

### 🔄 [Flujo de Notificaciones](./FLUJO_NOTIFICACIONES_REPROGRAMACION.md)
**Descripción**: Diagramas y explicación detallada del flujo completo desde la solicitud hasta el envío de notificaciones.

**Incluye**:
- ✅ Diagrama de flujo general
- ✅ Proceso de email para clientes
- ✅ Notificaciones web para soporte
- ✅ Manejo de errores y reintentos
- ✅ Métricas y monitoreo
- ✅ Testing del sistema

### 🌐 [Integración Frontend](./INTEGRACION_FRONTEND_NOTIFICACIONES.md)
**Descripción**: Guía completa para implementar notificaciones web en tiempo real para el equipo de soporte.

**Incluye**:
- ✅ HTTP Polling con React
- ✅ WebSockets en tiempo real
- ✅ Componentes frontend completos
- ✅ Panel de control para soporte
- ✅ Configuración de producción
- ✅ Testing de integración

### 📝 [Ejemplos y Templates](./EJEMPLOS_PAYLOADS_TEMPLATES.md)
**Descripción**: Ejemplos prácticos de payloads, templates HTML y configuraciones.

**Incluye**:
- ✅ Payloads JSON completos
- ✅ Templates HTML responsivos
- ✅ Templates de texto plano
- ✅ Variables de contexto
- ✅ Configuración de testing

## 🎯 Guía de Implementación Rápida

### 1. Configurar Reglas Básicas
```sql
-- Tiempo mínimo 24h para clientes
INSERT INTO reservas_reglasreprogramacion (nombre, tipo_regla, aplicable_a, valor_numerico, activa, mensaje_error)
VALUES ('Anticipación 24h', 'TIEMPO_MINIMO', 'CLIENTE', 24, true, 'Debe reprogramar con 24h de anticipación');

-- Máximo 3 reprogramaciones
INSERT INTO reservas_reglasreprogramacion (nombre, tipo_regla, aplicable_a, valor_numerico, activa, mensaje_error)  
VALUES ('Límite 3 reprogramaciones', 'LIMITE_REPROGRAMACIONES', 'CLIENTE', 3, true, 'Máximo 3 reprogramaciones por reserva');
```

### 2. Configurar Email
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
ADMIN_EMAILS=admin@tuagencia.com,soporte@tuagencia.com
```

### 3. Implementar Frontend (Básico)
```javascript
// Polling cada 30 segundos para notificaciones
setInterval(async () => {
    const response = await fetch('/api/reservas/notificaciones/soporte/');
    const data = await response.json();
    mostrarNotificaciones(data.notificaciones);
}, 30000);
```

## 🔗 Relación entre Componentes

```
┌─────────────────────┐    ┌─────────────────────┐
│   REGLAS DE         │    │   SISTEMA DE        │
│   REPROGRAMACIÓN    │───▶│   NOTIFICACIONES    │
│                     │    │                     │
│ • Validaciones      │    │ • Email Clientes    │
│ • Restricciones     │    │ • Web Soporte       │
│ • Políticas         │    │ • Templates         │
└─────────────────────┘    └─────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐
│   ENDPOINTS API     │    │   FRONTEND          │
│                     │    │                     │
│ • /reprogramar/     │    │ • Dashboard         │
│ • /reglas/          │    │ • Notificaciones    │
│ • /notificaciones/  │    │ • Panel Soporte     │
└─────────────────────┘    └─────────────────────┘
```

## 📋 Checklist de Implementación

### Backend ✅
- [ ] Configurar variables de entorno para email
- [ ] Crear reglas básicas de reprogramación  
- [ ] Configurar templates de email
- [ ] Probar endpoints de reprogramación
- [ ] Verificar logs de notificaciones

### Frontend 🌐
- [ ] Implementar componente de notificaciones
- [ ] Configurar polling o WebSockets
- [ ] Crear panel de soporte
- [ ] Integrar con sistema de autenticación
- [ ] Probar notificaciones en tiempo real

### Testing 🧪
- [ ] Tests unitarios de reglas
- [ ] Tests de integración de notificaciones
- [ ] Tests de endpoints de reprogramación
- [ ] Tests de frontend con mocks
- [ ] Tests de performance

### Producción 🚀
- [ ] Configurar servidor SMTP
- [ ] Configurar Redis para WebSockets
- [ ] Configurar Nginx para WebSockets
- [ ] Monitoreo de logs
- [ ] Métricas de notificaciones

## 🆘 Soporte y Resolución de Problemas

### Errores Comunes

1. **Email no se envía**
   - Verificar credenciales SMTP
   - Revisar `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`
   - Comprobar configuración 2FA de Gmail

2. **Reglas no se aplican**
   - Verificar que la regla esté `activa=True`
   - Comprobar el `aplicable_a` corresponde al rol del usuario
   - Revisar orden de prioridades

3. **Notificaciones web no funcionan**
   - Verificar permisos de usuario
   - Comprobar token de autenticación
   - Revisar configuración CORS

### Logs Importantes

```bash
# Ver logs de notificaciones
tail -f logs/notificaciones.log

# Ver logs de Django
python manage.py runserver --verbosity=2

# Ver logs de Celery (si se usa)
celery -A backend worker --loglevel=info
```

## 📞 Contacto

Para dudas sobre implementación o problemas técnicos, revisar:

1. **Documentación técnica**: Archivos individuales en este directorio
2. **Código fuente**: 
   - `reservas/models.py` - Modelos de reglas
   - `reservas/serializers.py` - Validaciones
   - `reservas/notifications.py` - Sistema de emails
   - `reservas/views.py` - Endpoints API

3. **Testing**: 
   - `reservas/tests/` - Tests automatizados
   - `scripts/` - Scripts de utilidad

---

📅 **Última actualización**: Septiembre 2025  
🔧 **Versión del sistema**: Django 4.2+  
📧 **Compatible con**: Gmail SMTP, SendGrid, AWS SES