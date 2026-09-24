"""
==============================================================================
config/urls.py - Enrutador Principal del Proyecto
==============================================================================
Explicación para alumnos:
Este archivo es el mapa central de URLs de tu sitio web.
Cuando un usuario ingresa una dirección en el navegador (ej: http://localhost:8000/contacto/),
Django busca en este archivo qué vista (view) debe responder a esa petición.

Buenas prácticas en Django:
1. 'include()': En lugar de definir todas las rutas acá, cada aplicación define sus
   propias rutas en su archivo 'urls.py' local, y acá simplemente las "incluimos".
2. 'admin/': Ruta prefabricada de Django para gestionar la base de datos visualmente.
==============================================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django (http://localhost:8000/admin/)
    path('admin/', admin.site.urls),

    # Módulo interactivo de Guía/Manual del Alumno (/manual/)
    path('manual/', include('apps.manual.urls', namespace='manual')),

    # Incluimos las rutas de la app principal 'core' en la raíz (/)
    path('', include('apps.core.urls', namespace='core')),
]

# ------------------------------------------------------------------------------
# SERVICIO DE ARCHIVOS ESTÁTICOS Y MEDIA EN DESARROLLO (DEBUG = True)
# ------------------------------------------------------------------------------
# Explicación para alumnos:
# ¿Para qué sirve este bloque 'if settings.DEBUG'?
#
# 1. En DESARROLLO (DEBUG = True):
#    El servidor de desarrollo de Django ('python manage.py runserver') no entrega
#    archivos estáticos ni archivos subidos por usuarios (Media) por defecto.
#    La función 'static()' le dice a Django:
#    - "Cuando el navegador pida '/static/css/styles.css', buscalo en STATIC_ROOT o STATICFILES_DIRS y entregalo."
#    - "Cuando pida '/media/foto.jpg', buscalo en la carpeta MEDIA_ROOT y entregalo."
#
# 2. En PRODUCCIÓN (DEBUG = False):
#    Por motivos de rendimiento y seguridad, Django NUNCA debe entregar archivos estáticos
#    en un servidor real. Esa tarea se delega a servidores web de alto rendimiento como
#    Nginx, Caddy o servicios de almacenamiento en la nube (ej. Amazon S3 / Google Cloud Storage).
#    Por eso este bloque sólo se activa cuando DEBUG es True.
# ------------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
