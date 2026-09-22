# Proyectos de Aula V7.0 FINAL — BI Institucional Inteligente

Esta edición consolida las correcciones de la V7.0 en una sola versión estable para pruebas locales antes de producción.

## Correcciones y mejoras incluidas

### Gestión documental
- Botón visible para adjuntar PDF desde el detalle de cada proyecto.
- Reemplazo de PDF.
- Eliminación de PDF con confirmación.
- Validación de extensión, firma PDF y límite de 20 MB.
- Inventario documental con filtros de búsqueda y estado.
- Indicador de PDF disponible/pendiente en el explorador y destacados.
- Metadatos básicos del archivo: nombre, tamaño y fecha de actualización.

### Explorador BI
- Búsqueda por proyecto, grupo, semestre y sección.
- Ordenamiento por nombre, nota, estudiantes y semestre.
- Exportación CSV y Excel.
- Títulos completos en MAYÚSCULAS.
- Estado documental visible por proyecto.

### Control institucional
- Nuevo módulo Documentos.
- Nuevo módulo Estado del sistema.
- Estado real de IA: generativa o modo local.
- Estado del modelo, fuente, documentos y versión.
- Conteo de documentos disponibles y pendientes.
- Fecha de actualización del estado.

### Conservación del modelo académico
- 154 proyectos válidos.
- 726 participaciones estudiantiles.
- 77 docentes.
- 36 asignaturas.
- 26 cohortes.
- Promedio final 4.08.
- 154 proyectos con nota.
- Criterio de destacado: mayor promedio final grupal por semestre; los empates se conservan.

### Arquitectura
- Se conserva FastAPI + modelo JSON + frontend Bootstrap 5.3.
- La carga documental queda separada del modelo académico.
- Preparado para futura migración de fuente a Microsoft Graph / SharePoint.
- La versión no publica ni expone claves de OpenAI.

## Prueba local

Windows:

```bat
py -m pip install -r requirements.txt
py run_local.py
```

Abrir el navegador en la dirección mostrada por el lanzador.

## Flujo recomendado para PDF

1. Ir a **Destacados** o **Proyectos**.
2. Abrir **Detalle**.
3. Seleccionar el PDF.
4. Pulsar **Subir PDF**.
5. Verificar **PDF disponible**.
6. Probar **Ver PDF**, **Reemplazar** y **Eliminar**.

## Producción

No publicar esta edición hasta terminar la prueba local. Para Render se mantienen los comandos de producción documentados en `DEPLOY_PRODUCCION.md`.
