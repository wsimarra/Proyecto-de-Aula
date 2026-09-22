# Proyectos de Aula V6 — BI + Asistente IA

Versión V6 construida sobre el modelo QA 726 de la versión anterior.

## Incluye
- Rediseño completo del dashboard con identidad institucional azul/rojo/blanco.
- KPIs: 154 proyectos válidos, 726 participaciones estudiantiles, 77 docentes, 36 asignaturas, 26 cohortes y promedio 4.08.
- Filtros globales por periodo, programa, semestre, sección, grupo, docente y asignatura.
- Módulo de proyectos y exportación CSV.
- Proyectos destacados por semestre y Top 5 según el criterio cuantitativo de mayor nota final.
- Módulo Líderes de Colectivo, distinguiendo asignaciones de líderes y docentes únicos.
- Estudiantes, docentes, evaluación, historial y auditoría.
- **Chat IA · Analista**, integrado al dashboard y conectado al modelo local.
- Diseño responsive y estados de interacción.

## Chat IA
El asistente V6 funciona localmente sobre el modelo cargado y no requiere una clave de API externa. Puede responder consultas sobre:
- cantidades de proyectos, estudiantes y docentes;
- promedio y notas;
- Top 5 y proyectos destacados;
- distribución por semestre;
- líderes de colectivo;
- reglas de cálculo y auditoría.

Ejemplos:
- ¿Cuántos proyectos hay?
- ¿Cuántos estudiantes participan en SEM-03?
- ¿Cuál es el promedio final?
- Muéstrame el top 5.
- ¿Qué proyectos están destacados?
- ¿Cómo se calcula la nota final?

## Ejecución local
```bash
pip install -r requirements.txt
python run_local.py
```

## Render
Start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Nota
La V6 conserva la fuente local Excel/model.json de esta entrega. La integración automática con OneDrive/SharePoint queda preparada como siguiente etapa mediante Microsoft Graph.
