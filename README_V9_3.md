# Proyecto de Aula V9.3 — Ajustes visuales

## Base
Construida sobre el paquete recibido `Proyecto_Aula_V9_2_SEGUIMIENTO_DOCENTES(1).zip`.

## Cambios incluidos
- Etiqueta del gráfico del resumen: “Número de estudiantes por semestre”.
- Etiquetas del gráfico y tooltip ajustadas para “Número de estudiantes”.
- Etiquetas de evaluación: “Proyectos con calificación”, “Promedio de calificación final” y “Proyectos sin calificación”.
- Títulos de evaluación: “Promedio de calificación por semestre” y “Distribución de calificaciones por rango”.
- Nuevo gráfico de dona “Proyectos por semestre”, alimentado por `d.by_semester` y la métrica `projects` del modelo.
- Textos de filtros, descripción y encabezados de tabla de Líderes de colectivo actualizados.

## Conservación
- No se modificó `app/main.py`, las reglas académicas ni los cálculos del backend.
- No se modificó la configuración de despliegue.
- El nuevo gráfico usa datos del modelo; no incluye cifras ficticias.

## Validación
La interfaz y el archivo JavaScript se deben probar en entorno local antes de desplegar. Confirmar especialmente que `by_semester.students` representa estudiantes únicos; si representa participaciones, debe cambiarse la etiqueta para reflejar el dato correctamente.
