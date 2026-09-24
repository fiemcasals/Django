"""
==============================================================================
apps/ia/views.py - Vistas para el Chat y Consulta Asistida por IA (Claude)
==============================================================================
Explicación Pedagógica para Alumnos:

1. ¿POR QUÉ LOGINREQUIREDMIXIN?
   El acceso a modelos de lenguaje comerciales genera costos por tokens.
   Protegemos la ruta con `LoginRequiredMixin` para asegurar que solo usuarios
   autenticados puedan consumir el servicio de IA. Si un visitante anónimo
   intenta entrar, Django lo redirige automáticamente a `/login/?next=/ia/consultas/`.

2. PATRÓN DE VISTA BASADA EN CLASES (View / FormView):
   - En peticiones `GET`: Se renderiza el formulario vacío con sugerencias de preguntas.
   - En peticiones `POST`: Se valida el formulario con `is_valid()`, se invoca al servicio
     `ClaudeService.procesar_consulta()` y se inyecta en el contexto de la plantilla
     el resultado detallado de las 2 Fases (Herramienta elegida + Datos locales + Síntesis).
==============================================================================
"""

import logging
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import ConsultaIAForm
from .services import ClaudeService

logger = logging.getLogger(__name__)


class ConsultaIAView(LoginRequiredMixin, View):
    """
    Vista protegida que gestiona la interacción interactiva con el asistente de IA.
    Visualiza pedagógicamente las dos fases de resolución:
    - Fase 1: Selección de Tool (Tokens mínimos).
    - Ejecución local: Consulta PostgreSQL ORM.
    - Fase 2: Síntesis final de Claude con métricas de tokens.
    """
    template_name = 'ia/chat.html'

    def get(self, request):
        """Renderiza la pantalla inicial con el formulario de consulta y sugerencias."""
        form = ConsultaIAForm()
        preguntas_sugeridas = [
            "¿Qué tutoriales sobre Django tienen disponibles?",
            "Muéstrame los cursos y recursos sobre PostgreSQL e indexación.",
            "Dame un resumen de todo el catálogo disponible.",
            "¿Cuál es el precio y contenido del ítem con ID 1?"
        ]
        context = {
            'form': form,
            'preguntas_sugeridas': preguntas_sugeridas,
            'resultado': None
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Procesa la pregunta del usuario a través de ClaudeService y retorna ambas fases."""
        form = ConsultaIAForm(request.POST)
        resultado = None

        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']
            service = ClaudeService()
            resultado = service.procesar_consulta(pregunta)

            if resultado.get('status') == 'error':
                # Registramos mensaje flash de aviso pedagógico
                messages.warning(request, f"Aviso del servicio de IA: {resultado.get('message')}")

        preguntas_sugeridas = [
            "¿Qué tutoriales sobre Django tienen disponibles?",
            "Muéstrame los cursos y recursos sobre PostgreSQL e indexación.",
            "Dame un resumen de todo el catálogo disponible.",
            "¿Cuál es el precio y contenido del ítem con ID 1?"
        ]

        context = {
            'form': form,
            'preguntas_sugeridas': preguntas_sugeridas,
            'resultado': resultado
        }
        return render(request, self.template_name, context)
