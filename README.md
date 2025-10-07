# OpenFGA: Implementación de Fine-Grained Authorization		

Este es el repositorio del curso de LinkedIn Learning `[OpenFGA: Implementación de Fine-Grained Authorization]`. El curso completo está disponible en [LinkedIn Learning][lil-course-url].

![OpenFGA: Implementación de Fine-Grained Authorization][lil-thumbnail-url] 

Consulta el archivo Readme en la rama main para obtener instrucciones e información actualizadas.

OpenFGA (Fine-Grained Authorization) es una solución de código abierto para la autorización granular inspirada en el sistema Zanzibar de Google. Resuelve uno de los problemas más complejos en aplicaciones modernas: cómo determinar qué usuarios pueden realizar qué acciones sobre qué recursos.
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

## Instrucciones

Este repositorio tiene ramas (branches) para cada uno de los vídeos del curso. Puedes usar el menú emergente de la rama en GitHub para cambiar a una rama específica y echar un vistazo al curso en esa etapa, o puedes añadir `/tree/nombre_de_la_rama` a la URL para ir a la rama a la que quieres acceder.

## Ramas

Las ramas están estructuradas para corresponder a los vídeos del curso. La convención de nomenclatura es Capítulo#_Vídeo#. Por ejemplo, la rama denominada `02_03` corresponde al segundo capítulo y al tercer vídeo de ese capítulo. Algunas ramas tendrán un estado inicial y otro final. Están marcadas con las letras i («inicio») y f («fin»). La branch i tiene el mismo código que al principio del vídeo. La branch f tiene el mismo código que al final del vídeo. La rama master tiene el estado final del código que aparece en el curso.

## Instalación

1. Para utilizar estos archivos de ejercicios, debes tener descargado lo siguiente:
   - [Docker](https://www.docker.com/get-started/)
   - Python 3.11+ (desarrollo local)

2. Clona este repositorio en tu máquina local usando la Terminal (macOS) o CMD (Windows), o una herramienta GUI como SourceTree.
3. Instrucciones 

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
      docker pull openfga/openfga
      docker run -p 8080:8080 -p 8081:8081 -p 3000:3000 openfga/openfga run
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
   - URL: http://localhost:3000/playground
   - Permite probar modelos visualmente
   - Útil para depuración y aprendizaje

### Docente

**Carla Urrea Stabile**

Echa un vistazo a mis otros cursos en [LinkedIn Learning](https://www.linkedin.com/learning/instructors/carla-urrea-stabile).

[0]: # (Replace these placeholder URLs with actual course URLs)
[lil-course-url]: https://www.linkedin.com/learning/openfga-implementacion-de-fine-grained-authorization
[lil-thumbnail-url]: https://media.licdn.com/dms/image/v2/D4E0DAQHXDdFv5CfHVA/learning-public-crop_675_1200/B4EZmfvPnnIMAc-/0/1759321586463?e=2147483647&v=beta&t=ml2D8-GQVM1_t0C3M1xzA0WkGJ6FzaeBN8k7wmKuGSo

[1]: # (End of ES-Instruction ###############################################################################################)
	
