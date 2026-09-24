"""
==============================================================================
config/settings.py - Configuración Central de Django
==============================================================================
Explicación para alumnos:
Este archivo contiene todos los ajustes del proyecto Django.
Para mantener un código profesional y seguro:
1. Las contraseñas, claves secretas y URLs de base de datos se leen desde el archivo '.env'.
2. Las aplicaciones que construyas se organizan dentro del directorio 'apps/'.
3. Cada bloque de configuración incluye un comentario explicando qué hace.
==============================================================================
"""

from pathlib import Path
import os
import sys
import environ

# ------------------------------------------------------------------------------
# 1. RUTAS BASE Y CARGA DE VARIABLES DE ENTORNO (.env)
# ------------------------------------------------------------------------------
# BASE_DIR apunta a la carpeta raíz del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Agregamos la carpeta 'apps' al path de Python para poder importar apps directamente
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Inicializamos django-environ para leer variables del sistema y del archivo .env
env = environ.Env(
    DEBUG=(bool, False),
    ENABLE_STUDENT_MANUAL=(bool, True),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
)

# Leemos el archivo .env si existe en la raíz
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

# ------------------------------------------------------------------------------
# 2. AJUSTES BÁSICOS DE SEGURIDAD
# ------------------------------------------------------------------------------
# Clave criptográfica única. En producción debe venir siempre de una variable de entorno secreta.
SECRET_KEY = env('SECRET_KEY', default='django-insecure-plantilla-didactica-default-key-change-in-production')

# Modo depuración:
# - True: Muestra pantallas detalladas con el error si algo falla (Ideal para aprender).
# - False: Oculta errores al usuario final (Obligatorio en producción).
DEBUG = env('DEBUG', default=True)

# Lista de dominios e IPs desde las cuales se puede acceder a esta web
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0'])

# ------------------------------------------------------------------------------
# 3. APLICACIONES INSTALADAS (INSTALLED_APPS)
# ------------------------------------------------------------------------------
# Django se compone de aplicaciones modulares.
# - Apps del Core de Django: Módulos estándar provistos por el framework.
# - Apps Locales (Tus Apps): Las que creamos en la carpeta 'apps/'.
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',          # Panel de administración prefabricado (/admin)
    'django.contrib.auth',           # Sistema de autenticación de usuarios y permisos
    'django.contrib.contenttypes',   # Sistema de tipos de contenido de Django
    'django.contrib.sessions',       # Gestión de sesiones de usuario
    'django.contrib.messages',       # Mensajes flash informativos (éxito, error)
    'django.contrib.staticfiles',    # Manejador de archivos estáticos (CSS, JS, imágenes)
]

LOCAL_APPS = [
    'apps.core.apps.CoreConfig',     # App base de bienvenida y utilidades globales
    'apps.manual.apps.ManualConfig', # App didáctica del Manual del Alumno
]

# Switch didáctico: Si la app de manual está activa, la exponemos
ENABLE_STUDENT_MANUAL = env('ENABLE_STUDENT_MANUAL', default=True)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# ------------------------------------------------------------------------------
# 4. MIDDLEWARE (Capa Intermedia de Procesamiento HTTP)
# ------------------------------------------------------------------------------
# Explicación exhaustiva para alumnos:
#
# ¿Qué es un Middleware?
# Es una cadena de filtros intermedios (patrón de diseño "Cebolla" o Pipeline).
# Toda petición HTTP que entra a tu servidor pasa por esta lista de middlewares
# ANTES de llegar a la vista (views.py). Luego, la respuesta generada por la vista
# vuelve a pasar por estos mismos middlewares en orden inverso ANTES de enviarse
# al navegador del usuario.
#
# Flujo visual:
#   Navegador (Petición HTTP entrante)
#         │
#         ▼
#     [ 1. SecurityMiddleware       ] -> Aplica cabeceras de seguridad (SSL, XSS)
#     [ 2. SessionMiddleware        ] -> Lee/crea cookie de sesión (request.session)
#     [ 3. CommonMiddleware         ] -> Normaliza URLs (agrega '/' si falta)
#     [ 4. CsrfViewMiddleware       ] -> Valida token de seguridad {% csrf_token %}
#     [ 5. AuthenticationMiddleware ] -> Asocia el usuario logueado a 'request.user'
#     [ 6. MessageMiddleware        ] -> Gestiona alertas flash (messages.success)
#     [ 7. XFrameOptionsMiddleware  ] -> Bloquea ataques de Clickjacking (iframes)
#         │
#         ▼
#     Vista (views.py) -> Procesa datos y retorna HTML/JSON
#         │
#         ▼ (Respuesta HTTP saliente: recorre la lista en orden inverso)
#   Navegador (Recibe la página)
#
# ¡EL ORDEN ES CRUCIAL!
# Por ejemplo: 'AuthenticationMiddleware' necesita saber qué sesión tiene el usuario,
# por lo tanto DEBE colocarse obligatoriamente DESPUÉS de 'SessionMiddleware'.
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    # 1. Seguridad básica: Agrega encabezados HTTP de protección (X-Content-Type-Options, etc.)
    'django.middleware.security.SecurityMiddleware',

    # 2. Manejo de Sesiones: Lee la cookie de sesión del navegador y crea el diccionario
    #    'request.session', permitiendo persistir datos del usuario entre distintas páginas.
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 3. Utilidades comunes: Normaliza URLs (redirige automáticamente si falta la barra final '/')
    #    y gestiona encabezados estándar de navegadores.
    'django.middleware.common.CommonMiddleware',

    # 4. Protección CSRF (Cross-Site Request Forgery): Evita que un sitio web malicioso envíe
    #    peticiones POST simuladas a nombre de un usuario autenticado. Obliga a que todo
    #    formulario HTML incluya la etiqueta {% csrf_token %}.
    'django.middleware.csrf.CsrfViewMiddleware',

    # 5. Autenticación de Usuarios: Toma el ID almacenado en la sesión y carga el objeto
    #    del usuario en 'request.user'. Si no inició sesión, 'request.user.is_authenticated' es False.
    #    (Requiere que SessionMiddleware esté ubicado antes en esta lista).
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 6. Mensajes Flash: Permite almacenar notificaciones temporales de un solo uso
    #    ('messages.success', 'messages.error') que se borran automáticamente al ser mostradas.
    'django.contrib.messages.middleware.MessageMiddleware',

    # 7. Protección contra Clickjacking: Evita que tu sitio web sea incrustado dentro
    #    de un elemento <iframe> invisible en otra página web para engañar al usuario.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo de enrutador de URLs principal
