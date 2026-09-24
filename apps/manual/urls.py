"""
==============================================================================
apps/manual/urls.py - Enrutador del Manual del Alumno
==============================================================================
"""

from django.urls import path
from . import views

app_name = 'manual'

urlpatterns = [
    path('', views.manual_index_view, name='index'),
    path('arquitectura/', views.manual_arquitectura_view, name='arquitectura'),
    path('comandos/', views.manual_comandos_view, name='comandos'),
]
