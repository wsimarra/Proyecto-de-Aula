# QA Report — Proyecto Aula V9.0

- [x] `app/main.py` compila con `py_compile`.
- [x] Suite de pruebas: 6 pruebas aprobadas (3 heredadas + 3 nuevas de V9.0).
- [x] `/api/students`: 200; 726 registros en contexto sin filtros.
- [x] Cada fila expone seguimiento 2/3 como nulo y definitiva igual a la nota grupal.
- [x] `/api/teachers`: 200; 77 docentes en contexto completo.
- [x] Filtros de estado de docentes responden 200.
- [x] `/api/export/students.xlsx`: 200 y devuelve un XLSX válido.
- [x] JavaScript inline validado con `node --check`.

## Limitación de fuente
La fuente del modelo solo contiene registros de notas con corte `TERCERO`. No contiene Seguimiento 2 ni Seguimiento 3, ni identifica el usuario que registró una calificación. Esos campos se indican transparentemente como no disponibles.

## Resultado de estado docente observado en el modelo
Las 151 asignaciones docente-asignatura-cohorte tienen al menos un registro de nota TERCERO; por tanto, el estado derivado actualmente aparece como “CON NOTAS” para los 77 docentes. Esto no prueba quién digitó las notas ni descarta que existan pendientes en otros cortes que no están cargados.
