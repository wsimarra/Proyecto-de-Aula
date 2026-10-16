# V10.0 — Integración de datos 2026-1 y 2026-2

## Cambios
- Se conserva el modelo base de 2026-1.
- Se incorporan los Excel del periodo 2026-2 desde los dos ZIP recibidos.
- Los archivos nuevos se almacenan con prefijo `2026-2__` para evitar sobrescribir archivos homónimos de 2026-1.
- El cargador de notas de corte ahora resuelve cada Excel por el vínculo explícito archivo-cohorte, separando periodos y admitiendo varios programas.
- Se mantiene la interfaz y las rutas API existentes; el selector de periodo puede consultar ambos periodos.

## Recuento tras integración
- **2026-1:** 26 cohortes/secciones, 162 grupos de proyecto detectados.
- **2026-2:** 31 cohortes/secciones, 166 grupos de proyecto detectados.

## Validación pendiente
- Probar los endpoints y la navegación completa en entorno local antes de considerar la versión lista para producción.
- Las cifras de 2026-2 se derivan de los campos disponibles en los Excel; los títulos se toman de la hoja de asignatura cuando están registrados; los grupos de 2026-2 sin nota de tercer corte se conservan como proyectos sin calificación, no como nota cero.
- Las diferencias entre sección del nombre de archivo y sección dentro de la hoja se conservan como incidencias de calidad; no se corrigen silenciosamente.
