# QA V9.2 — Seguimiento de docentes

## Pruebas realizadas
- Sintaxis Python: pendiente de ejecutar en este paquete.
- Sintaxis JavaScript: pendiente de ejecutar si Node está disponible.
- Endpoint `/api/teacher-detail`: agregado.
- Navegación por clic, Enter y barra espaciadora: implementada.
- Filtro y búsqueda del detalle: implementados.
- Exportación de seguimiento a CSV: implementada.

## Regla de negocio
Una fila del detalle representa la relación docente + asignatura + cohorte + grupo/proyecto. Las notas existentes se verifican contra los estudiantes inscritos en ese grupo y asignatura. Estado:
- CON NOTAS: todos los estudiantes del grupo tienen nota.
- PARCIAL: algunos estudiantes tienen nota.
- PENDIENTE: no hay notas para los estudiantes del grupo, o no hay integrantes vinculados en la fuente.

La fuente no registra el usuario que digitó cada nota. No se debe interpretar el estado como auditoría de autoría.

## Validación pendiente del usuario
- Abrir la versión en Windows.
- Seleccionar 2 o 3 docentes de distintas asignaturas.
- Comparar grupos y proyectos mostrados contra los Excel de origen.
- Probar exportación y filtros.
