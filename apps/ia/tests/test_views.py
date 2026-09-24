"""
==============================================================================
apps/ia/tests/test_views.py - Suite de Tests Unitarios para Vistas de IA
==============================================================================
Explicación para alumnos:
En este archivo verificamos el comportamiento HTTP de las vistas de IA:
1. Control de acceso: Requiere inicio de sesión obligatorio (LoginRequiredMixin).
2. Renderizado GET: Carga de formulario y sugerencias (200 OK).
3. Envío POST exitoso: Mockeamos el servicio para verificar el renderizado visual de las 2 Fases.
4. Resiliencia ante errores: Ante fallos en la API externa, la vista muestra mensajes
   didácticos sin emitir un error 500 del servidor.
==============================================================================
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ConsultaIAViewTestCase(TestCase):
    """
    Suite de 4 tests unitarios para la vista ConsultaIAView:
    - test_login_required
    - test_render_chat_page
    - test_post_consulta_exitosa
    - test_post_manejo_error_api
    """

    def setUp(self):
        """Crea usuario de prueba y cliente HTTP de Django."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='alumno_test',
            email='alumno@universidad.edu.ar',
            password='Password123!'
        )
        self.url = reverse('ia:consultas')

    def test_login_required(self):
        """
        1. Verifica que un usuario anónimo sea redirigido a login al intentar acceder.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_render_chat_page(self):
        """
        2. Verifica que un usuario autenticado pueda acceder y renderice el formulario.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ia/chat.html')
        self.assertIn('form', response.context)
        self.assertContains(response, 'Consulta Inteligente a Base de Datos con IA')

    @patch('apps.ia.views.ClaudeService.procesar_consulta')
    def test_post_consulta_exitosa(self, mock_procesar):
        """
        3. Verifica que un envío POST exitoso renderice las 2 fases del flujo de IA.
        """
        self.client.force_login(self.user)

        # Mock del resultado en 2 fases
        mock_procesar.return_value = {
            "status": "success",
            "tipo_respuesta": "tool_calling",
            "fase_1": {
                "tool_invocado": "buscar_items_por_texto",
                "parametros": {"query": "Django"},
                "tokens_fase_1": {"input_tokens": 120, "output_tokens": 35}
            },
            "fase_2": {
                "registros_encontrados": 2,
                "datos_locales": [
                    {"id": 1, "titulo": "Curso Django", "categoria": "tutorial", "descripcion": "Intro MVT"}
                ],
                "respuesta_final": "Encontré recursos sobre Django disponibles en el catálogo.",
                "tokens_fase_2": {"input_tokens": 200, "output_tokens": 50}
            },
            "total_tokens": 405
        }

        response = self.client.post(self.url, {'pregunta': '¿Tienen cursos de Django?'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ia/chat.html')
        self.assertContains(response, 'buscar_items_por_texto')
        self.assertContains(response, 'Encontré recursos sobre Django')
        self.assertContains(response, '405 tokens')

    @patch('apps.ia.views.ClaudeService.procesar_consulta')
    def test_post_manejo_error_api(self, mock_procesar):
        """
        4. Verifica que ante un error en la API se renderice un aviso amigable sin causar HTTP 500.
        """
        self.client.force_login(self.user)

        # Mock de error del servicio
        mock_procesar.return_value = {
            "status": "error",
            "error_type": "AuthenticationError",
            "message": "Clave de API de Anthropic inválida o no configurada."
        }

        response = self.client.post(self.url, {'pregunta': '¿Qué hay en el catálogo?'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aviso del Servicio de IA')
        self.assertContains(response, 'AuthenticationError')
        self.assertContains(response, 'Clave de API de Anthropic inválida')
