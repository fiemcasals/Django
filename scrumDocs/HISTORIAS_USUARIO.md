# Historias de Usuario -- django

_Generado automaticamente el 2026-09-24T17:13:53.234Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Arquitectura base modular y entorno Dockerizado con documentación didáctica

Como alumno o docente sin conocimientos avanzados de infraestructura, quiero disponer de un proyecto Django base modular, dockerizado con PostgreSQL y con cada archivo clave documentado en código, para entender la separación entre configuración central y aplicaciones, y poder extender el proyecto de manera guiada tanto manualmente como con asistentes IA.

### Criterios de Aceptacion

1. El proyecto debe estar contenerizado con Dockerfile y docker-compose.yml, levantando el servicio web de Django y una base de datos PostgreSQL lista para desarrollo.
2. Debe quedar explícita la distinción entre el paquete de configuración central (config/) y las aplicaciones independientes (apps/).
3. Cada archivo base estándar (settings.py, urls.py, models.py, views.py, forms.py, admin.py, apps.py) debe contener comentarios explicativos claros sobre su propósito y cómo reproducirlo/extenderlo.
4. El archivo settings.py debe incluir únicamente las variables necesarias, cada una comentada explicando su función y cargando credenciales sensibles mediante variables de entorno (.env).
5. Debe incluir un archivo README.md con los comandos exactos para levantar el entorno (docker compose up --build), correr migraciones y crear un superusuario.

### Detalle Tecnico y Reglas de Negocio

Python 3.12, Django 5.x, PostgreSQL 16. Gestión de variables de entorno con django-environ o python-dotenv. Estructura limpia y reproducible sin sobrecarga de librerías innecesarias.

## HU-02: Módulo didáctico interactivo (Manual del Alumno) con mecanismo de activación u ocultamiento

Como alumno o docente que utiliza la plantilla, quiero disponer de una sección interactiva integrada en la app que explique paso a paso la arquitectura de Django y cómo extenderla, con un mecanismo simple para protegerla u ocultarla, para consultar la guía en tiempo de aprendizaje y desactivarla/removerla fácilmente al entregar o publicar el producto final sin dejar rastro visible para usuarios finales.

### Criterios de Aceptacion

1. Debe existir una aplicación dedicada (apps/manual/ o apps/guia/) con vistas y templates que ilustren el flujo de peticiones en Django (MVT: Model-View-Template, URLs, Forms).
2. El acceso al manual debe poder controlarse mediante una clave de acceso simple en interfaz o una variable de entorno configurable (por ejemplo, ENABLE_STUDENT_MANUAL=True/False).
3. Si la variable o flag está desactivada, las rutas del manual deben quedar deshabilitadas o responder 404 / No disponible y no mostrar enlaces en la barra de navegación principal.
4. El código del módulo manual debe estar completamente aislado para que el alumno pueda eliminar la carpeta de la app y su referencia en INSTALLED_APPS sin romper el resto del sistema.
5. Debe incluir una sección con ejemplos prácticos de comandos habituales de Django (makemigrations, migrate, createsuperuser, startapp).

### Detalle Tecnico y Reglas de Negocio

App desacoplada en apps/manual/. Inclusión condicional de URLs en config/urls.py según configuración en settings.py. Context processor o middleware liviano para ocultar/mostrar elementos del manual en la UI base.