ROOT_URLCONF = 'config.urls'

# ------------------------------------------------------------------------------
# 5. PLANTILLAS / TEMPLATES (Capa de Presentación HTML)
# ------------------------------------------------------------------------------
# Configura el motor de renderizado HTML y las carpetas donde buscar plantillas.
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Carpeta global 'templates/' en la raíz para base.html y vistas compartidas
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Permite buscar templates dentro de la carpeta templates/ de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Permite acceder a {{ request }} en HTML
                'django.contrib.auth.context_processors.auth', # Permite acceder a {{ user }} en HTML
                'django.contrib.messages.context_processors.messages', # Permite mostrar mensajes en HTML
                # Context processor didáctico para exponer flags globales a los templates
                'apps.core.context_processors.global_context',
            ],
        },
    },
]

# Punto de entrada para servidores web WSGI (ej. Gunicorn)
WSGI_APPLICATION = 'config.wsgi.application'

# ------------------------------------------------------------------------------
# 6. BASE DE DATOS (DATABASES)
# ------------------------------------------------------------------------------
# Lee la URL de la base de datos desde .env (DATABASE_URL)
# Formato PostgreSQL: postgres://usuario:password@host:puerto/nombre_bd
# Si no hay DATABASE_URL configurada, utiliza SQLite local automáticamente.
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# ------------------------------------------------------------------------------
# 7. VALIDACIÓN DE CONTRASEÑAS
# ------------------------------------------------------------------------------
# Reglas de seguridad automáticas para contraseñas de usuarios.
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------------------
# 8. INTERNACIONALIZACIÓN Y ZONA HORARIA
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'es-ar'      # Español (Argentina)
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True              # Habilita sistema de traducción
USE_TZ = True                # Habilita almacenamiento de fechas con zona horaria UTC

# ------------------------------------------------------------------------------
# 9. ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ------------------------------------------------------------------------------
# URL pública para acceder a los archivos estáticos desde el navegador
STATIC_URL = 'static/'

# Carpetas adicionales donde Django busca estáticos durante el desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Carpeta donde se recopilan todos los estáticos para producción (con collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos subidos por los usuarios (Media)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------------------
# 10. REDIRECCIONES DE AUTENTICACIÓN
# ------------------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# ------------------------------------------------------------------------------
# 11. CONFIGURACIÓN DE CORREO ELECTRÓNICO
# ------------------------------------------------------------------------------
# En desarrollo local usamos console.EmailBackend para imprimir los correos en la terminal
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# ------------------------------------------------------------------------------
# 12. TIPO DE CLAVE PRIMARIA (PRIMARY KEY) POR DEFECTO PARA MODELOS
# ------------------------------------------------------------------------------
# Explicación para alumnos:
# Cuando creas una clase en models.py sin especificar un campo 'id' manual,
# Django crea automáticamente una clave primaria autoincremental: 'id = models.AutoField(...)'.
#
# 'BigAutoField' es un entero de 64 bits (en vez de 32 bits estándar).
# ¿Por qué se usa?
# - AutoField (32 bits): Permite hasta ~2.147 millones de registros (2^31 - 1).
# - BigAutoField (64 bits): Permite hasta 9 trillones de registros (2^63 - 1).
# Es el estándar moderno en Django desde la versión 3.2 para evitar que una base de datos
# se quede sin identificadores si la tabla crece mucho.
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# 12. CONFIGURACIÓN DE IA (ANTHROPIC CLAUDE)
# ------------------------------------------------------------------------------
ANTHROPIC_API_KEY = env('ANTHROPIC_API_KEY', default='')
