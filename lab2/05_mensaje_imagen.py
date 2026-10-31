"""
05_mensaje_imagen.py
Paso 5: publicar un mensaje con una imagen adjunta.
  - POST /messages  -> se envía como multipart/form-data (texto + archivo)

Uso:  python3 05_mensaje_imagen.py                 (usa imagen_prueba.png)
      python3 05_mensaje_imagen.py otra_imagen.jpg
"""
import mimetypes
import os
import sys

from webex_utils import cargar_token, cargar_variable, llamar_api, leer_sala

token = cargar_token()
room_id = leer_sala()
nombre = cargar_variable("NOMBRE_COMPLETO")

ruta = sys.argv[1] if len(sys.argv) > 1 else "imagen_prueba.png"
if not os.path.exists(ruta):
    print("[ERROR] No encuentro el archivo {}".format(ruta))
    sys.exit(1)

tipo = mimetypes.guess_type(ruta)[0] or "application/octet-stream"
texto = "Saludos Webex, mi nombre es {}. Adjunto una imagen.".format(nombre)

# Con un archivo NO se usa json=: los campos van en data= y el archivo en files=.
# requests arma solo el encabezado Content-Type: multipart/form-data.
with open(ruta, "rb") as imagen:
    respuesta = llamar_api(
        "POST", "messages", token,
        data={"roomId": room_id, "text": texto},
        files={"files": (os.path.basename(ruta), imagen, tipo)},
    )

datos = respuesta.json()
print("[OK] Mensaje con imagen publicado (HTTP {})".format(respuesta.status_code))
print("     Archivo : {} ({} KB)".format(ruta, os.path.getsize(ruta) // 1024))
print("     Adjuntos: {}".format(len(datos.get("files", []))))
