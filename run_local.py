import socket,subprocess,sys,time,webbrowser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=socket.socket();s.bind(("127.0.0.1",0));port=s.getsockname()[1];s.close()
url=f"http://127.0.0.1:{port}"
p=subprocess.Popen([sys.executable,"-m","uvicorn","app.main:app","--host","127.0.0.1","--port",str(port)],cwd=ROOT)
time.sleep(1.2);webbrowser.open(url)
try:p.wait()
except KeyboardInterrupt:p.terminate()
