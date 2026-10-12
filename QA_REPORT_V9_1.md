# QA V9.1 — notas individuales

- Python compile: PASS.
- Tests base V8/modelo: 3/3 PASS.
- Hoja `DEFINITIVAS` leída en 26 archivos Excel.
- Filas de cortes indexadas por cohorte, estudiante y grupo: 727 claves.
- Registros de estudiantes en el endpoint: 726.
- Registros con Seguimiento 2 ausente: 0.
- Registros con Seguimiento 3 ausente: 0.
- Definitivas individuales ausentes: 0.
- Caso comprobado desde `TGNI-SEM-01-SEC-01.xlsx`: LUIS JOSE AGUILAR RAMOS, G01; SEG-CORTE 4,2; TER-CORTE 4,6; definitiva individual 4,40.
- Exportación usa las mismas notas y la definitiva individual calculada.

## Regla
Seguimiento 2 = `SEG-CORTE`; Seguimiento 3 = `TER-CORTE`; definitiva = promedio simple (50 % cada uno) de los valores mostrados a un decimal. Si falta un corte válido, no se inventa la definitiva.
