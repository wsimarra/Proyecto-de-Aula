# Proyecto Aula V9.2 — Seguimiento de calificación por docente

## Novedades
- Las filas de docentes son seleccionables con clic, Enter o barra espaciadora.
- Al seleccionar un docente, se abre el detalle de sus asignaturas, semestres, secciones, grupos y proyectos asociados.
- El detalle muestra cantidad de estudiantes, estudiantes con nota, pendientes y estado: CON NOTAS, PARCIAL o PENDIENTE.
- Búsqueda inmediata por proyecto, asignatura, grupo, semestre y sección.
- Filtro por estado de calificación.
- Exportación del detalle del docente a Excel (.xlsx), con filtros y columnas de seguimiento.
- Se conservan las calificaciones individuales SEG-CORTE / TER-CORTE y la definitiva 50/50 de V9.1.

## Interpretación responsable
La responsabilidad se infiere de la asignación docente-asignatura-cohorte. El estado se determina por existencia de notas para los estudiantes del grupo y asignatura. La fuente no identifica qué usuario digitó cada nota; por tanto, el tablero no afirma autoría individual de la calificación.

## Ejecutar en Windows
Doble clic en `run_windows.bat`. Si aparece un error, conserva la ventana abierta para ver el mensaje.

## Publicación
Build: `pip install -r requirements.txt`
Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Antes de publicar en producción, validar visualmente el módulo Docentes y revisar el acceso autorizado a los datos académicos.
