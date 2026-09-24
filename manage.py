#!/usr/bin/env python
"""
==============================================================================
manage.py - Utilidad de línea de comandos de Django
==============================================================================
Explicación para alumnos:
Este archivo es el punto de entrada principal para ejecutar comandos de gestión en Django.
Nunca debes modificar la lógica interna de este archivo.

Comandos habituales que ejecutarás usando este script:
1. Iniciar servidor de desarrollo:
   python manage.py runserver

2. Crear migraciones cuando modifiques tus modelos (models.py):
   python manage.py makemigrations

3. Aplicar las migraciones a la base de datos:
   python manage.py migrate

4. Crear un usuario administrador para el panel de Django (/admin):
   python manage.py createsuperuser

5. Ejecutar la suite de pruebas unitarias:
   python manage.py test

6. Crear una nueva aplicación modular dentro de apps/:
   python manage.py startapp nombre_app apps/nombre_app
==============================================================================
"""
import os
import sys


def main():
    """Ejecuta tareas administrativas de Django."""
    # Establece el módulo de configuración central por defecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste activar "
            "tu entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
