"""
==============================================================================
config/wsgi.py - Web Server Gateway Interface
==============================================================================
Explicación para alumnos:
WSGI es el estándar de comunicación síncrona entre servidores web (como Nginx,
Apache o Gunicorn) y aplicaciones Python como Django.
No necesitas modificar este archivo.
==============================================================================
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
