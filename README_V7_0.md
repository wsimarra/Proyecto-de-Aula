# Proyectos de Aula V7.0 — BI Institucional Inteligente

V7.0 consolida la evolución de V6.4 en una sola versión integral, manteniendo el modelo académico y las reglas de negocio validadas.

## Mejoras incluidas

1. Rediseño BI institucional azul/rojo/blanco con navegación lateral y experiencia responsive.
2. KPIs ejecutivos: proyectos, participaciones estudiantiles, docentes, asignaturas, cohortes y promedio final.
3. Filtros dependientes por periodo, programa, semestre, sección, grupo, docente y asignatura.
4. Gráficos interactivos con Chart.js para evolución, distribución, asignaturas y evaluación.
5. Módulo de proyectos con búsqueda, orden visual, exportación CSV y detalle modal.
6. Títulos de proyectos completos y en MAYÚSCULAS en las zonas de consulta.
7. Reconocimiento con trofeo/estrellas y destacados por semestre según mayor promedio final grupal; empates conservados.
8. Historial con comparación de promedio, proyectos y participaciones.
9. Evaluación con cobertura, promedio, faltantes y distribución de notas.
10. Módulos de estudiantes, docentes, líderes y programas.
11. Detalle de proyecto con estudiantes, líder, nota y PDF cuando existe.
12. Auditoría ampliada con reglas, exclusiones, discrepancias y trazabilidad.
13. Chat IA Libre con contexto de filtros y protección contra invenciones mediante fuente de verdad institucional.
14. Endpoint de estado del sistema y versión.
15. Endpoint de analítica consolidada.
16. Arquitectura preparada para OneDrive/SharePoint/Microsoft Graph.
17. Mejoras de responsive, accesibilidad visual, estados de carga, feedback y microinteracciones.

## Reglas académicas preservadas
- 154 proyectos válidos en el modelo actual.
- 726 participaciones estudiantiles.
- 77 docentes.
- 36 asignaturas.
- 26 cohortes.
- Promedio final global validado: 4.08.
- Nota final: promedio de DEFINITIVAS → TERCER CORTE → TER-CORTE.
- Título: LIDER → TITULOS DE LOS PROYECTOS DE AULA.
- Sección operativa: nombre del archivo, contrastado con LIDER!H2.

## Ejecución local
`py -m pip install -r requirements.txt`

`py run_local.py`

## Producción
Build: `pip install -r requirements.txt`

Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Variables: `OPENAI_API_KEY` y opcional `OPENAI_MODEL`.

Antes de uso institucional público se recomienda incorporar autenticación/autorización.
