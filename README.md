# Proyecto Aula V9.0 — BI Institucional

Versión de mejora sobre V8.0. Consulte `README_V9_0.md` y `QA_REPORT_V9_0.md` para los cambios de notas de estudiantes, exportación Excel y estado de calificación docente.

## Inicio en Windows
Ejecute `run_windows.bat`. Se crea/usa el entorno virtual, instala dependencias y abre el dashboard en el navegador.

## Inicio manual
```powershell
python -m pip install -r requirements.txt
python run_local.py
```

## Notas sobre las fuentes
La definitiva mostrada en Estudiantes es la nota grupal del proyecto. Los seguimientos 2 y 3 no están en la fuente actual y se muestran como N/D hasta que se agreguen sus registros originales. El estado docente se deriva de notas TERCERO disponibles y no identifica al usuario que digitó la nota.
