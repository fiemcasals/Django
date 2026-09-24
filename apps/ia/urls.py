"""
==============================================================================
apps/ia/urls.py - Enrutamiento de la Aplicación de Inteligencia Artificial
==============================================================================
Explicación para alumnos:
Configura el espacio de nombres 'ia' y las rutas para acceder al chat y
consultas inteligentes en 2 Fases con Anthropic Claude.
==============================================================================
"""

from django.urls import path
from .views import ConsultaIAView

app_name = 'ia'

urlpatterns = [
    # Ruta principal para el chat interactivo y consultas pedagógicas con IA
    path('consultas/', ConsultaIAView.as_view(), name='consultas'),
]
