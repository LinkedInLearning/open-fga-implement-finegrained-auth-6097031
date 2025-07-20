# OpenFGA con FastAPI - Curso de LinkedIn

## ¿Qué es OpenFGA y por qué usarlo?

### Introducción

**OpenFGA (Fine-Grained Authorization)** es una solución de código abierto para la autorización granular inspirada en el sistema Zanzibar de Google. Resuelve uno de los problemas más complejos en aplicaciones modernas: **cómo determinar qué usuarios pueden realizar qué acciones sobre qué recursos**.

### Problemas que Resuelve OpenFGA

#### 1. **Autorización Compleja y Escalable**
En aplicaciones tradicionales, las reglas de autorización suelen estar dispersas en el código, lo que genera:
- Código difícil de mantener
- Reglas inconsistentes
- Dificultad para auditar permisos
- Problemas de escalabilidad

#### 2. **Permisos Granulares**
OpenFGA permite definir permisos específicos como:
- "El usuario Alice puede **editar** el documento X"
- "El usuario Bob puede **ver** todos los documentos de la carpeta Y"
- "Los miembros del equipo Marketing pueden **comentar** en los documentos públicos"

#### 3. **Relaciones Dinámicas**
Maneja relaciones complejas como:
- Herencia de permisos (si tienes acceso a la carpeta, tienes acceso a sus documentos)
- Roles contextuales (eres admin en el proyecto A, pero viewer en el proyecto B)
- Permisos temporales o condicionales

### Beneficios de OpenFGA

#### ✅ **Separación de Responsabilidades**
- La lógica de autorización está separada de la lógica de negocio
- Los cambios en permisos no requieren cambios en el código de la aplicación

#### ✅ **Flexibilidad y Expresividad**
- Modela cualquier tipo de relación y permiso
- Soporte para reglas complejas usando su DSL (Domain Specific Language)

#### ✅ **Performance y Escalabilidad**
- Optimizado para consultas rápidas de autorización
- Diseñado para manejar millones de relaciones

#### ✅ **Auditabilidad**
- Todas las decisiones de autorización son rastreables
- Facilita el cumplimiento de regulaciones (GDPR, SOX, etc.)

#### ✅ **Interoperabilidad**
- API REST estándar
- SDKs disponibles para múltiples lenguajes
- Fácil integración con aplicaciones existentes

### Arquitectura de OpenFGA

OpenFGA se basa en tres conceptos fundamentales:

1. **Modelo de Autorización**: Define los tipos de objetos, relaciones y permisos
2. **Tuplas**: Representan las relaciones específicas (ej: "user:alice has relation owner on object:doc1")
3. **Consultas**: Verifican si un usuario tiene permiso para realizar una acción

### Casos de Uso Comunes

- **Aplicaciones SaaS**: Control de acceso por inquilino y roles
- **Sistemas de Gestión Documental**: Permisos granulares por documento/carpeta
- **Plataformas Colaborativas**: Gestión de equipos y proyectos
- **APIs y Microservicios**: Autorización centralizada y consistente

## Estructura del Proyecto

Este proyecto FastAPI evoluciona a lo largo del curso para demostrar las capacidades de OpenFGA:

```
openfga-fastapi-linkedin/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── database.py          # Configuración de base de datos
│   ├── models/              # Modelos SQLAlchemy
│   ├── routes/              # Endpoints de la API
│   └── services/            # Lógica de negocio y OpenFGA
├── docker-compose.yml       # Orquestación de servicios
├── Dockerfile               # Imagen de la aplicación
├── requirements.txt         # Dependencias Python
├── .env.example             # Variables de entorno
└── README.md                # Este archivo
```

## Configuración y Ejecución

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)
- Git

### Ejecutar con Docker (Recomendado)

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd openfga-fastapi-linkedin
   ```

2. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env según sea necesario
   ```

3. **Ejecutar los servicios**:
   ```bash
   docker-compose up -d
   ```

4. **Verificar que todo funciona**:
   - FastAPI: http://localhost:8000
   - OpenFGA API: http://localhost:8080
   - OpenFGA Playground: http://localhost:8081

### Desarrollo Local

1. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar OpenFGA**:
   ```bash
   docker run -p 8080:8080 -p 8081:8081 openfga/openfga:v1.9.0 run --playground-enabled
   ```

4. **Ejecutar la aplicación**:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

## Herramientas de Desarrollo

### OpenFGA CLI

El CLI de OpenFGA es una herramienta esencial para el desarrollo:

```bash
# Instalar (macOS)
brew install openfga/tap/fga

# Instalar (Linux/Windows)
# Descargar desde: https://github.com/openfga/cli/releases
```

### OpenFGA Playground

Interfaz web para experimentar con modelos y consultas:
- URL: http://localhost:8081
- Permite probar modelos visualmente
- Útil para depuración y aprendizaje

## Progresión del Curso

Este proyecto evoluciona a través de 6 secciones:

1. **Fundamentos**: Configuración y conceptos básicos
2. **Modelado**: Definición de tipos, relaciones y permisos
3. **Gestión de Datos**: Crear y manejar tuplas (relaciones)
4. **Consultas**: Verificación de permisos y optimizaciones
5. **Patrones Avanzados**: Jerarquías, CI/CD y monitoreo
6. **Producción**: Mejores prácticas y escalabilidad

## Recursos Adicionales

- [Documentación Oficial de OpenFGA](https://openfga.dev/)
- [Especificación de Zanzibar (Google)](https://research.google/pubs/pub48190/)
- [Playground Online de OpenFGA](https://play.fga.dev/)
- [Comunidad de OpenFGA](https://github.com/openfga/community)

---

**Nota**: Este es un proyecto educativo del curso "Autorización Avanzada con OpenFGA" de LinkedIn Learning.