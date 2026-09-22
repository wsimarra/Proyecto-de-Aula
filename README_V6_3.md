# Proyectos de Aula — V6.3 Chat IA Libre

## Objetivo
V6.3 conserva el dashboard BI de V6.2 y amplía el Chat IA para aceptar **preguntas libres** sobre el modelo institucional cargado, sin depender de una lista cerrada de preguntas.

## Chat IA Libre
El asistente puede:
- Buscar proyectos por título, grupo, semestre y sección.
- Consultar estudiantes asociados a un proyecto.
- Consultar docentes y asignaturas asociadas a las cohortes.
- Consultar Líderes de Colectivo.
- Consultar notas finales y promedios.
- Comparar semestres, secciones o grupos.
- Calcular diferencias, porcentajes y agregaciones con los datos entregados.
- Explicar reglas del modelo y observaciones de auditoría.
- Mantener el contexto de los filtros seleccionados en el dashboard.
- Conservar los títulos de proyectos completos y en MAYÚSCULAS.
- Indicar cuando un dato solicitado no está disponible, sin inventarlo.

La IA generativa recibe un contexto estructurado de los proyectos válidos, integrantes, asignaciones, líderes, KPIs y resúmenes por semestre. El backend no expone la clave de OpenAI al navegador.

## Datos base
La versión mantiene los indicadores validados:
- 154 proyectos válidos.
- 726 participaciones estudiantiles en proyectos.
- 725 personas únicas dentro de proyectos válidos.
- 752 estudiantes únicos registrados en toda la fuente.
- 77 docentes.
- 36 asignaturas.
- 26 cohortes.
- Promedio final general 4.08.

## Ejecución local
```bash
pip install -r requirements.txt
python run_local.py
```

## IA generativa
Configurar únicamente en el entorno del servidor:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` opcional; por defecto `gpt-5`

El endpoint `/api/ai/status` indica si la IA generativa está configurada.

## Render
Build:
```bash
pip install -r requirements.txt
```

Start:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Seguridad
No guardar `OPENAI_API_KEY` en HTML, JavaScript ni GitHub. Para datos académicos institucionales se recomienda incorporar autenticación/autorización antes de uso público.
