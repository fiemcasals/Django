"""
apps/datos/admin.py - Registro de modelos en el panel de administración
"""
from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio', 'disponible', 'fecha_creacion')
    list_filter = ('categoria', 'disponible')
    search_fields = ('titulo', 'descripcion')
    ordering = ('-fecha_creacion',)
