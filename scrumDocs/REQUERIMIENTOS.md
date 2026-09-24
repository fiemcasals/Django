# Requerimientos -- django

_Generado automaticamente el 2026-09-24T23:39:24.451Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Arquitectura base modular y entorno Dockerizado con documentación didáctica

### RF-01: Configuración central y estructura modular de aplicaciones Django (Funcional)

Crear la estructura de carpetas modular (config/, apps/core/, templates/, static/). Entregar los archivos centrales (settings.py, urls.py, wsgi.py, asgi.py) y la app base con sus archivos obligatorios comentados didácticamente (models.py, views.py, forms.py, urls.py, admin.py, apps.py, tests.py). Incluir .env.example, .gitignore, requirements.txt y plantilla base.html. Condición de aprobación: python manage.py check con código 0 y servidor funcional sin secretos hardcodeados.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RNF-01: Contenerización del entorno con Docker, docker-compose y PostgreSQL (No funcional)

Crear el archivo Dockerfile optimizado (Python 3.12) y docker-compose.yml que orqueste el servicio web (Django) y el servicio db (PostgreSQL 16) con volumen persistente para datos y variables de entorno vinculadas. Crear .dockerignore y script de espera para la base de datos. Actualizar el archivo README.md con los comandos exactos paso a paso (docker compose up --build, ejecución de migraciones y creación de superusuario). Entregables: Dockerfile, docker-compose.yml, .dockerignore, README.md. Condición de aprobación: docker compose up levanta ambos servicios, conecta a PostgreSQL y responde HTTP 200 en http://localhost:8000.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-02: Módulo didáctico interactivo (Manual del Alumno) con mecanismo de activación u ocultamiento

### RF-01: Módulo interactivo de Guía/Manual del Alumno con switch de activación (Funcional)

Crear una aplicación independiente (apps/manual/) con vistas y plantillas que expliquen interactivamente la arquitectura de Django (MVT, flujo de peticiones y comandos de terminal). El módulo debe activarse o desactivarse mediante la variable de entorno ENABLE_STUDENT_MANUAL. Si está inactivo, las rutas deben quedar inaccesibles (404) y ocultar los links del menú. Todo el código de la app debe estar desacoplado para permitir su eliminación limpia sin romper el proyecto. Entregables: apps/manual/ (apps.py, views.py, urls.py) y templates/manual/ (index.html, arquitectura.html, comandos.html). Condición de aprobación: con ENABLE_STUDENT_MANUAL=True el manual es navegable en /manual/; con False retorna 404 y se oculta del navbar; remover la app no rompe el resto del sistema.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-03: Autenticación de usuarios (Login, Logout y Restablecimiento de Contraseña)

### RF-01: Sistema de inicio, cierre de sesión y control de acceso (Funcional)

Implementar vistas, formularios y templates para Login (/login/) y Logout (/logout/). Configurar variables LOGIN_URL, LOGIN_REDIRECT_URL y LOGOUT_REDIRECT_URL. Aplicar decorador @login_required y adaptar barra de navegación. Entregables: apps/usuarios/ (views.py, urls.py), templates/registration/ (login.html, logged_out.html), apps/usuarios/tests/test_auth.py. Suite de tests obligatoria: login credenciales válidas (302), login inválidas (200 con error), logout cierra sesión, vista protegida redirige a anónimos y responde 200 a autenticados. Aprobación: python manage.py test apps.usuarios.tests.test_auth OK (5 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Circuito de restablecimiento y cambio de contraseña con emisor de consola (Funcional)

Implementar el circuito completo de restablecimiento de contraseña (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView) y cambio de contraseña activa (PasswordChangeView). Configurar EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'. Entregables: templates/registration/ (password_reset_form.html, password_reset_done.html, password_reset_confirm.html, password_reset_complete.html, password_change_form.html, password_change_done.html), apps/usuarios/tests/test_password_reset.py. Suite de tests obligatoria: genera correo con uidb64 y token, rechaza token inválido, confirma reseteo exitoso y permite cambio autenticado. Aprobación: python manage.py test apps.usuarios.tests.test_password_reset OK (4 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-04: CRUD de información didáctico con indexación en base de datos PostgreSQL

### RF-01: Modelos de datos con indexación y métodos de extracción de catálogo/índice (Funcional)

Crear la aplicación apps/datos/ con un modelo representativo (Item/Recurso) que incluya campos de texto, fecha, categoría y claves indexadas en PostgreSQL (db_index=True, Meta.indexes). Implementar en el modelo o manager el método obtener_catalogo_indice() que extraiga únicamente los metadatos livianos (ID, título, categoría) para optimización de tokens, y los métodos de búsqueda parametrizados. Entregables: apps/datos/ (apps.py, models.py, services.py), apps/datos/tests/test_models.py. Suite de tests obligatoria: crear registro persiste, obtener_catalogo_indice liviano, buscar por texto y filtrar por categoría. Aprobación: python manage.py test apps.datos.tests.test_models OK (4 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Interfaz Web CRUD para gestión de datos con validaciones (Funcional)

Implementar formularios (ModelForm) con validaciones y vistas protegidas con @login_required para el ciclo CRUD completo (Listar, Detalle, Crear, Editar, Eliminar) del modelo Item/Recurso. Renderizar plantillas HTML claras con mensajes de feedback. Entregables: apps/datos/ (forms.py, views.py, urls.py), templates/datos/ (lista.html, detalle.html, form.html, confirmar_eliminar.html), apps/datos/tests/test_views.py. Suite de tests obligatoria: listar responde 200, crear form válido persiste, crear form inválido muestra errores, editar actualiza y eliminar borra. Aprobación: python manage.py test apps.datos.tests.test_views OK (5 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-05: Consulta inteligente a base de datos asistida por IA (Anthropic API con optimización estricta de tokens)

### RF-01: Servicio de IA con Anthropic SDK, Tool Calling en dos pasos y optimización de tokens (Funcional)

Implementar en apps/ia/services.py la integración con Claude (anthropic SDK) leyendo ANTHROPIC_API_KEY desde .env. Implementar flujo en 2 pasos: Fase 1 para selección de tool de consulta liviano y Fase 2 para ejecución local en PostgreSQL y reenvío de datos a Claude para síntesis final. Manejar errores de conexión y cuotas. Entregables: apps/ia/ (apps.py, services.py), apps/ia/tests/test_ai_service.py. Suite de tests obligatoria (con mocks): esquema tools mínimo, selección de herramienta Fase 1, síntesis Fase 2 y captura de errores sin error 500. Aprobación: python manage.py test apps.ia.tests.test_ai_service OK (4 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Interfaz Web y Chat Didáctico para consultas con visualización del flujo de IA (Funcional)

Crear vistas, formularios y plantillas para interfaz de consultas asistidas por IA (/ia/consultas/). Permitir enviar preguntas en lenguaje natural y renderizar interactivamente las 2 etapas: 1. Tool seleccionado; 2. Respuesta final de Claude con datos de PostgreSQL. Entregables: apps/ia/ (forms.py, views.py, urls.py), templates/ia/ (chat.html, resultado_parcial.html), apps/ia/tests/test_views.py. Suite de tests obligatoria (con mocks): requiere login, renderiza 200, envío exitoso muestra ambas etapas y manejo de error visual ante falla de API. Aprobación: python manage.py test apps.ia.tests.test_views OK (4 tests pasados).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._
