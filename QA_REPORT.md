# PROYECTOS DE AULA V5.1 — QA REPORT
Fecha: 2026-09-21

## FUENTE
- 26 archivos Excel únicos.
- Semestres: SEM-01 a SEM-06.
- Cohortes operativas: 26.
- Periodo: 2026-1 / Primer periodo.

## MODELO
- Estudiantes únicos: 752.
- Docentes: 77.
- Asignaturas: 36.
- Proyectos de Aula válidos: 154.
- Proyectos excluidos: 8.
- Relaciones de matrícula después de deduplicar registros exactos: 4461.
- Notas de tercer corte después de deduplicar registros exactos: 4369.
- Líderes de colectivo por sección: 26 asignaciones.
- Docentes únicos con rol de líder: 18.

## PROYECTOS
- SEM-01: 44
- SEM-02: 21
- SEM-03: 37
- SEM-04: 13
- SEM-05: 24
- SEM-06: 15
- Total: 154.

## LÍDERES DE COLECTIVO
- Fuente: hoja LIDER de cada Excel.
- Rol: fila/columna donde aparece LIDER; la asignatura asociada se toma de la celda correspondiente y el docente de la fila de nombres.
- La asignación se identifica por periodo + semestre + sección.
- El mismo docente puede liderar varias secciones; esas asignaciones se conservan y no se deduplican entre secciones.
- Endpoint: GET /api/collective-leaders.
- Filtros: periodo, semestre, sección, líder y asignatura del líder.

## PRUEBAS
1. Compilación Python: PASS
2. Sintaxis JavaScript (Node --check): PASS
3. GET /: PASS
4. GET /api/meta: PASS
5. GET /api/dashboard: PASS — 154 proyectos, 752 estudiantes.
6. GET /api/audit: PASS
7. GET /api/collective-leaders: PASS — 26 asignaciones, 18 líderes únicos.
8. Filtro SEM-01 en líderes: PASS — 6 secciones.
9. Filtro JENNIFER GIRALDO GUZMAN: PASS — 2 secciones.
10. Proyectos por semestre: PASS — 44/21/37/13/24/15.
11. Deduplicación exacta de matrícula: PASS — 5 duplicados exactos eliminados.
12. Deduplicación exacta de notas: PASS — 5 duplicados exactos eliminados.

## CONTROL DE CALIDAD
- Se conserva la discrepancia documentada de TGNI-SEM-02-SEC-04.xlsx: nombre de archivo SEC-04 frente a LIDER!H2 con sección 1. La sección operativa sigue siendo la del nombre del archivo y la discrepancia queda visible en Auditoría.
- Validación visual automatizada con Playwright no realizada en este entorno; debe verificarse en Windows/Edge del usuario.
