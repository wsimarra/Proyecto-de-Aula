# PROYECTOS DE AULA V5.2 — QA DATA / MATEMÁTICA / ESTADÍSTICA

Fecha: 2026-09-21

## Base revisada
- 26 archivos Excel únicos, semestres SEM-01 a SEM-06.
- 26 cohortes operativas.
- 154 proyectos válidos.
- 8 registros excluidos del universo inicial de 162.

## Indicadores validados
- Proyectos válidos: 154.
- Distribución: SEM-01 44, SEM-02 21, SEM-03 37, SEM-04 13, SEM-05 24, SEM-06 15.
- Suma: 44 + 21 + 37 + 13 + 24 + 15 = 154.
- Porcentajes sobre 154: 28.57%, 13.64%, 24.03%, 8.44%, 15.58%, 9.74%; suma redondeada = 100.00%.
- Promedio final general: 4.08 (cálculo no redondeado ≈ 4.0794).
- Docentes únicos: 77.
- Asignaturas únicas: 36.
- Cohortes: 26.
- Líderes de colectivo: 26 asignaciones / 18 docentes únicos.

## Estudiantes: definición corregida
La tarjeta institucional **ESTUDIANTES EN PROYECTOS** utiliza la suma de integrantes de los 154 proyectos válidos, no el conteo global de nombres únicos de toda la fuente.

- Estudiantes/participaciones en proyectos válidos: **726**.
- Personas únicas dentro de proyectos válidos: **725**.
- Estudiantes únicos registrados en toda la fuente: 752.

La cifra de 726 es la que debe mostrarse en la tarjeta de impacto de Proyectos de Aula, porque corresponde al total de estudiantes asociados a los proyectos válidos. Un mismo estudiante puede participar en más de un proyecto; por eso 726 participaciones no equivale necesariamente a 726 personas únicas.

## Distribución de estudiantes por semestre en el modelo actual
- SEM-01: 212
- SEM-02: 98
- SEM-03: 167
- SEM-04: 65
- SEM-05: 111
- SEM-06: 73
- Total: 726.

**Observación:** el reporte institucional mostrado en conversación presenta SEM-03 = 168 y SEM-05 = 110. El total sigue siendo 726, pero existe una diferencia de una participación entre esos dos semestres. No se debe modificar silenciosamente sin volver a cotejar los Excel fuente.

## Cobertura
- 154/154 proyectos tienen un valor de nota registrado, por lo que la cobertura técnica es 100%.
- La auditoría debe diferenciar existencia de nota de nota positiva: hay 153 proyectos con nota > 0 y 1 proyecto con nota 0.

## Duplicados
- Matrículas actuales: 4461 relaciones, sin duplicados exactos detectados en la V5.1.
- Notas actuales: 4369 registros, sin duplicados exactos detectados en la V5.1.

## Líderes de colectivo
- 26 asignaciones, una por sección.
- 18 docentes únicos.
- Un mismo docente puede liderar varias secciones y no se deduplica como asignación.
- El conteo de estudiantes de líderes utiliza estudiantes asociados a proyectos válidos, no todas las matrículas de la cohorte.

## Pruebas API V5.2
- GET /: PASS
- GET /api/meta: PASS
- GET /api/dashboard: PASS
- GET /api/students: PASS (726 filas de participación de proyecto)
- GET /api/collective-leaders: PASS (26 asignaciones, 18 líderes, 726 estudiantes en proyectos)
- Filtro líder Jennifer Giraldo Guzman: PASS (2 secciones, 16 proyectos, 76 participaciones estudiantiles)
- GET /api/audit: PASS (154 válidos, 726 participaciones, 725 personas únicas, 8 excluidos)
- Python compile: PASS

## Resultado QA
**PASS con observación:** los indicadores principales quedan corregidos y consistentes con la definición de estudiantes en proyectos: 154 proyectos, 726 participaciones estudiantiles, 77 docentes, 36 asignaturas y 26 cohortes.

Pendiente antes de declarar cierre institucional: cotejar la distribución SEM-03/SEM-05 (168/110 en el reporte institucional vs 167/111 en el modelo actual) y validar académicamente el único proyecto con nota 0.
