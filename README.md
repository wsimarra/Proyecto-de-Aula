# Proyectos de Aula — V5.2 Líderes de Colectivo

Versión local del dashboard de Gestión y Seguimiento de Proyectos de Aula.

## Ejecutar en Windows
Doble clic en `run_windows.bat` o ejecutar `python run_local.py`.

## Datos
- 26 archivos Excel únicos.
- 154 Proyectos de Aula válidos.
- 752 estudiantes únicos.
- 4461 relaciones de matrícula después de deduplicar registros exactos.
- 4369 notas de tercer corte después de deduplicar registros exactos.
- 77 docentes.
- 36 asignaturas.
- 26 asignaciones de Líder de Colectivo por sección.
- 18 docentes únicos con rol de Líder de Colectivo.

## Nueva funcionalidad V5.2
Se agregó el módulo **Líderes de Colectivo**. El dato se extrae de la hoja `LIDER` de cada archivo y se relaciona con semestre y sección. Un docente puede liderar varias secciones y esas asignaciones se conservan.

Filtros del módulo:
- Periodo
- Semestre
- Sección
- Líder de Colectivo
- Asignatura (Líder)

La pantalla muestra la tabla por sección, proyectos y estudiantes asociados, además del detalle del docente seleccionado.

## Regla de proyectos
Los proyectos válidos se calculan mediante la lógica corregida: se excluyen grupos 0 y registros sin proyecto documentado según las reglas aplicadas en la auditoría. Resultado actual: 154.

## Siguiente fase
La fuente puede migrarse posteriormente a OneDrive/SharePoint mediante Microsoft Graph sin rehacer el modelo ni la interfaz.


### V5.2 — Corrección de estudiantes
- La tarjeta principal usa **726 estudiantes en proyectos** (participaciones en los 154 proyectos válidos).
- Se conserva 752 como estudiantes únicos registrados en toda la fuente para trazabilidad, y 725 como personas únicas dentro de proyectos válidos.
- Los módulos de Líderes, Programas, Estudiantes y Auditoría usan la misma definición de 726 para mantener consistencia.
