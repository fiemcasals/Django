"""
==============================================================================
apps/usuarios/tests/test_password_reset.py - Tests de Restablecimiento y Cambio
==============================================================================
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class PasswordResetTests(TestCase):
    """
    Suite de pruebas unitarias para el circuito de recuperación y cambio de contraseña.
    """

    def setUp(self):
        """Crea usuario de prueba."""
        self.username = 'alumno_recovery'
        self.email = 'recovery@universidad.edu.ar'
        self.password = 'ClaveInicial123!'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_solicitud_password_reset_envia_email_con_token(self):
        """Verifica que solicitar reseteo envíe un correo simulado con token y uidb64."""
        response = self.client.post(reverse('usuarios:password_reset'), {
            'email': self.email
        })
        self.assertEqual(response.status_code, 302)
        # Comprueba que se haya generado un correo electrónico en la bandeja de salida
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn(self.email, sent_email.to)
        # Comprueba que el correo incluya el enlace con uid y token
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.assertIn(uidb64, sent_email.body)

    def test_password_reset_confirm_token_valido_actualiza_clave(self):
        """Verifica que ingresar con token válido permita establecer una nueva clave."""
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        confirm_url = reverse('usuarios:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})

        # 1. Cargar formulario siguiendo redirección interna de sesión de Django 5
        get_resp = self.client.get(confirm_url, follow=True)
        self.assertEqual(get_resp.status_code, 200)
        post_url = get_resp.redirect_chain[0][0] if get_resp.redirect_chain else confirm_url

        # 2. Enviar nueva contraseña
        nueva_clave = 'NuevaClaveSegura2026!'
        post_resp = self.client.post(post_url, {
            'new_password1': nueva_clave,
            'new_password2': nueva_clave,
        })
        self.assertEqual(post_resp.status_code, 302)

        # 3. Validar que la autenticación funcione con la nueva contraseña
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(nueva_clave))

    def test_password_reset_confirm_token_invalido_rechaza_reseteo(self):
        """Verifica que un token inválido o corrupto no permita cambiar la clave."""
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'token-invalido-12345'
        confirm_url = reverse('usuarios:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': invalid_token})

        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "inválido o ha expirado")

    def test_password_change_usuario_autenticado_actualiza_clave(self):
        """Verifica que un usuario autenticado pueda cambiar su clave desde password_change."""
        self.client.login(username=self.username, password=self.password)
        change_url = reverse('usuarios:password_change')

        # 1. Cargar formulario
        get_resp = self.client.get(change_url)
        self.assertEqual(get_resp.status_code, 200)

        # 2. Enviar cambio de clave
        nueva_clave = 'ClaveCambiada2026!'
        post_resp = self.client.post(change_url, {
            'old_password': self.password,
            'new_password1': nueva_clave,
            'new_password2': nueva_clave,
        })
        self.assertEqual(post_resp.status_code, 302)

        # 3. Validar en base de datos
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(nueva_clave))
