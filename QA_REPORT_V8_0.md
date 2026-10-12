# QA V8.0 — BI Institucional

## Alcance
V8.0 aplica los bloques solicitados: Datos, BI y UX/UI sobre la base V7.0.

## Bloque 1 — Datos
- Se mantienen **154 proyectos válidos**.
- Se mantienen **58 títulos genéricos positivos** porque son valores reales de la fuente.
- Los títulos genéricos se identifican como `GENÉRICO DE FUENTE`; no se inventan nombres.
- Se conserva la regla especial: un registro con nota 0 y título genérico se excluye por falta de evidencia suficiente.
- El KPI de participaciones sigue en **726**.
- Estudiantes únicos dentro de proyectos válidos: **725**.
- Promedio simple de notas grupales: **4.08**.
- Promedio ponderado por estudiantes: **4.11**.

## Bloque 3 — BI
- KPI de asignaturas ahora es dinámico y responde a filtros; ya no está hardcodeado en 36.
- Se separan `SECCIONES` y `COHORTES` para evitar mezclar conceptos.
- Se explicita la definición del promedio.
- Se evita mezclar proyectos y participaciones en una sola escala visual.
- El historial separa promedio y participación estudiantil.
- La distribución de notas usa bandas académicas: 0–2.99, 3.00–3.49, 3.50–3.99, 4.00–4.49, 4.50–5.00.
- Las asignaturas muestran nombres completos en tooltip/etiqueta de datos; el sistema no genera abreviaturas del nombre.

## Bloque 4 — UX/UI
- Paleta institucional azul, rojo y blanco con menos gradientes decorativos.
- Tipografía y etiquetas ampliadas para lectura en pantalla.
- Mayor jerarquía visual en encabezado, filtros, KPIs y paneles.
- Los proyectos se muestran en MAYÚSCULAS y sin truncamiento por puntos suspensivos.
- Las tarjetas de proyecto muestran grupo, semestre, sección, proyecto y nota.
- Se identifica visualmente un título genérico proveniente de la fuente.
- Diseño responsive para escritorio, tablet y móvil.
- Botones, filtros, tablas y estados de carga con mayor contraste y consistencia.

## Validaciones automáticas
- Conteo de archivos: 26.
- Proyectos válidos: 154.
- Títulos genéricos de fuente incluidos: 58.
- Participaciones: 726.
- Docentes: 77.
- Asignaturas: 36.
- Secciones: 26.
- Promedio simple: 4.08.
- Promedio ponderado: 4.11.
- Cobertura de nota: 100%.
