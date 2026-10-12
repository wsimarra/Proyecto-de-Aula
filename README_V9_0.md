# Proyecto Aula V9.0 — BI Institucional

## Novedades de esta versión

### Estudiantes
- Búsqueda instantánea por nombre/apellido y título del proyecto.
- Columnas Nota seguimiento 2, Nota seguimiento 3 y Definitiva general individual (50/50).
- Definitiva general individual = promedio simple de SEG-CORTE y TER-CORTE, con peso 50 % cada uno.
- Exportación Excel de notas; respeta filtros globales y texto de búsqueda.
- La V9.1 lee SEG-CORTE y TER-CORTE de la hoja DEFINITIVAS de cada Excel; la definitiva individual se calcula como el promedio de ambos cortes.

### Docentes
- Estado de notas inferido por registros TERCERO disponibles para asignatura/cohorte.
- Filtros: todos, con notas registradas, sin notas registradas y con asignaciones pendientes.
- Conteo de asignaciones con notas y pendientes.
- La fuente no registra quién digitó cada nota; el tablero no atribuye autoría individual.

## Ejecución local
Windows: ejecutar `run_windows.bat` desde la carpeta raíz.
También se puede ejecutar `python run_local.py`.

## Validación importante
Los campos de seguimiento 2/3 no están presentes en el modelo de origen actual. Para llenarlos se requiere incorporar los cortes originales correspondientes desde los Excel institucionales.


## Inicio corregido en Windows (V9.0.1)

Ejecuta `run_windows.bat`. El lanzador usa directamente `.venv\\Scripts\\python.exe` y no depende de activar el entorno con `activate.bat`. Si Python no está instalado, instala Python 3.10 o superior y marca la opción `Add Python to PATH`.
