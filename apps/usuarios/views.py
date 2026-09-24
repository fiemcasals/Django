"""
==============================================================================
apps/usuarios/views.py - Vistas de Autenticación y Perfil de Usuario
==============================================================================
Explicación para alumnos:
Django incluye un robusto sistema de autenticación prefabricado en 'django.contrib.auth'.
En lugar de escribir lógica vulnerable de hashing de contraseñas o sesiones desde cero:
1. 'LoginView': Clase base que maneja el formulario de login, valida credenciales
   y autentica la sesión del usuario.
2. 'logout()': Función que destruye la sesión activa del usuario y limpia cookies.
3. '@login_required': Decorador de seguridad que restringe el acceso a una vista
   únicamente a usuarios autenticados. Si un usuario anónimo intenta entrar,
   lo redirige automáticamente a LOGIN_URL (?next=/ruta/protegida).
==============================================================================
"""

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """
    Vista de inicio de sesión basada en clases (CBV).
    Renderiza el formulario de login y maneja redirecciones automáticas.
    """
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirige al home o a la URL previa indicada en el parámetro '?next='."""
        return self.get_redirect_url() or reverse_lazy('core:home')

    def form_valid(self, form):
        messages.success(self.request, f"¡Bienvenido/a de nuevo, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos. Por favor, verificá tus datos.")
        return super().form_invalid(form)


def logout_view(request):
    """
    Vista de cierre de sesión.
    Limpia la sesión de Django, emite un mensaje flash y redirige a la página principal.
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"Hasta luego, {username}. Tu sesión ha sido cerrada correctamente.")
    return redirect('core:home')


@login_required
def perfil_view(request):
    """
    Vista protegida de perfil de usuario.
    Demuestra el uso del decorador @login_required y acceso a datos del usuario autenticado.
    """
    context = {
        'titulo_pagina': f'Perfil de {request.user.username}',
        'usuario': request.user,
    }
    return render(request, 'usuarios/perfil.html', context)
