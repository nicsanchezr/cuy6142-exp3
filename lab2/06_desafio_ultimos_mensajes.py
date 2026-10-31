"""
06_desafio_ultimos_mensajes.py
Desafío (opcional): leer los últimos mensajes de la sala.
  - GET /messages  -> roomId + max
"""
from webex_utils import cargar_token, llamar_api, leer_sala

token = cargar_token()
room_id = leer_sala()

mensajes = llamar_api("GET", "messages", token,
                      params={"roomId": room_id, "max": 5}).json()["items"]

print("Últimos {} mensajes (del más nuevo al más antiguo):".format(len(mensajes)))
for m in mensajes:
    adjuntos = " [+{} adjunto(s)]".format(len(m["files"])) if m.get("files") else ""
    print("  {}  {}: {}{}".format(m["created"][:16].replace("T", " "),
                                  m["personEmail"], m.get("text", ""), adjuntos))
