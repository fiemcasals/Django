"""
==============================================================================
apps/datos/services.py - Capa de Servicios de Datos y Optimización
==============================================================================
Explicación para alumnos:
La Capa de Servicios ('Service Layer') encapsula lógica de negocio que no pertenece
exclusivamente a una vista ni a un modelo puntual. Facilita la reutilización y el testeo.
==============================================================================
"""

from .models import Item


class CatalogoService:
    """Servicio de dominio para consultas optimizadas de catálogo."""

    @staticmethod
    def obtener_indice_liviano():
        """Retorna el catálogo resumido para alimentar prompts y herramientas de IA."""
        return Item.objects.obtener_catalogo_indice()

    @staticmethod
    def buscar_items(query=None, categoria=None):
        """Combina filtros de búsqueda y categoría sobre el catálogo."""
        qs = Item.objects.filter(disponible=True)
        if categoria:
            qs = qs.filter(categoria__iexact=categoria)
        if query:
            qs = qs.buscar_por_texto(query)
        return qs
