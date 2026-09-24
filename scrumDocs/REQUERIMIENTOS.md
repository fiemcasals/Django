# Requerimientos -- django

_Generado automaticamente el 2026-09-24T17:33:54.165Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Arquitectura base modular y entorno Dockerizado con documentación didáctica

### RF-01: Configuración central y estructura modular de aplicaciones Django (Funcional)

Crear la estructura de carpetas modular (config/, apps/core/, templates/, static/). Entregar los archivos centrales (settings.py, urls.py, wsgi.py, asgi.py) y la app base con sus archivos obligatorios comentados didácticamente (models.py, views.py, forms.py, urls.py, admin.py, apps.py, tests.py). Incluir .env.example, .gitignore, requirements.txt y plantilla base.html. Condición de aprobación: python manage.py check con código 0 y servidor funcional sin secretos hardcodeados.
