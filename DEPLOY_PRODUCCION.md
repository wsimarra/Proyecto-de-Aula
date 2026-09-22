# Publicación en Render
1. GitHub: subir el proyecto a la rama `main`.
2. Render → New → Web Service → seleccionar repositorio.
3. Build Command: `pip install -r requirements.txt`.
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Environment Variables: `OPENAI_API_KEY` y opcional `OPENAI_MODEL=gpt-5`.
6. Deploy.
7. Abrir `/api/ai/status` y comprobar `configured: true`.
8. Probar el dashboard y el Chat IA.

No compartas la clave por chat. Render permite guardar variables como secretos.
