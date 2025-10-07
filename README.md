# 🌟 Sistema de Reservas Turísticas - Bolivia
### Universidad Autónoma Gabriel René Moreno - Sistema de Información II

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

**API REST completa para gestión de reservas turísticas en Bolivia**

[Documentación API](#-documentación-api) • [Instalación](#-instalación) • [Arquitectura](#-arquitectura) • [Contribuir](#-contribución)

</div>

---

## 📖 Descripción del Proyecto

**Sistema de Reservas Turísticas** es una plataforma web desarrollada como proyecto final para la materia **Sistema de Información II** de la Universidad Autónoma Gabriel René Moreno. 

El sistema permite gestionar de manera integral las reservas de servicios turísticos en Bolivia, incluyendo paquetes turísticos, servicios individuales, usuarios, descuentos y un completo sistema de reprogramaciones.

### 🎯 Objetivo Principal
Crear una solución tecnológica robusta que facilite la gestión de reservas turísticas, optimizando la experiencia tanto para operadores turísticos como para clientes.

---

## ✨ Características Principales

### 🔐 **Autenticación y Autorización**
- ✅ Sistema de usuarios con roles (Cliente, Operador, Admin)
- ✅ Autenticación JWT con refresh tokens
- ✅ Gestión de permisos por roles
- ✅ Perfiles de usuario completos

### 🏞️ **Catálogo Turístico**
- ✅ Gestión de servicios turísticos individuales
- ✅ Paquetes turísticos con múltiples servicios
- ✅ Categorización y clasificación de servicios
- ✅ Sistema de calificaciones y reseñas

### 📋 **Sistema de Reservas**
- ✅ Reservas de servicios individuales y paquetes
- ✅ **Detección automática de paquetes** vs servicios
- ✅ Gestión de acompañantes y titulares
- ✅ Cálculo automático de precios para múltiples personas
- ✅ Estados de reserva (Pendiente, Pagada, Cancelada)

### 🔄 **Reprogramaciones Avanzadas**
- ✅ Sistema completo de reprogramación de reservas
- ✅ Reglas dinámicas configurables
- ✅ Historial completo de cambios
- ✅ Notificaciones automáticas por email
- ✅ Políticas de reprogramación por roles

### 💰 **Gestión Comercial**
- ✅ Sistema de cupones y descuentos
- ✅ Múltiples monedas (BOB, USD)
- ✅ Cálculo automático de precios
- ✅ Gestión de promociones

### 📧 **Comunicaciones**
- ✅ Notificaciones por email
- ✅ Templates HTML personalizables
- ✅ Confirmaciones de reserva
- ✅ Alertas de reprogramación

---

## 🏗️ Arquitectura del Sistema

### **Backend (Django REST Framework)**
```
📁 backend/
├── 🔐 authz/          # Autenticación y autorización
├── 📊 catalogo/       # Servicios y paquetes turísticos  
├── 📋 reservas/       # Sistema de reservas y reprogramaciones
├── 🎫 cupones/        # Cupones y descuentos
├── 💰 descuentos/     # Gestión de promociones
├── 🛠️  core/          # Utilidades compartidas
├── 💬 soporte/        # Sistema de soporte al cliente
└── 📧 templates/      # Templates de email
```

### **Base de Datos**
- **PostgreSQL**: Base de datos principal
- **Migraciones**: Control de versiones de BD
- **Seeders**: Datos iniciales para desarrollo

### **APIs y Documentación**
- **Django REST Framework**: Framework principal
- **Swagger/OpenAPI**: Documentación automática
- **drf-spectacular**: Generación de esquemas

---

## 🚀 Instalación

### **Requisitos Previos**
- Python 3.8+
- PostgreSQL 12+
- Git

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/hebertsb/Backend_SI2.git
cd Backend_SI2
```

### **2. Crear Entorno Virtual**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

**Ejemplo de `.env`:**
```env
DEBUG=True
SECRET_KEY=tu_secret_key_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/reservas_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

### **4. ⚡ Setup Ultra Simplificado**

**🎯 UN SOLO COMANDO PARA TODO:**
```bash
# Setup completo: migraciones + datos de prueba + configuración
python manage.py setup_database --reset
```

**✅ Este comando automáticamente:**
- Ejecuta todas las migraciones de Django
- Corrige problemas en fixtures automáticamente
- Carga usuarios con autenticación JWT
- Carga catálogo de servicios turísticos
- Carga reservas de prueba con reprogramaciones
- Configura descuentos y cupones
- ¡Deja el sistema listo para usar!

**📋 Opciones adicionales:**
```bash
python manage.py setup_database --help           # Ver ayuda completa
python manage.py setup_database --fixtures-only  # Solo recargar datos
python manage.py setup_database --no-fixtures    # Solo migraciones
```

**⚙️ Método Manual (Solo si necesitas control detallado):**
```bash
python manage.py makemigrations
python manage.py migrate
# Los fixtures se cargan automáticamente con el comando setup_database
```

### **6. Crear Superusuario**
```bash
python manage.py createsuperuser
```

### **7. Ejecutar el Servidor**
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

---

## �️ Comandos Útiles

### **🚀 Comando Principal: setup_database**

El comando `setup_database` es la herramienta principal para inicializar y mantener la base de datos del proyecto. Realiza todas las correcciones necesarias automáticamente.

```bash
# Setup completo (migraciones + fixtures)
python manage.py setup_database --reset

# Solo cargar fixtures (útil durante desarrollo)
python manage.py setup_database --fixtures-only

# Solo ejecutar migraciones sin datos
python manage.py setup_database --no-fixtures

# Ver ayuda completa
python manage.py setup_database --help
```

**🎯 Beneficios del Comando Unificado:**
- ⚡ **95% menos comandos**: De 15+ comandos a 1 solo
- 🔧 **Corrección automática**: Arregla problemas en fixtures
- 📊 **Datos consistentes**: Carga completa garantizada
- 🚀 **Setup en segundos**: No más procesos largos y manuales

**📊 Datos que Carga Automáticamente:**
- ✅ 4 Usuarios con diferentes roles y autenticación
- ✅ 4 Roles del sistema (Admin, Cliente, Operador, Soporte)
- ✅ 10+ Servicios turísticos con precios
- ✅ Paquetes turísticos completos
- ✅ Cupones y descuentos configurados
- ✅ Reservas de prueba con reprogramaciones
- ✅ Reglas de negocio del sistema

### **🔄 Scripts Automatizados (Usan el comando unificado)**
```bash
# PowerShell (Windows) - Usa automáticamente setup_database
.\scripts\setup_after_clone.ps1 -CreateVenv -InstallDeps -RunMigrations -LoadData

# Bash (Linux/Mac) - Usa automáticamente setup_database  
./scripts/setup_after_clone.sh
```

---

## �📚 Documentación API

### **Endpoints Principales**

#### 🔐 **Autenticación**
```
POST /api/auth/login/          # Iniciar sesión
POST /api/auth/refresh/        # Renovar token
POST /api/auth/register/       # Registrar usuario
POST /api/auth/logout/         # Cerrar sesión
```

#### 📋 **Reservas**
```
GET    /api/reservas/          # Listar reservas
POST   /api/reservas/          # Crear reserva
GET    /api/reservas/{id}/     # Detalle de reserva
PUT    /api/reservas/{id}/     # Actualizar reserva
DELETE /api/reservas/{id}/     # Cancelar reserva
```

#### 🔄 **Reprogramaciones**
```
POST /api/reservas/{id}/reprogramar/     # Reprogramar reserva
GET  /api/reservas/{id}/historial/       # Historial de cambios
GET  /api/reglas-reprogramacion/         # Reglas activas
```

#### 🏞️ **Catálogo**
```
GET /api/servicios/            # Listar servicios
GET /api/paquetes/             # Listar paquetes
GET /api/categorias/           # Listar categorías
```

### **Documentación Interactiva**
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **Schema JSON**: `http://localhost:8000/api/schema/`

---

## 🧪 Testing

### **Ejecutar Pruebas**
```bash
python manage.py test
```

### **Cobertura de Pruebas**
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### **Pruebas con Postman**
Se incluye una colección de Postman en `docs/postman/` con ejemplos de todos los endpoints.

---

## 🔧 Características Técnicas Avanzadas

### **⚡ Optimizaciones de Rendimiento**
- Lazy loading en relaciones
- Paginación automática
- Caché de consultas frecuentes
- Índices de base de datos optimizados

### **🛡️ Seguridad**
- Validación de entrada robusta
- Sanitización de datos
- Rate limiting en APIs críticas
- Logs de auditoría completos

### **📊 Funcionalidades Destacadas**

#### **Detección Automática de Paquetes**
El sistema incluye una innovadora funcionalidad que detecta automáticamente si una reserva corresponde a un paquete turístico o servicios individuales:

```python
# El frontend envía: total=2400, cantidad=2
# El sistema detecta automáticamente:
# - Paquete "Bolivia Complete Tour" = $2400 total
# - Calcula: $1200 por persona × 2 = $2400 ✅ Correcto
```

#### **Sistema de Reglas Dinámicas**
Configuración flexible de políticas de reprogramación:
- Tiempo mínimo de anticipación
- Límites de reprogramaciones por usuario
- Días y horas bloqueados
- Penalizaciones por cambios

---

## 📁 Estructura del Proyecto

```
📦 Backend_SI2/
├── 📁 authz/                    # Autenticación y autorización
│   ├── models.py               # Modelos de Usuario y Rol
│   ├── serializers.py          # Serializadores JWT
│   ├── views.py                # Vistas de autenticación
│   └── jwt_views.py            # Lógica JWT personalizada
├── 📁 catalogo/                 # Catálogo turístico
│   ├── models.py               # Servicios, Paquetes, Categorías
│   ├── serializers.py          # Serializadores del catálogo
│   └── views.py                # APIs del catálogo
├── 📁 reservas/                 # Sistema de reservas
│   ├── models.py               # Reservas, Reprogramaciones, Reglas
│   ├── serializers.py          # Lógica de negocio compleja
│   ├── views.py                # APIs de reservas
│   └── signals.py              # Señales y notificaciones
├── 📁 cupones/                  # Sistema de cupones
├── 📁 descuentos/               # Gestión de descuentos
├── 📁 soporte/                  # Sistema de soporte
├── 📁 templates/                # Templates de email
│   └── emails/                 # Plantillas HTML para notificaciones
├── 📁 scripts/                  # Scripts de utilidad
├── 📁 docs/                     # Documentación adicional
├── 📄 requirements.txt          # Dependencias Python
├── 📄 manage.py                # Comando principal Django
└── ⚙️ .env.example             # Variables de entorno
```

---

## 🌍 Variables de Entorno

### **Base de Datos**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db_name
```

### **Email**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
EMAIL_USE_TLS=True
```

### **Seguridad**
```env
SECRET_KEY=tu_secret_key_muy_segura_aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### **CORS y Frontend**
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://tu-frontend.com
CSRF_TRUSTED_ORIGINS=https://tu-frontend.com
```

---

## 🚀 Despliegue

### **Docker (Recomendado)**
```bash
# Construir imagen
docker build -t reservas-backend .

# Ejecutar contenedor
docker run -p 8000:8000 reservas-backend
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/reservas
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: reservas
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
```

### **Heroku**
```bash
heroku create tu-app-reservas
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
```

---

## 🎯 Para Desarrolladores Frontend

### **🚀 Setup Rápido para Integración**
```bash
# 1. Setup del backend completo en 1 comando
python manage.py setup_database --reset

# 2. Iniciar servidor
python manage.py runserver

# 3. API Lista en: http://127.0.0.1:8000/api/
```

### **📱 Credenciales de Prueba (Cargadas automáticamente)**
```
Admin:    gabriel.moreno@autonoma.edu.bo / admin123
Usuario:  juan.perez@autonoma.edu.bo / admin123  
Operador: maria.lopez@autonoma.edu.bo / admin123
Soporte:  soporte@autonoma.edu.bo / admin123
```

### **🔗 Documentación para Frontend**
- **`FRONTEND_UPDATE_GUIDE.txt`**: Endpoints detallados de reprogramaciones
- **`prompt_integracion_frontend.txt`**: Guía de roles y permisos
- **API Base**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## 🤝 Contribución

### **🚀 Setup para Nuevos Desarrolladores**
```bash
# Setup completo en 4 comandos
git clone https://github.com/hebertsb/Backend_SI2.git
cd Backend_SI2
pip install -r requirements.txt
python manage.py setup_database --reset
python manage.py runserver
```

### **Estándares de Código**
- Seguir PEP 8 para Python
- Usar el comando `setup_database` para pruebas
- Documentar nuevas funcionalidades
- Escribir tests para cambios críticos

### **Reportar Issues**
Incluye en tu reporte:
- Descripción del problema
- Comando que ejecutaste
- Output del comando `setup_database`
- Versión de Python/Django

---

## 📄 Información del Proyecto

**Universidad**: Universidad Autónoma Gabriel René Moreno  
**Materia**: Sistema de Información II  
**Año**: 2024  
**Tecnologías**: Django 5.2.6, Python 3.12, SQLite/PostgreSQL  

**🎯 Objetivo Académico**: Demostrar competencias en desarrollo de APIs REST, autenticación JWT, modelado de datos y arquitectura de software.

---

## 👥 Equipo de Desarrollo

### **Estudiantes**
- **Nombre**: [Hebert Suarez Burgos,]
- **Carrera**: Ingeniería Informática
- **Universidad**: Universidad Autónoma Gabriel René Moreno
- **Materia**: Sistema de Información II
- **Gestión**: 2025

### **Docente**
- **Profesor**: [Nombre del Profesor]
- **Materia**: Sistema de Información II

---

## 📞 Contacto y Soporte

### **Contacto Académico**
- **Email**: [tu-email@est.uagrm.edu.bo]
- **GitHub**: [@hebertsb](https://github.com/hebertsb)

### **Documentación Adicional**
- [Guía de Instalación Detallada](docs/INSTALLATION.md)
- [Manual de Usuario](docs/USER_GUIDE.md)
- [Documentación Técnica](docs/TECHNICAL_DOCS.md)
- [Changelog](CHANGELOG.md)

---

<div align="center">

### ⭐ ¡Si te gusta el proyecto, no olvides darle una estrella! ⭐

**Desarrollado con ❤️ para Sistema de Información II**  
**Universidad Autónoma Gabriel René Moreno - 2025**

</div>