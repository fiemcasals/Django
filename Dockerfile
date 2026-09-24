# ==============================================================================
# Dockerfile - Entorno de Ejecución Contenerizado para Django
# ==============================================================================
# ¿Qué es un Dockerfile?
# Es una receta paso a paso para construir una imagen de contenedor independiente y
# reproducible. Garantiza que la aplicación se ejecute exactamente igual en la máquina
# de cualquier desarrollador, en testing o en producción, sin depender de lo que cada uno
# tenga instalado en su sistema operativo.
# ==============================================================================

# 1. IMAGEN BASE
# Usamos Python 3.12 en su variante 'slim'.
# 'slim' es una versión ligera basada en Debian que incluye Python sin paquetes
# innecesarios, reduciendo el tamaño de la imagen y mejorando la velocidad de descarga y seguridad.
FROM python:3.12-slim

# 2. VARIABLES DE ENTORNO DE PYTHON
# PYTHONDONTWRITEBYTECODE=1: Evita que Python genere archivos .pyc en el disco del contenedor,
# manteniendo la imagen limpia y ahorrando espacio.
# PYTHONUNBUFFERED=1: Fuerza a Python a enviar los logs (stdout y stderr) directamente a la terminal
# en tiempo real sin almacenarlos en búfer, facilitando el monitoreo con 'docker logs'.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. DIRECTORIO DE TRABAJO
# Define la carpeta dentro del contenedor donde residirá y se ejecutará todo el código de la app.
WORKDIR /app

# 4. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA OPERATIVO
# Instalamos herramientas mínimas necesarias para compilar librerías en C y conectar con PostgreSQL:
# - gcc: Compilador de C necesario para compilar paquetes nativos.
# - libpq-dev: Librería de desarrollo de PostgreSQL necesaria para psycopg2.
# - curl: Herramienta de red útil para comprobaciones de estado (healthchecks).
# Limpiamos la caché de apt (/var/lib/apt/lists/*) al final de la misma capa para no inflar la imagen.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. COPIAR E INSTALAR DEPENDENCIAS DE PYTHON
# Aprovechamos el sistema de caché por capas de Docker: copiamos primero requirements.txt
# e instalamos las dependencias. De esta forma, si cambiamos código de la aplicación pero no
# requirements.txt, Docker reutiliza la capa cacheada sin reinstalar todo.
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. COPIAR EL CÓDIGO FUENTE
# Copia todos los archivos del proyecto al directorio de trabajo /app dentro del contenedor.
COPY . /app/

# 7. PUERTO EXPUESTO
# Documenta que el contenedor escucha en el puerto 8000 (puerto estándar de Django runserver).
EXPOSE 8000

# 8. COMANDO POR DEFECTO
# Ejecuta el servidor de desarrollo escuchando en 0.0.0.0 (todas las interfaces del contenedor)
# para que sea accesible desde la máquina anfitriona (host).
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
