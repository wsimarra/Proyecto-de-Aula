# Proyectos de Aula — V3 FINAL LOCAL

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

## Siguiente fase
Sustituir la fuente local por OneDrive/SharePoint mediante Microsoft Graph, sin rehacer el modelo ni la interfaz.
