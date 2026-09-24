"""
==============================================================================
apps/manual/tests.py - Pruebas Unitarias del Módulo Manual del Alumno
==============================================================================
"""

from django.test import TestCase, override_settings
from django.urls import reverse


class ManualAlumnoTests(TestCase):
    """
    Suite de pruebas automatizadas para el Manual Didáctico del Alumno.
    Verifica el funcionamiento del Feature Toggle (ENABLE_STUDENT_MANUAL).
    """

    @override_settings(ENABLE_STUDENT_MANUAL=True)
    def test_manual_habilitado_responde_200(self):
        """
        Con ENABLE_STUDENT_MANUAL=True:
        Verifica que todas las rutas del manual respondan HTTP 200 OK.
        """
        rutas = [
            reverse('manual:index'),
            reverse('manual:arquitectura'),
            reverse('manual:comandos'),
        ]
        for url in rutas:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                f"La URL {url} debería responder 200 cuando ENABLE_STUDENT_MANUAL=True"
            )

    @override_settings(ENABLE_STUDENT_MANUAL=False)
    def test_manual_deshabilitado_responde_404(self):
        """
        Con ENABLE_STUDENT_MANUAL=False:
        Verifica que todas las rutas del manual queden inaccesibles y retornen HTTP 404.
        """
        rutas = [
            reverse('manual:index'),
            reverse('manual:arquitectura'),
            reverse('manual:comandos'),
        ]
        for url in rutas:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                404,
                f"La URL {url} debería responder 404 cuando ENABLE_STUDENT_MANUAL=False"
            )

    def test_contenido_arquitectura_renderiza_secciones_clave(self):
        """
        Verifica que la página de arquitectura contenga los conceptos pedagógicos (MVT, Modelos, Vistas, Templates).
        """
        response = self.client.get(reverse('manual:arquitectura'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MVT")
        self.assertContains(response, "Modelo")
        self.assertContains(response, "Vista")
        self.assertContains(response, "Template")

    def test_contenido_comandos_renderiza_comandos_django(self):
        """
        Verifica que la página de comandos incluya 'makemigrations', 'migrate' y 'runserver'.
        """
        response = self.client.get(reverse('manual:comandos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "makemigrations")
        self.assertContains(response, "migrate")
        self.assertContains(response, "runserver")
