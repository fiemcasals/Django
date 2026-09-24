"""
==============================================================================
apps/manual/views.py - Vistas del Manual Didáctico del Alumno
==============================================================================
Explicación para alumnos:
Este módulo implementa el concepto de 'Feature Flag' (Switch o Bandera de Función).
Permite habilitar o deshabilitar todo el manual interactivo mediante la variable
ENABLE_STUDENT_MANUAL en el archivo .env o settings.py.

Si ENABLE_STUDENT_MANUAL es False:
1. El decorador @manual_required intercepta la petición antes de ejecutar la vista.
2. Lanza una excepción Http404, haciendo que las rutas sean invisibles e inaccesibles.
3. El context processor en base.html oculta automáticamente los enlaces de navegación.
==============================================================================
"""

from functools import wraps
from django.conf import settings
from django.http import Http404
from django.shortcuts import render


def manual_required(view_func):
    """
    Decorador didáctico que verifica si el manual está habilitado en settings.
    Si ENABLE_STUDENT_MANUAL es False, retorna un error 404 (Página no encontrada).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        is_enabled = getattr(settings, 'ENABLE_STUDENT_MANUAL', True)
        if not is_enabled:
            raise Http404("El Manual del Alumno está deshabilitado por configuración (ENABLE_STUDENT_MANUAL=False).")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@manual_required
def manual_index_view(request):
    """
    Vista principal del manual didáctico.
    Presenta la tabla de contenidos, conceptos clave y accesos directos.
    """
    context = {
        'titulo_pagina': 'Manual del Alumno - Inicio',
        'seccion_activa': 'inicio',
    }
    return render(request, 'manual/index.html', context)


@manual_required
def manual_arquitectura_view(request):
    """
    Vista que explica la arquitectura interna de Django:
    - Patrón MVT (Model - View - Template).
    - Ciclo de vida de una Petición HTTP (Request -> Middlewares -> URL Resolver -> View -> Context -> Template -> Response).
    - Rol de los Middlewares y la Base de Datos.
    """
    context = {
        'titulo_pagina': 'Arquitectura Django (MVT) - Manual del Alumno',
        'seccion_activa': 'arquitectura',
    }
    return render(request, 'manual/arquitectura.html', context)


@manual_required
def manual_comandos_view(request):
    """
    Vista interactiva con el diccionario de comandos más utilizados en Django y Docker.
    Permite copiar comandos con un clic y entender qué hace cada parámetro.
    """
    comandos = [
        {
            'categoria': 'Gestión de Base de Datos y Migraciones',
            'items': [
                {
                    'comando': 'python manage.py makemigrations',
                    'descripcion': 'Lee los cambios en models.py y crea los archivos de migración en python (apps/*/migrations/).',
                    'ejemplo': 'python manage.py makemigrations'
                },
                {
                    'comando': 'python manage.py migrate',
                    'descripcion': 'Ejecuta las migraciones pendientes y crea/modifica las tablas reales en la base de datos.',
                    'ejemplo': 'python manage.py migrate'
                },
                {
                    'comando': 'python manage.py showmigrations',
                    'descripcion': 'Lista todas las migraciones del proyecto indicando cuáles ya están aplicadas con [X].',
                    'ejemplo': 'python manage.py showmigrations'
                }
            ]
        },
        {
            'categoria': 'Servidor, Usuarios y Verificación',
            'items': [
                {
                    'comando': 'python manage.py runserver',
                    'descripcion': 'Inicia el servidor web local de desarrollo en http://127.0.0.1:8000.',
                    'ejemplo': 'python manage.py runserver'
                },
                {
                    'comando': 'python manage.py createsuperuser',
                    'descripcion': 'Crea un usuario administrador con acceso total al panel de administración /admin/.',
                    'ejemplo': 'python manage.py createsuperuser'
                },
                {
                    'comando': 'python manage.py check',
                    'descripcion': 'Inspecciona todo el proyecto en busca de errores de configuración, sintaxis o rutas.',
                    'ejemplo': 'python manage.py check'
                },
                {
                    'comando': 'python manage.py test',
                    'descripcion': 'Descubre y ejecuta toda la suite de pruebas unitarias automatizadas.',
                    'ejemplo': 'python manage.py test'
                }
            ]
        },
        {
            'categoria': 'Docker y Docker Compose',
            'items': [
                {
                    'comando': 'docker compose up --build',
                    'descripcion': 'Construye las imágenes e inicia todos los contenedores (Django + PostgreSQL) mostrando logs en vivo.',
                    'ejemplo': 'docker compose up --build'
                },
                {
                    'comando': 'docker compose exec web python manage.py migrate',
                    'descripcion': 'Ejecuta comandos de Django directamente dentro del contenedor web en ejecución.',
                    'ejemplo': 'docker compose exec web python manage.py migrate'
                },
                {
                    'comando': 'docker compose down',
                    'descripcion': 'Detiene y elimina los contenedores creados sin borrar el volumen de datos de PostgreSQL.',
                    'ejemplo': 'docker compose down'
                }
            ]
        }
    ]

    context = {
        'titulo_pagina': 'Comandos Útiles - Manual del Alumno',
        'seccion_activa': 'comandos',
        'grupos_comandos': comandos,
    }
    return render(request, 'manual/comandos.html', context)
