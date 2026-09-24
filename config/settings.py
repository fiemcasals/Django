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
]

# Switch didáctico: Si la app de manual está activa, la registramos
ENABLE_STUDENT_MANUAL = env('ENABLE_STUDENT_MANUAL', default=True)
if ENABLE_STUDENT_MANUAL:
    # Podrá ser incorporada en apps/manual/ en HU-02
    pass

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# ------------------------------------------------------------------------------
# 4. MIDDLEWARE (Filtros de Peticiones y Respuestas)
# ------------------------------------------------------------------------------
# Los middlewares son capas intermedias que procesan cada solicitud HTTP antes
# de llegar a las vistas y antes de enviar la respuesta al navegador.
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gestiona sesiones entre peticiones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',            # Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Asocia request.user al usuario actual
    'django.contrib.messages.middleware.MessageMiddleware',  # Habilita el sistema de mensajes
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

# Clave primaria por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# 12. CONFIGURACIÓN DE IA (ANTHROPIC CLAUDE)
# ------------------------------------------------------------------------------
ANTHROPIC_API_KEY = env('ANTHROPIC_API_KEY', default='')
