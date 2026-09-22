# V6.3 Chat IA Libre

Build: `pip install -r requirements.txt`
Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Variables en el servidor:
- `OPENAI_API_KEY` (secreta; nunca en HTML/JS/GitHub)
- `OPENAI_MODEL` opcional, por defecto `gpt-5`

Comprobar `/api/ai/status`. `configured:true` significa que la IA generativa está lista. Sin clave, el chat conserva un modo local determinista.

Para datos académicos institucionales, añadir autenticación/autorización antes de exponer la aplicación al público.
