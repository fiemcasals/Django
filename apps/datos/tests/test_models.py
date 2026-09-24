"""
==============================================================================
apps/datos/tests/test_models.py - Pruebas Unitarias del Modelo Item y Catálogo
==============================================================================
"""

from django.test import TestCase
from apps.datos.models import Item
from apps.datos.services import CatalogoService


class ItemModelTests(TestCase):
    """
    Suite de pruebas para el modelo Item, sus índices y optimizaciones de extracción.
    """

    def setUp(self):
        """Crea registros de muestra para las consultas."""
        self.item1 = Item.objects.create(
            titulo='Curso de Django 5 Modular',
            categoria='Cursos',
            descripcion='Aprende Django desde cero con buenas prácticas y arquitectura limpia.',
            precio=49.99,
            disponible=True
        )
        self.item2 = Item.objects.create(
            titulo='Guía Avanzada de PostgreSQL',
            categoria='Bases de Datos',
            descripcion='Índices, particionado, optimización de queries y escalabilidad.',
            precio=29.99,
            disponible=True
        )
        self.item_oculto = Item.objects.create(
            titulo='Borrador no publicado',
            categoria='Borradores',
            descripcion='Contenido en desarrollo.',
            precio=0.00,
            disponible=False
        )

    def test_crear_item_persiste_correctamente(self):
        """Verifica que el registro se guarde en la BD y retorne el __str__ esperado."""
        self.assertEqual(Item.objects.count(), 3)
        self.assertEqual(str(self.item1), "Curso de Django 5 Modular [Cursos]")

    def test_obtener_catalogo_indice_extrae_unicamente_campos_livianos(self):
        """
        Verifica que obtener_catalogo_indice() retorne solo {id, titulo, categoria}
        y excluya campos pesados (como 'descripcion') para optimizar consumo de tokens de IA.
        """
        indice = Item.objects.obtener_catalogo_indice()
        # Solo debe incluir los disponibles (2 de los 3)
        self.assertEqual(len(indice), 2)
        primer_item = indice[0]
        self.assertIn('id', primer_item)
        self.assertIn('titulo', primer_item)
        self.assertIn('categoria', primer_item)
        # Campos pesados NO deben viajar en el índice
        self.assertNotIn('descripcion', primer_item)
        self.assertNotIn('precio', primer_item)

    def test_buscar_por_texto_encuentra_coincidencias(self):
        """Verifica búsqueda insensible a mayúsculas en título o descripción."""
        resultados = Item.objects.buscar_por_texto("PostgreSQL")
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first(), self.item2)

    def test_filtrar_por_categoria(self):
        """Verifica filtro optimizado por categoría."""
        resultados = Item.objects.filtrar_por_categoria("Cursos")
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first(), self.item1)

    def test_catalogo_service_obtiene_indice_para_ia(self):
        """Verifica que el servicio de dominio CatalogoService retorne el formato esperado."""
        res = CatalogoService.obtener_indice_liviano()
        self.assertEqual(len(res), 2)
