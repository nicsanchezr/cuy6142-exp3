"""
00_verificar_entorno.py
Revisa que el entorno de trabajo tenga todo lo necesario para los laboratorios:
Python 3.8 o superior, las librerías requests y python-dotenv, Git,
y conexión con la API de Webex.
"""
import shutil
import sys

print("Revisando el entorno de trabajo...\n")
todo_ok = True

# 1) Versión de Python
version = sys.version_info
if version >= (3, 8):
    print(f"[OK]    Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"[FALTA] Python {version.major}.{version.minor}: se necesita 3.8 o más")
    todo_ok = False

# 2) Librerías
for libreria in ["requests", "dotenv"]:
    try:
        __import__(libreria)
        print(f"[OK]    Librería {libreria}")
    except ImportError:
        print(f"[FALTA] Librería {libreria}: python3 -m pip install --user -r requirements.txt")
        todo_ok = False

# 3) Git
if shutil.which("git"):
    print("[OK]    Git instalado")
else:
    print("[FALTA] Git no está instalado (en Colab no es necesario)")

# 4) Conexión con la API de Webex.
#    Sin token, Webex responde 401: eso confirma que la red llega hasta la API.
try:
    import requests
    respuesta = requests.get("https://webexapis.com/v1/people/me", timeout=10)
    if respuesta.status_code == 401:
        # 401 = "falta el token": la red llega bien hasta Webex
        print("[OK]    Conexión con webexapis.com (401 sin token: esperado)")
    else:
        print(f"[AVISO] webexapis.com respondió HTTP {respuesta.status_code}")
except Exception as error:
    print(f"[FALTA] Sin conexión con webexapis.com: {error}")
    todo_ok = False

print()
if todo_ok:
    print("Entorno listo.")
else:
    print("Corrige lo que aparece como [FALTA] y vuelve a ejecutar.")
