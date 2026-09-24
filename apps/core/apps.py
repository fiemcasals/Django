"""
==============================================================================
apps/core/apps.py - Configuración de la Aplicación Core
==============================================================================
Explicación para alumnos:
En este archivo se define la clase 'CoreConfig', que hereda de AppConfig.
Django usa esta clase para registrar la aplicación en settings.INSTALLED_APPS.
- 'name': Nombre del módulo Python (en este caso 'core').
- 'verbose_name': Nombre legible para humanos en el panel de administración.
==============================================================================
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Aplicación Principal (Core)'
