# Proyecto Aula V9.1 — Notas individuales desde Excel

## Cambio principal: notas por estudiante
- `Nota seguimiento 2` se lee de la columna `SEG-CORTE` de la hoja `DEFINITIVAS`.
- `Nota seguimiento 3` se lee de la columna `TER-CORTE` de la hoja `DEFINITIVAS`.
- Ambas notas se presentan con un decimal, como en la hoja fuente.
- `Definitiva general individual` = (Seguimiento 2 + Seguimiento 3) / 2, con peso 50 % cada corte.
- Si alguna nota está vacía o contiene un error/texto no numérico, la definitiva queda pendiente; no se reemplaza por cero.
- La exportación Excel incluye las dos notas y la definitiva individual calculada.
- Las notas se relacionan por archivo/cohorte, estudiante y grupo.

Ejemplo de comprobación: 4,2 y 4,6 producen 4,40.

## Conservado
- 154 proyectos válidos, 726 participaciones estudiantiles, 77 docentes, 36 asignaturas y 26 cohortes.
- Filtros globales, búsqueda en estudiantes, exportación y módulos existentes.
- El criterio de proyecto destacado y las notas grupales en los módulos de proyectos no se alteran.

## Inicio en Windows
Ejecuta `run_windows.bat`. El lanzador crea `.venv` si hace falta, instala requisitos y espera a que el servidor esté disponible antes de abrir el navegador.

## Fuente y precisión
Las notas se leen de la hoja `DEFINITIVAS` de cada Excel. Las columnas D y E de esa hoja contienen `SEG-CORTE` y `TER-CORTE`. Cada corte se muestra redondeado a un decimal, según su presentación en la hoja, y el promedio se calcula a partir de esos valores mostrados.
