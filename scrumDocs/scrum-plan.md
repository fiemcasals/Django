# Plan de Requerimientos — django

_Generado automáticamente el 2026-09-24T17:49:14.543Z — no editar a mano, se sobreescribe en cada publicación._

Orden sugerido de desarrollo (respeta dependencias entre Requerimientos). Cada fila indica de qué Requerimientos depende, si tiene.

| Orden | Código | Requerimiento | Historia de Usuario | Módulo | Entrega | Estado | Desarrollador | Depende de | Rechazos |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RF-01 | Configuración central y estructura modular de aplicaciones Django | HU-01 | — | — | Hacer | dev-django | — | — |
| 2 | RNF-01 | Contenerización del entorno con Docker, docker-compose y PostgreSQL | HU-01 | — | — | Hacer | dev-django | RF-01 | — |
| 3 | RF-01 | Módulo interactivo de Guía/Manual del Alumno con switch de activación | HU-02 | — | — | Hacer | dev-django | RF-01 | — |
| 4 | RF-01 | Sistema de inicio, cierre de sesión y control de acceso | HU-03 | — | — | Hacer | dev-django | RF-01 | — |
| 5 | RF-02 | Circuito de restablecimiento y cambio de contraseña con emisor de consola | HU-03 | — | — | Hacer | dev-django | RF-01 | — |

## Detalle

### RF-01 — Configuración central y estructura modular de aplicaciones Django
- Estimado: 4h

### RNF-01 — Contenerización del entorno con Docker, docker-compose y PostgreSQL
- Estimado: 4h

### RF-01 — Módulo interactivo de Guía/Manual del Alumno con switch de activación
- Estimado: 4h

### RF-01 — Sistema de inicio, cierre de sesión y control de acceso
- Estimado: 3h

### RF-02 — Circuito de restablecimiento y cambio de contraseña con emisor de consola
- Estimado: 3h
