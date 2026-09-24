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

    # Incluimos las rutas de la app principal 'core' en la raíz (/)
    path('', include('apps.core.urls', namespace='core')),
]

# En modo DEBUG, le decimos a Django que sirva los archivos estáticos y media directamente
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
