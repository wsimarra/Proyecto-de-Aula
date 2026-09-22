# Proyectos de Aula — V6.2 Producción + Chat IA

## Publicación
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variable opcional para IA generativa: `OPENAI_API_KEY`
- Variable opcional de modelo: `OPENAI_MODEL` (por defecto `gpt-5`)

La clave de IA debe configurarse únicamente como variable secreta del servidor; nunca en `static/index.html`. Si no existe `OPENAI_API_KEY`, el chat funciona con el asistente local determinista.

## Endpoints de comprobación
- `/api/ai/status` indica si la IA generativa está configurada, sin revelar secretos.
- `/api/dashboard` recarga el modelo actual.
- `/api/ai/chat` recibe las preguntas del chat.

## Producción
Para datos académicos institucionales se recomienda añadir autenticación/autorización antes de abrir el servicio al público.
