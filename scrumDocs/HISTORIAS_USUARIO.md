# Historias de Usuario -- django

_Generado automaticamente el 2026-09-24T17:16:08.610Z -- no editar a mano, se sobreescribe en cada publicacion._

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

## HU-03: Autenticación de usuarios (Login, Logout y Restablecimiento de Contraseña)

Como usuario o alumno que utiliza la aplicación, quiero contar con un flujo completo de autenticación que incluya inicio/cierre de sesión y restablecimiento de contraseña olvidada, para gestionar mi acceso con seguridad y entender cómo funciona el sistema de auth, tokens y gestión de correos en Django.

### Criterios de Aceptacion

1. Debe incluir vistas, formularios y templates para Login (/login/) y Logout (/logout/) con protección CSRF y redirecciones configuradas.
2. Debe implementar el circuito estándar de restablecimiento de contraseña mediante token (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView y PasswordResetCompleteView).
3. Para el entorno de desarrollo local, el envío de emails debe configurarse con el backend de consola (console.EmailBackend), imprimiendo el enlace de reseteo directamente en la terminal para que el alumno pueda probarlo inmediatamente sin requerir credenciales SMTP.
4. Debe incluir soporte para cambio de contraseña desde la sesión activa (PasswordChangeView).
5. Las rutas protegidas deben requerir autenticación (@login_required), redirigiendo al login si el usuario es anónimo.
6. Cada template y vista del circuito debe estar comentado explicando paso a paso la generación del token y el ciclo de vida del reseteo.

### Detalle Tecnico y Reglas de Negocio

Uso de django.contrib.auth.views y sus formularios estándar. Configuración didáctica de EMAIL_BACKEND en settings.py mediante variables de entorno.
