PROYECTOS DE AULA V3 — QA REPORT
Fecha: 2026-09-21

FUENTE
- 26 archivos Excel únicos.
- 54 archivos físicos detectados inicialmente; los duplicados con (1)/(2) tenían SHA-256 idéntico y se consolidaron.
- Semestres: SEM-01 a SEM-06.
- Cohortes operativas: 26.
- Programa: TECNOLOGÍA EN GESTIÓN DE NEGOCIOS INTERN.
- Periodo configurado: 2026-1 / Primer periodo (contexto de la fuente; no existe como campo dentro de las celdas revisadas).

MODELO
- Estudiantes únicos por nombre normalizado: 752
- Docentes: 77
- Asignaturas: 36
- Grupos/proyectos: 162
- Relaciones de matrícula: 4466
- Notas de tercer corte por estudiante/asignatura: 4374
- Títulos de proyecto no genéricos: 96/162

REGLAS
- Sección operativa: nombre de archivo SEM-XX-SEC-YY.
- Auditoría de sección: LIDER!H2.
- Nota final de grupo: promedio de DEFINITIVAS!E (TER-CORTE).
- Título: LIDER filas 29-40, columna E, posición G01-G12.
- Destacado: mayor promedio final por semestre; empates conservados.

PRUEBAS
1. Compilación Python: PASS
2. Sintaxis JavaScript (Node --check): PASS
3. Arranque Uvicorn: PASS
4. GET /api/meta: PASS
5. GET /api/dashboard: PASS
6. Filtro SEM-03 -> secciones: PASS
7. Filtro SEM-03 + sección -> grupos: PASS
8. Filtro SEM-03 + sección + grupo -> docentes: PASS
9. Filtro docente -> dashboard con datos: PASS
10. Endpoint estudiantes: PASS
11. Endpoint docentes: PASS
12. Auditoría detecta discrepancia de sección: PASS

CONTROL DE CALIDAD DETECTADO
- 1 discrepancia: TGNI-SEM-02-SEC-04.xlsx declara SEC-04 en el nombre, pero LIDER!H2 contiene sección 1.
- La V3 usa SEC-04 como clave operativa y muestra la discrepancia en Auditoría; no se oculta ni se corrige silenciosamente.
- La prueba visual automatizada con Playwright no pudo ejecutarse porque el entorno de ejecución bloqueó el acceso del navegador headless a localhost (ERR_BLOCKED_BY_ADMINISTRATOR). La aplicación y API sí fueron probadas directamente.

RESULTADO
Backend, modelo, endpoints, filtros dependientes y sintaxis frontend: PASS.
Validación visual final: pendiente de ejecutarse en el Windows del usuario, donde ya existe Chromium/Edge y el servidor local.
