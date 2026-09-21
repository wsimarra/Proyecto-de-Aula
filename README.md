# Proyectos de Aula — V4 DESTACADOS LOCAL

## Fuente
26 archivos Excel únicos de Tecnología en Gestión de Negocios Internacionales, semestres 01 a 06. Los archivos duplicados por nombre con (1)/(2) tenían el mismo hash y se consolidaron en una sola copia.

## Ejecutar
Windows: doble clic en `run_windows.bat`. Busca un puerto libre y abre el navegador automáticamente.

## Modelo
La V3 usa los datos reales de los Excel y un modelo JSON generado por ETL. El dashboard consulta una API FastAPI.

## Reglas validadas
- Sección operativa: nombre del archivo `SEM-XX-SEC-YY`.
- Sección interna de `LIDER!H2` se conserva para auditoría.
- Periodo local: 2026-1 / Primer periodo, como contexto de esta fuente.
- Nota final de grupo: promedio de `DEFINITIVAS!E` (TER-CORTE) para estudiantes con nota válida del grupo.
- Título: `LIDER`, sección TITULOS DE LOS PROYECTOS DE AULA, filas 29-40, por posición G01-G12.
- Proyecto destacado: mayor promedio final disponible por semestre; empates se conservan.

## Calidad detectada
Existe una inconsistencia en `TGNI-SEM-02-SEC-04.xlsx`: el nombre indica SEC-04, mientras `LIDER!H2` indica sección 1. La V3 usa SEC-04 como sección operativa porque es la convención del archivo y lo deja visible en Auditoría.

## V4 — Proyectos destacados
- Top 5 de proyectos con nota dentro del contexto de filtros seleccionado.
- Proyecto(s) destacado(s) por semestre, conservando empates.
- Detalle de integrantes por proyecto.
- Espacio para vincular el PDF de cada proyecto mediante `data/project_documents.json`.
- El PDF se abre mediante un enlace; en esta versión no se almacena el archivo binario dentro del servicio Render.
- Criterio mostrado: mayor promedio final del grupo según TERCER CORTE de DEFINITIVAS.

## Siguiente fase
Sustituir la fuente local por OneDrive/SharePoint mediante Microsoft Graph, sin rehacer el modelo ni la interfaz.


### PDF de proyectos destacados
La V4 permite **📎 Adjuntar PDF** y **📄 Ver PDF** en cada proyecto destacado. Los archivos se guardan en `data/pdfs/` y la relación queda en `data/project_documents.json`. Para producción institucional se recomienda migrar estos documentos a OneDrive/SharePoint, porque el almacenamiento local de Render no debe considerarse permanente.
