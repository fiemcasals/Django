"""
==============================================================================
apps/core/views.py - Vistas (Controladores de Lógica)
==============================================================================
Explicación para alumnos:
En el patrón MVT (Model-View-Template) de Django, la 'Vista' es la función o clase
que recibe la solicitud HTTP del usuario ('request'), procesa la información
(consultando modelos, validando formularios) y retorna una respuesta HTTP ('response'),
habitualmente renderizando una plantilla HTML.

Estructura típica de una vista:
1. Recibe 'request' como primer parámetro.
2. Realiza consultas al ORM (ej. MensajeBienvenida.objects.filter(activo=True)).
3. Arma un diccionario de datos ('context').
4. Retorna render(request, 'nombre_template.html', context).
==============================================================================
"""

from django.shortcuts import render
from django.contrib import messages
from .models import MensajeBienvenida


def home_view(request):
    """
    Vista de la página de inicio (Landing didáctica).
    Obtiene los mensajes de bienvenida activos y los pasa a la plantilla.
    """
    mensajes_activos = MensajeBienvenida.objects.filter(activo=True)

    # Mensaje informativo de demostración para el sistema de mensajes de Django
    if not request.session.get('saludo_mostrado'):
        messages.info(request, "¡Bienvenido a la plantilla didáctica de Django! Esta estructura está lista para ser extendida.")
        request.session['saludo_mostrado'] = True

    context = {
        'titulo_pagina': 'Inicio - Plantilla Django Didáctica',
        'mensajes': mensajes_activos,
        'modulos_disponibles': [
            {'nombre': 'Arquitectura Modular', 'estado': 'Completada', 'desc': 'Estructura separada entre config/ y apps/.'},
            {'nombre': 'Manual Interactivo', 'estado': 'Pendiente HU-02', 'desc': 'Guía del alumno con switch de activación.'},
            {'nombre': 'Autenticación y Sesiones', 'estado': 'Pendiente HU-03', 'desc': 'Login, logout y reseteo por consola.'},
            {'nombre': 'CRUD y Persistencia PostgreSQL', 'estado': 'Pendiente HU-04', 'desc': 'Modelos indexados y consultas optimizadas.'},
            {'nombre': 'Integración con IA (Claude)', 'estado': 'Pendiente HU-05', 'desc': 'Tool calling y consulta a base de datos.'},
        ]
    }
    return render(request, 'core/index.html', context)


def salud_sistema_view(request):
    """
    Vista de comprobación de estado de la aplicación (Health Check).
    Útil para verificar que el servidor está respondiendo correctamente.
    """
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'ok',
        'framework': 'Django 5.x',
        'python_version': '3.12',
        'app': 'Plantilla Didáctica',
    })
