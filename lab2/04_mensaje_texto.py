"""
04_mensaje_texto.py
Paso 4: publicar un mensaje con formato Markdown y un emoji en la sala.
  - POST /messages  -> roomId + markdown
"""
from webex_utils import cargar_token, cargar_variable, llamar_api, leer_sala

token = cargar_token()
room_id = leer_sala()
nombre = cargar_variable("NOMBRE_COMPLETO")    # ejemplo: María González

# \U0001F44B es el emoji de la mano saludando (así no hay que escribirlo en nano).
emoji = "\U0001F44B"
mensaje = "Saludos Webex, mi nombre es **{}** {}".format(nombre, emoji)

respuesta = llamar_api("POST", "messages", token,
                       json={"roomId": room_id, "markdown": mensaje})
datos = respuesta.json()

print("[OK] Mensaje publicado (HTTP {})".format(respuesta.status_code))
print("     Texto  : {}".format(datos["text"]))
print("     Fecha  : {}".format(datos["created"]))
