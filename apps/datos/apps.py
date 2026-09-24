"""
apps/datos/apps.py - Configuración de la aplicación Datos
"""
from django.apps import AppConfig


class DatosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.datos'
    verbose_name = 'Gestión de Datos y Catálogo'
