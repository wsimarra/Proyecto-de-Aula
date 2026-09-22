# Proyectos de Aula V6.4 — Bootstrap BI Institucional

V6.4 es una evolución visual de V6.3. Mantiene el backend, el modelo de datos, las reglas de cálculo, los filtros, las APIs y el Chat IA Libre; el cambio principal es la capa UX/UI.

## Cambios
- Bootstrap 5.3 como capa de layout y componentes.
- Bootstrap Icons para navegación y acciones.
- Sidebar institucional con navegación más clara y estado activo.
- Barra móvil responsive con acceso al menú y Chat IA.
- Filtros con iconografía y mejor jerarquía visual.
- KPI con acentos institucionales y mejor lectura.
- Tablas, tarjetas, auditoría y Chat IA con una capa visual coherente.
- Se conserva la lógica de V6.3: 154 proyectos válidos, 726 participaciones estudiantiles, 77 docentes, 36 asignaturas, 26 cohortes y promedio final 4.08.
- No se cambia la definición de proyecto destacado ni las reglas académicas.

## Dependencias
Bootstrap 5.3.3 y Bootstrap Icons 1.11.3 se cargan desde CDN en `static/index.html`. El CSS institucional propio permanece como capa de personalización y fallback.

## Ejecución
```bash
pip install -r requirements.txt
python run_local.py
```

## Publicación
Se conserva el mismo Build y Start de las versiones anteriores:
`pip install -r requirements.txt`
`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

V6.4 Bootstrap BI
