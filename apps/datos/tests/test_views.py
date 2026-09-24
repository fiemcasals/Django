"""
==============================================================================
apps/datos/tests/test_views.py - Pruebas Unitarias de Vistas CRUD de Datos
==============================================================================
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.datos.models import Item

User = get_user_model()


class ItemViewsTests(TestCase):
    """
    Suite de pruebas para las vistas CRUD del catálogo de datos.
    """

    def setUp(self):
        """Crea usuario y registros iniciales."""
        self.user = User.objects.create_user(username='autor_test', password='ClaveSegura123!')
        self.item = Item.objects.create(
            titulo='Curso de Python 3',
            categoria='Cursos',
            descripcion='Aprende sintaxis básica y avanzada.',
            precio=19.99,
            disponible=True
        )
        self.lista_url = reverse('datos:lista')
        self.crear_url = reverse('datos:crear')
        self.detalle_url = reverse('datos:detalle', kwargs={'pk': self.item.pk})
        self.editar_url = reverse('datos:editar', kwargs={'pk': self.item.pk})
        self.eliminar_url = reverse('datos:eliminar', kwargs={'pk': self.item.pk})

    def test_listar_items_responde_200(self):
        """Verifica que el listado público responda HTTP 200 y contenga el ítem."""
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.titulo)

    def test_detalle_item_responde_200(self):
        """Verifica la vista de detalle de un ítem existente."""
        response = self.client.get(self.detalle_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.titulo)
        self.assertContains(response, self.item.descripcion)

    def test_crear_item_anonimo_redirige_a_login(self):
        """Verifica que un usuario anónimo no pueda acceder al formulario de creación."""
        response = self.client.get(self.crear_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_crear_item_autenticado_persiste_registro(self):
        """Verifica que un usuario autenticado pueda crear un nuevo ítem válido."""
        self.client.login(username='autor_test', password='ClaveSegura123!')
        response = self.client.post(self.crear_url, {
            'titulo': 'Manual de Docker Compose',
            'categoria': 'DevOps',
            'descripcion': 'Guía paso a paso de contenerización.',
            'precio': '25.00',
            'disponible': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(titulo='Manual de Docker Compose').exists())

    def test_crear_item_invalido_muestra_errores(self):
        """Verifica que un formulario con título de menos de 3 caracteres sea rechazado."""
        self.client.login(username='autor_test', password='ClaveSegura123!')
        response = self.client.post(self.crear_url, {
            'titulo': 'AB',  # Menor a 3 caracteres
            'categoria': 'Test',
            'descripcion': 'Corta',
            'precio': '10.00',
            'disponible': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "al menos 3 caracteres")

    def test_editar_item_autenticado_actualiza_datos(self):
        """Verifica que un usuario logueado pueda actualizar un ítem existente."""
        self.client.login(username='autor_test', password='ClaveSegura123!')
        response = self.client.post(self.editar_url, {
            'titulo': 'Curso de Python 3 y Django 5',
            'categoria': 'Cursos',
            'descripcion': self.item.descripcion,
            'precio': '29.99',
            'disponible': True
        })
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.titulo, 'Curso de Python 3 y Django 5')

    def test_eliminar_item_autenticado_borra_registro(self):
        """Verifica que confirmar eliminación borre el registro de la BD."""
        self.client.login(username='autor_test', password='ClaveSegura123!')
        response = self.client.post(self.eliminar_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
