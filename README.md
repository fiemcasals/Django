# 🚀 Plantilla Django Didáctica para Clases

Esta es una plantilla base para proyectos de Django 5.x diseñada con fines pedagógicos. Está pensada para que alumnos con o sin conocimientos avanzados puedan comprender la arquitectura de Django, su separación modular, la integración con bases de datos relacionales (PostgreSQL), la contenerización con Docker y cómo extenderla.

---

## 📁 Estructura del Proyecto

```text
├── config/                  # Paquete de Configuración Central
│   ├── settings.py          # Ajustes centrales comentados línea por línea
│   ├── urls.py              # Enrutador de URLs principal
│   ├── wsgi.py / asgi.py    # Interfaces de despliegue
├── apps/                    # Directorio de Aplicaciones Modulares
│   ├── core/                # Aplicación base de bienvenida
│   │   ├── models.py        # Entidades y tablas de la Base de Datos (ORM)
│   │   ├── views.py         # Controladores de respuesta a peticiones
│   │   ├── forms.py         # Formularios y validaciones
│   │   ├── urls.py          # Enrutamiento local de la app
│   │   ├── admin.py         # Registro en el panel de administración
│   │   └── tests.py         # Pruebas unitarias automatizadas
├── templates/               # Capa de Presentación HTML (DTL)
│   ├── base.html            # Plantilla maestra con navegación y footer común
│   └── core/index.html      # Página de inicio didáctica
├── static/                  # Archivos Estáticos
│   ├── css/styles.css       # Estilos con variables CSS modernas
│   └── js/main.js           # Scripts del navegador
├── Dockerfile               # Receta de construcción de imagen Docker (Python 3.12 slim)
├── docker-compose.yml       # Orquestador de servicios (Web Django + DB PostgreSQL 16)
├── .dockerignore            # Archivos excluidos del contexto Docker
├── manage.py                # Script ejecutable de gestión de Django
├── requirements.txt         # Dependencias de Python
├── .env.example             # Plantilla de variables de entorno documentadas
└── .gitignore               # Exclusiones de control de versiones
```

---

## 🐳 Opción 1: Puesta en Marcha con Docker y PostgreSQL (Recomendada)

Docker permite levantar la aplicación y el motor de base de datos PostgreSQL en contenedores aislados sin necesidad de instalar Python ni PostgreSQL en tu máquina física.

### 1. Construir e iniciar los servicios:
```bash
docker compose up --build
```
> **Nota:** La bandera `-d` (daemon) se puede agregar si querés que corra en segundo plano: `docker compose up -d`.

### 2. Aplicar migraciones de base de datos en PostgreSQL:
```bash
docker compose exec web python manage.py migrate
```

### 3. Crear usuario Administrador (Superuser):
```bash
docker compose exec web python manage.py createsuperuser
```

### 4. Ejecutar las pruebas automatizadas dentro del contenedor:
```bash
docker compose exec web python manage.py test
```

### 5. Detener los contenedores:
```bash
docker compose down
```
*(Si querés borrar también el volumen de base de datos: `docker compose down -v`)*

---

## 🛠️ Opción 2: Puesta en Marcha en Entorno Local Tradicional

### 1. Clonar el repositorio y entrar a la carpeta:
```bash
git clone https://github.com/fiemcasals/Django.git
cd Django
```

### 2. Crear y activar el entorno virtual (`venv`):
* En Windows (PowerShell):
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* En Linux / macOS:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno:
Copiá el archivo de ejemplo `.env.example` como `.env`:
* En Windows: `copy .env.example .env`
* En Linux / macOS: `cp .env.example .env`

### 5. Crear y aplicar las migraciones iniciales:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear un usuario Administrador:
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```
Abrí tu navegador en: `http://localhost:8000/`  
Panel de administración: `http://localhost:8000/admin/`

---

## 🧪 Ejecutar Pruebas Automatizadas (Tests)

Para verificar que todos los componentes y vistas funcionen correctamente:
```bash
python manage.py test
```
O para probar una app específica:
```bash
python manage.py test apps.core
```

---

## 📚 Comandos Útiles para Alumnos

* **Comprobar la configuración:** `python manage.py check`
* **Crear una nueva app modular:** `python manage.py startapp nombre_app apps/nombre_app`
* **Ejecutar comandos dentro de Docker:** `docker compose exec web python manage.py <comando>`