# Requerimientos -- django

_Generado automaticamente el 2026-09-24T17:35:34.550Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Arquitectura base modular y entorno Dockerizado con documentación didáctica

### RF-01: Configuración central y estructura modular de aplicaciones Django (Funcional)

Crear la estructura de carpetas modular (config/, apps/core/, templates/, static/). Entregar los archivos centrales (settings.py, urls.py, wsgi.py, asgi.py) y la app base con sus archivos obligatorios comentados didácticamente (models.py, views.py, forms.py, urls.py, admin.py, apps.py, tests.py). Incluir .env.example, .gitignore, requirements.txt y plantilla base.html. Condición de aprobación: python manage.py check con código 0 y servidor funcional sin secretos hardcodeados.

### RNF-01: Contenerización del entorno con Docker, docker-compose y PostgreSQL (No funcional)

Crear el archivo Dockerfile optimizado (Python 3.12) y docker-compose.yml que orqueste el servicio web (Django) y el servicio db (PostgreSQL 16) con volumen persistente para datos y variables de entorno vinculadas. Crear .dockerignore y script de espera para la base de datos. Actualizar el archivo README.md con los comandos exactos paso a paso (docker compose up --build, ejecución de migraciones y creación de superusuario). Entregables: Dockerfile, docker-compose.yml, .dockerignore, README.md. Condición de aprobación: docker compose up levanta ambos servicios, conecta a PostgreSQL y responde HTTP 200 en http://localhost:8000.
