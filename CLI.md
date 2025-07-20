# Cómo Ejecutar OpenFGA Localmente y Utilizar la Línea de Comandos

## Introducción

Este guía te enseñará cómo configurar OpenFGA localmente usando Docker y cómo utilizar las herramientas de línea de comandos (CLI) para interactuar con el servidor OpenFGA. Estas herramientas son fundamentales para desarrollar y probar modelos de autorización.

## Ejecución Local con Docker

### Opción 1: Docker Compose (Recomendado)

Ya tienes configurado `docker-compose.yml` en el proyecto. Para ejecutar OpenFGA:

```bash
# Ejecutar todos los servicios
docker-compose up -d

# Verificar que los contenedores están corriendo
docker-compose ps

# Ver logs de OpenFGA
docker-compose logs openfga

# Parar los servicios
docker-compose down
```

### Opción 2: Docker Run Directo

Si solo necesitas OpenFGA sin la aplicación FastAPI:

```bash
# Ejecutar OpenFGA con playground habilitado
docker run -d \
  --name openfga \
  -p 8080:8080 \
  -p 8081:8081 \
  openfga/openfga:v1.9.0 \
  run --playground-enabled

# Verificar que está corriendo
docker ps

# Ver logs
docker logs openfga

# Parar el contenedor
docker stop openfga
docker rm openfga
```

### Verificación de la Instalación

Una vez que OpenFGA esté corriendo, verifica que funciona correctamente:

```bash
# Verificar la API
curl http://localhost:8080/stores

# Debería retornar una lista vacía: {"stores":[]}
```

También puedes acceder al playground en: http://localhost:8081

## Instalación del CLI de OpenFGA

El CLI de OpenFGA (`fga`) es una herramienta poderosa para interactuar con OpenFGA desde la terminal.

### macOS

```bash
# Usando Homebrew
brew install openfga/tap/fga

# Verificar instalación
fga version
```

### Linux

```bash
# Descargar la última versión
curl -L https://github.com/openfga/cli/releases/latest/download/fga_linux_amd64.tar.gz | tar -xzf -

# Mover a PATH
sudo mv fga /usr/local/bin/

# Verificar instalación
fga version
```

### Windows

```bash
# Usando Chocolatey
choco install fga

# O descargar manualmente desde:
# https://github.com/openfga/cli/releases
```

### Instalación Manual

Si prefieres instalar manualmente:

1. Ve a https://github.com/openfga/cli/releases
2. Descarga la versión para tu sistema operativo
3. Extrae el archivo y colócalo en tu PATH

## Configuración del CLI

### Archivo de Configuración

El CLI puede usar un archivo de configuración para evitar repetir parámetros:

```bash
# Crear archivo de configuración
mkdir -p ~/.config/fga
cat > ~/.config/fga/config.yaml << EOF
api-url: http://localhost:8080
EOF
```

### Variables de Entorno

Alternativamente, puedes usar variables de entorno:

```bash
export FGA_API_URL=http://localhost:8080
export FGA_STORE_ID=<tu-store-id>
export FGA_MODEL_ID=<tu-model-id>
```

## Comandos Básicos del CLI

### 1. Crear un Store

Un "store" es un contenedor para tus modelos y datos de autorización:

```bash
# Crear un nuevo store
fga store create --name "LinkedIn Course Store"

# Ejemplo de respuesta:
# {
#   "id": "01HXX...",
#   "name": "LinkedIn Course Store",
#   "created_at": "2024-01-20T10:30:00Z",
#   "updated_at": "2024-01-20T10:30:00Z"
# }
```

### 2. Listar Stores

```bash
# Ver todos los stores
fga store list
```

### 3. Obtener Información de un Store

```bash
# Obtener detalles de un store específico
fga store get --store-id <store-id>
```

### 4. Configurar Store por Defecto

```bash
# Configurar el store para usar en comandos futuros
fga configure --store-id <store-id>
```

### 5. Crear un Modelo Básico

```bash
# Crear un archivo de modelo simple
cat > model.fga << 'EOF'
model
  schema 1.1

type user

type document
  relations
    define owner: [user]
    define viewer: [user]
    define can_read: viewer or owner
    define can_write: owner
EOF

# Aplicar el modelo
fga model write --file model.fga
```

### 6. Ver Modelos

```bash
# Listar todos los modelos del store
fga model list

# Ver un modelo específico
fga model get --model-id <model-id>
```

### 7. Trabajar con Tuplas (Relaciones)

```bash
# Crear una tupla (relación)
fga tuple write user:alice owner document:readme

# Leer tuplas
fga tuple read

# Eliminar una tupla
fga tuple delete user:alice owner document:readme
```

### 8. Verificar Permisos

```bash
# Verificar si un usuario tiene un permiso
fga query check user:alice can_read document:readme

# Ejemplo de respuesta:
# {
#   "allowed": true
# }
```

## Ejemplos Prácticos

### Ejemplo 1: Sistema Básico de Documentos

