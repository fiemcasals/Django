"""
==============================================================================
apps/ia/apps.py - Configuración de la Aplicación de Inteligencia Artificial
==============================================================================
Explicación para alumnos:
En Django, cada aplicación debe tener una clase AppConfig que define los
metadatos del paquete. Aquí configuramos el nombre 'apps.ia' y el nombre
legible para el panel de administración.
==============================================================================
"""

from django.apps import AppConfig


class IaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ia'
    verbose_name = 'Inteligencia Artificial Didáctica'
