"""
==============================================================================
apps/core/models.py - Modelos de Datos (ORM)
==============================================================================
Explicación para alumnos:
En Django, los 'Modelos' son clases de Python que representan tablas en la Base de Datos.
El ORM (Object-Relational Mapping) de Django traduce automáticamente estas clases
en sentencias SQL sin que tengas que escribir consultas a mano.

Conceptos clave:
- Cada atributo de la clase representa una columna en la tabla.
- '__str__()': Define cómo se representará el objeto como texto (ej. en el Admin).
- 'class Meta': Metadatos de la tabla (nombre en plural, ordenación, índices).

Flujo de trabajo con modelos:
1. Escribís o modificás la clase acá.
2. Ejecutás: python manage.py makemigrations (Django detecta los cambios).
3. Ejecutás: python manage.py migrate (Django aplica los cambios en PostgreSQL/SQLite).
==============================================================================
"""

from django.db import models


class MensajeBienvenida(models.Model):
    """
    Modelo de ejemplo para demostrar la estructura de una entidad en Django.
    """
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título descriptivo del mensaje"
    )
    contenido = models.TextField(
        verbose_name="Contenido",
        help_text="Texto completo del mensaje"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="¿Está activo?",
        help_text="Indica si este mensaje debe mostrarse en la página principal"
    )
    creado_el = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    actualizado_el = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Mensaje de Bienvenida"
        verbose_name_plural = "Mensajes de Bienvenida"
        ordering = ['-creado_el']

    def __str__(self):
        return f"{self.titulo} ({'Activo' if self.activo else 'Inactivo'})"
