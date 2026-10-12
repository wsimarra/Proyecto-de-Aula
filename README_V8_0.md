# Proyecto de Aula V8.0 — BI Institucional

Versión construida sobre V7.0 con los bloques solicitados:

### 🔴 Bloque 1 — Datos
- Conserva los **154 proyectos válidos** del modelo.
- Conserva los **58 títulos genéricos positivos** que vienen de la fuente.
- Los títulos genéricos no se reemplazan ni se inventan: se identifican como `GENÉRICO DE FUENTE` y se presentan en MAYÚSCULAS.
- Se mantiene la exclusión del registro `G07 / Proyecto 7` con nota 0 por falta de evidencia suficiente.
- KPI de participaciones: **726**.
- Estudiantes únicos dentro de proyectos válidos: **725**.

### 🟠 Bloque 3 — BI
- KPI de asignaturas dinámico según filtros.
- Separación explícita entre secciones y cohortes.
- Promedio simple de proyectos: **4.08**.
- Promedio ponderado por estudiantes: **4.11**.
- Gráficas sin mezclar proyectos y participaciones en una misma escala.
- Historial separado para promedio y participación.
- Distribución de notas por bandas 0–2.99, 3.00–3.49, 3.50–3.99, 4.00–4.49 y 4.50–5.00.

### 🟠 Bloque 4 — UX/UI
- Rediseño institucional azul, rojo y blanco.
- Menos gradientes decorativos y mayor jerarquía visual.
- Tipografía, etiquetas y tablas más legibles.
- Títulos completos en MAYÚSCULAS y sin truncamiento por puntos suspensivos.
- Tarjetas y detalle con Grupo, Semestre, Sección, Proyecto y Nota.
- Indicador visible cuando un título es genérico de fuente.
- Responsive para escritorio, tablet y móvil.

## QA ejecutado
Se ejecutan tres pruebas automatizadas de modelo con `unittest`:

1. Conteos y 58 títulos genéricos de fuente.
2. KPIs institucionales y promedios.
3. Comportamiento dinámico del filtro de asignatura.

Resultado: **3/3 pruebas OK**.

## Arranque local
```bash
pip install -r requirements.txt
python run_local.py
```

O en Windows:
```bat
run_windows.bat
```

## Nota de producción
La integración real con OneDrive/SharePoint y la autenticación institucional siguen siendo una etapa posterior. No se incluyen credenciales ni secretos en este paquete.
