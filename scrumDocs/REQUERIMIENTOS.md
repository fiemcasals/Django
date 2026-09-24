# Requerimientos -- django

_Generado automaticamente el 2026-09-24T17:37:36.548Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Arquitectura base modular y entorno Dockerizado con documentación didáctica

### RF-01: Configuración central y estructura modular de aplicaciones Django (Funcional)

Crear la estructura de carpetas modular (config/, apps/core/, templates/, static/). Entregar los archivos centrales (settings.py, urls.py, wsgi.py, asgi.py) y la app base con sus archivos obligatorios comentados didácticamente (models.py, views.py, forms.py, urls.py, admin.py, apps.py, tests.py). Incluir .env.example, .gitignore, requirements.txt y plantilla base.html. Condición de aprobación: python manage.py check con código 0 y servidor funcional sin secretos hardcodeados.

### RNF-01: Contenerización del entorno con Docker, docker-compose y PostgreSQL (No funcional)

Crear el archivo Dockerfile optimizado (Python 3.12) y docker-compose.yml que orqueste el servicio web (Django) y el servicio db (PostgreSQL 16) con volumen persistente para datos y variables de entorno vinculadas. Crear .dockerignore y script de espera para la base de datos. Actualizar el archivo README.md con los comandos exactos paso a paso (docker compose up --build, ejecución de migraciones y creación de superusuario). Entregables: Dockerfile, docker-compose.yml, .dockerignore, README.md. Condición de aprobación: docker compose up levanta ambos servicios, conecta a PostgreSQL y responde HTTP 200 en http://localhost:8000.

## HU-02: Módulo didáctico interactivo (Manual del Alumno) con mecanismo de activación u ocultamiento

### RF-01: Módulo interactivo de Guía/Manual del Alumno con switch de activación (Funcional)

Crear una aplicación independiente (apps/manual/) con vistas y plantillas que expliquen interactivamente la arquitectura de Django (MVT, flujo de peticiones y comandos de terminal). El módulo debe activarse o desactivarse mediante la variable de entorno ENABLE_STUDENT_MANUAL. Si está inactivo, las rutas deben quedar inaccesibles (404) y ocultar los links del menú. Todo el código de la app debe estar desacoplado para permitir su eliminación limpia sin romper el proyecto. Entregables: apps/manual/ (apps.py, views.py, urls.py) y templates/manual/ (index.html, arquitectura.html, comandos.html). Condición de aprobación: con ENABLE_STUDENT_MANUAL=True el manual es navegable en /manual/; con False retorna 404 y se oculta del navbar; remover la app no rompe el resto del sistema.
