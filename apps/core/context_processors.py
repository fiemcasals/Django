"""
==============================================================================
apps/core/context_processors.py - Contexto Global para Plantillas
==============================================================================
Explicación para alumnos:
Un Context Processor es una función que retorna un diccionario de variables
que estarán disponibles automáticamente en TODOS los templates HTML del proyecto,
sin necesidad de pasarlas manualmente en cada vista.
==============================================================================
"""

from django.conf import settings


def global_context(request):
    """
    Retorna variables globales disponibles en todos los templates:
    - 'app_name': Nombre del sistema.
    - 'enable_manual': Flag para mostrar u ocultar la sección didáctica del alumno.
    """
    return {
        'APP_NAME': 'Plantilla Django Didáctica',
        'ENABLE_STUDENT_MANUAL': getattr(settings, 'ENABLE_STUDENT_MANUAL', True),
    }
