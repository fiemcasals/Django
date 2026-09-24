"""
==============================================================================
apps/core/admin.py - Registro en el Panel de Administración de Django
==============================================================================
Explicación para alumnos:
Django incluye automáticamente un panel de administración visual listo para usar en '/admin'.
Para que tus modelos aparezcan en ese panel, debes registrarlos en este archivo.

Personalizaciones habituales:
- 'list_display': Columnas visibles en la tabla del panel de administración.
- 'list_filter': Filtros laterales rápidos (por fecha, booleano, etc.).
- 'search_fields': Barra de búsqueda por texto.
==============================================================================
"""

from django.contrib import admin
from .models import MensajeBienvenida


@admin.register(MensajeBienvenida)
class MensajeBienvenidaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'creado_el', 'actualizado_el')
    list_filter = ('activo', 'creado_el')
    search_fields = ('titulo', 'contenido')
    ordering = ('-creado_el',)