```bash
# 1. Crear store
STORE_ID=$(fga store create --name "Document System" --format json | jq -r .id)

# 2. Configurar CLI para usar este store
fga configure --store-id $STORE_ID

# 3. Crear modelo
cat > document-model.fga << 'EOF'
model
  schema 1.1

type user

type document
  relations
    define owner: [user]
    define viewer: [user]
    define can_read: viewer or owner
    define can_write: owner
EOF

# 4. Aplicar modelo
MODEL_ID=$(fga model write --file document-model.fga --format json | jq -r .authorization_model_id)

# 5. Crear algunas relaciones
fga tuple write user:alice owner document:readme
fga tuple write user:bob viewer document:readme

# 6. Verificar permisos
fga query check user:alice can_write document:readme  # true
fga query check user:bob can_write document:readme    # false
fga query check user:bob can_read document:readme     # true
```

### Ejemplo 2: Sistema con Equipos

```bash
# Crear modelo más complejo
cat > team-model.fga << 'EOF'
model
  schema 1.1

type user

type team
  relations
    define member: [user]
    define admin: [user]

type document
  relations
    define owner: [user, team#member]
    define viewer: [user, team#member]
    define can_read: viewer or owner
    define can_write: owner
EOF

# Aplicar modelo
fga model write --file team-model.fga

# Crear relaciones de equipo
fga tuple write user:alice member team:engineering
fga tuple write user:bob member team:engineering
fga tuple write user:charlie admin team:engineering

# Asignar permisos a nivel de equipo
fga tuple write team:engineering#member owner document:architecture-doc

# Verificar permisos
fga query check user:alice can_write document:architecture-doc  # true
fga query check user:bob can_write document:architecture-doc    # true
```

## Comandos Avanzados

### Importar/Exportar Datos

```bash
# Exportar todas las tuplas
fga tuple read --format json > tuplas-backup.json

# Importar tuplas desde archivo
fga tuple write --file tuplas-backup.json
```

### Validación de Modelos

```bash
# Validar un modelo antes de aplicarlo
fga model validate --file model.fga
```

### Transformaciones de Modelo

```bash
# Convertir modelo a diferentes formatos
fga model transform --file model.fga --format json
fga model transform --file model.fga --format yaml
```

### Consultas de Depuración

```bash
# Ver qué objetos puede acceder un usuario
fga query list-objects user:alice can_read document

# Ver qué usuarios tienen acceso a un objeto
fga query list-users can_read document:readme

# Expandir todas las relaciones de un objeto
fga query expand can_read document:readme
```

## Mejores Prácticas para el CLI

### 1. **Usar Archivos de Configuración**
```bash
# Crear configuración de proyecto
cat > fga-config.yaml << EOF
api-url: http://localhost:8080
store-id: ${STORE_ID}
model-id: ${MODEL_ID}
EOF

# Usar configuración específica
fga --config fga-config.yaml query check user:alice can_read document:readme
```

### 2. **Scripts de Automatización**
```bash
#!/bin/bash
# setup-demo.sh

set -e

echo "🚀 Configurando demo de OpenFGA..."

# Crear store
STORE_ID=$(fga store create --name "Demo Store" --format json | jq -r .id)
echo "✅ Store creado: $STORE_ID"

# Configurar CLI
fga configure --store-id $STORE_ID
echo "✅ CLI configurado"

# Aplicar modelo
MODEL_ID=$(fga model write --file model.fga --format json | jq -r .authorization_model_id)
echo "✅ Modelo aplicado: $MODEL_ID"

# Cargar datos de demo
fga tuple write --file demo-data.json
echo "✅ Datos de demo cargados"

echo "🎉 Demo listo!"
```

### 3. **Validación y Testing**
```bash
# Script de testing
#!/bin/bash
# test-permissions.sh

echo "🧪 Probando permisos..."

test_permission() {
    local user=$1
    local permission=$2
    local object=$3
    local expected=$4
    
    result=$(fga query check $user $permission $object --format json | jq -r .allowed)
    
    if [ "$result" = "$expected" ]; then
        echo "✅ $user $permission $object: $result"
    else
        echo "❌ $user $permission $object: esperado $expected, obtenido $result"
        exit 1
    fi
}

# Casos de prueba
test_permission "user:alice" "can_write" "document:readme" "true"
test_permission "user:bob" "can_write" "document:readme" "false"
test_permission "user:bob" "can_read" "document:readme" "true"

echo "🎉 Todos los tests pasaron!"
```

## Troubleshooting Común

### Error de Conexión
```bash
# Verificar que OpenFGA está corriendo
curl http://localhost:8080/stores

# Si falla, verificar Docker
docker-compose ps
docker-compose logs openfga
```

### Store No Encontrado
```bash
# Verificar stores disponibles
fga store list

# Reconfigurar CLI
fga configure --store-id <store-id-correcto>
```

### Modelo Inválido
```bash
# Validar modelo antes de aplicar
fga model validate --file model.fga

# Ver errores detallados
fga model write --file model.fga --verbose
```

## Recursos Útiles

- **Documentación CLI**: https://github.com/openfga/cli
- **Ejemplos de Modelos**: https://openfga.dev/docs/modeling
- **Playground Online**: https://play.fga.dev/
- **Sintaxis DSL**: https://openfga.dev/docs/configuration-language

---

Con esta configuración, tienes un entorno completo para desarrollar y probar modelos de autorización con OpenFGA. En el siguiente video, comenzaremos a modelar escenarios de autorización más complejos usando el DSL de OpenFGA.