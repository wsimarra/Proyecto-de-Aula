import socket, subprocess, sys, time, webbrowser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=socket.socket(); s.bind(("127.0.0.1",0)); port=s.getsockname()[1]; s.close()
url=f"http://127.0.0.1:{port}"
p=subprocess.Popen([sys.executable,"-m","uvicorn","app.main:app","--host","127.0.0.1","--port",str(port)],cwd=ROOT)
try:
    deadline=time.time()+30
    ready=False
    while time.time()<deadline and p.poll() is None:
        try:
            with socket.create_connection(("127.0.0.1",port),timeout=0.5):
                ready=True
                break
        except OSError:
            time.sleep(0.25)
    if ready:
        print(f"Proyecto Aula V9.1 disponible en: {url}", flush=True)
        webbrowser.open(url)
    else:
        print("El servidor no respondió en 30 segundos. Revisa el error mostrado arriba.", flush=True)
    p.wait()
except KeyboardInterrupt:
    p.terminate()
