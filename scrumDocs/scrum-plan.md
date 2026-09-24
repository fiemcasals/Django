# Plan de Requerimientos — django

_Generado automáticamente el 2026-09-24T19:25:27.891Z — no editar a mano, se sobreescribe en cada publicación._

Orden sugerido de desarrollo (respeta dependencias entre Requerimientos). Cada fila indica de qué Requerimientos depende, si tiene.

| Orden | Código | Requerimiento | Historia de Usuario | Módulo | Entrega | Estado | Desarrollador | Depende de | Rechazos |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RF-01 | Configuración central y estructura modular de aplicaciones Django | HU-01 | — | — | Hecho | dev-django | — | — |
| 2 | RNF-01 | Contenerización del entorno con Docker, docker-compose y PostgreSQL | HU-01 | — | — | Hecho | dev-django | RF-01 | — |
| 3 | RF-01 | Módulo interactivo de Guía/Manual del Alumno con switch de activación | HU-02 | — | — | Hecho | dev-django | RF-01 | — |
| 4 | RF-01 | Sistema de inicio, cierre de sesión y control de acceso | HU-03 | — | — | Haciendo | dev-django | RF-01 | — |
| 5 | RF-01 | Modelos de datos con indexación y métodos de extracción de catálogo/índice | HU-04 | — | — | Hacer | dev-django | RF-01 | — |
| 6 | RF-02 | Circuito de restablecimiento y cambio de contraseña con emisor de consola | HU-03 | — | — | Hacer | dev-django | RF-01 | — |
| 7 | RF-02 | Interfaz Web CRUD para gestión de datos con validaciones | HU-04 | — | — | Hacer | dev-django | RF-01 | — |
| 8 | RF-01 | Servicio de IA con Anthropic SDK, Tool Calling en dos pasos y optimización de tokens | HU-05 | — | — | Hacer | dev-django | RF-01 | — |
| 9 | RF-02 | Interfaz Web y Chat Didáctico para consultas con visualización del flujo de IA | HU-05 | — | — | Hacer | dev-django | RF-01 | — |

## Detalle

### RF-01 — Configuración central y estructura modular de aplicaciones Django
Inicio de desarrollo de RF-01: Configuración central y estructura modular de aplicaciones Django
- Estimado: 4h

### RNF-01 — Contenerización del entorno con Docker, docker-compose y PostgreSQL
- Estimado: 4h

### RF-01 — Módulo interactivo de Guía/Manual del Alumno con switch de activación
- Estimado: 4h

### RF-01 — Sistema de inicio, cierre de sesión y control de acceso
- Estimado: 3h

### RF-01 — Modelos de datos con indexación y métodos de extracción de catálogo/índice
- Estimado: 3h

### RF-02 — Circuito de restablecimiento y cambio de contraseña con emisor de consola
- Estimado: 3h

### RF-02 — Interfaz Web CRUD para gestión de datos con validaciones
- Estimado: 3h

### RF-01 — Servicio de IA con Anthropic SDK, Tool Calling en dos pasos y optimización de tokens
- Estimado: 4h

### RF-02 — Interfaz Web y Chat Didáctico para consultas con visualización del flujo de IA
- Estimado: 3h
