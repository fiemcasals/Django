"""
==============================================================================
apps/core/urls.py - Enrutador Local de la App Core
==============================================================================
Explicación para alumnos:
Cada aplicación tiene su propio archivo 'urls.py'.
Esto permite que la aplicación sea modular y portátil (se puede copiar a otro proyecto sin romper nada).

Conceptos clave:
- 'app_name': Define el espacio de nombres (namespace).
  Permite referenciar rutas en templates como {% url 'core:home' %}.
- 'path(ruta, vista, name="nombre_ruta")': Conecta una URL con su función vista.
==============================================================================
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Ruta raíz de la app (http://localhost:8000/)
    path('', views.home_view, name='home'),

    # Ruta de Health Check (http://localhost:8000/salud/)
    path('salud/', views.salud_sistema_view, name='salud'),
]
