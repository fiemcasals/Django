"""
==============================================================================
apps/usuarios/tests/test_auth.py - Pruebas Unitarias de Autenticación
==============================================================================
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AutenticacionTests(TestCase):
    """
    Suite de pruebas unitarias para el ciclo de autenticación:
    Login, Logout y Control de Acceso con decorador @login_required.
    """

    def setUp(self):
        """Prepara un usuario de prueba en la base de datos de test."""
        self.username = 'alumno_test'
        self.password = 'ClaveSegura123!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='alumno@universidad.edu.ar'
        )
        self.login_url = reverse('usuarios:login')
        self.logout_url = reverse('usuarios:logout')
        self.perfil_url = reverse('usuarios:perfil')

    def test_login_renderiza_formulario_200(self):
        """Verifica que la página de login responda HTTP 200 y contenga los inputs."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Iniciar Sesión")
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_login_exitoso_credenciales_validas(self):
        """Verifica que ingresar credenciales correctas autentique y redirija (302)."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        # Verificamos que el usuario quedó autenticado en la sesión
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_fallido_credenciales_invalidas(self):
        """Verifica que ingresar una contraseña errónea rechace el acceso (HTTP 200 con errores)."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'password_incorrecta',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertContains(response, "incorrectos")

    def test_logout_cierra_sesion_exitosamente(self):
        """Verifica que al hacer logout la sesión se destruya y redirija."""
        self.client.login(username=self.username, password=self.password)
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        # La sesión ya no debe contener al usuario autenticado
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_vista_protegida_redirige_a_usuario_anonimo(self):
        """Verifica que un usuario no autenticado sea redirigido a login al intentar entrar a perfil."""
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    def test_vista_protegida_permite_acceso_a_autenticado(self):
        """Verifica que un usuario logueado pueda ver su perfil (HTTP 200)."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username)
