"""
==============================================================================
apps/core/tests.py - Pruebas Unitarias Automatizadas de la App Core
==============================================================================
Explicación para alumnos:
En Django, las pruebas unitarias se escriben heredando de 'django.test.TestCase'.
Django crea automáticamente una base de datos temporal y aislada para ejecutar
las pruebas, garantizando que nunca se toquen ni ensucien los datos reales.

Para ejecutar las pruebas:
python manage.py test apps.core
==============================================================================
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import MensajeBienvenida
from .forms import MensajeBienvenidaForm


class CoreAppTests(TestCase):
    """Suite de pruebas para verificar el funcionamiento de la app Core."""

    def setUp(self):
        """Prepara el entorno y datos de prueba antes de cada test."""
        self.client = Client()
        self.mensaje = MensajeBienvenida.objects.create(
            titulo="Mensaje de Prueba",
            contenido="Este es un contenido de prueba para validar el sistema.",
            activo=True
        )

    def test_01_home_view_responde_200(self):
        """Verifica que la página de inicio responda código HTTP 200 y use el template correcto."""
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, "Mensaje de Prueba")

    def test_02_health_check_responde_json_ok(self):
        """Verifica que el endpoint de salud /salud/ devuelva status: ok."""
        url = reverse('core:salud')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')

    def test_03_modelo_str_y_persistencia(self):
        """Verifica la correcta representación en texto y persistencia del modelo."""
        self.assertEqual(str(self.mensaje), "Mensaje de Prueba (Activo)")
        self.assertEqual(MensajeBienvenida.objects.count(), 1)

    def test_04_formulario_valido(self):
        """Verifica que el formulario acepte datos válidos."""
        datos = {
            'titulo': 'Nuevo Mensaje Válido',
            'contenido': 'Contenido explicativo suficiente.',
            'activo': True
        }
        form = MensajeBienvenidaForm(data=datos)
        self.assertTrue(form.is_valid())

    def test_05_formulario_invalido_por_titulo_corto(self):
        """Verifica que la validación personalizada rechace títulos de menos de 3 caracteres."""
        datos = {
            'titulo': 'Ab', # Menos de 3 caracteres
            'contenido': 'Contenido de prueba',
            'activo': True
        }
        form = MensajeBienvenidaForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
