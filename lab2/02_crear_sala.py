"""
02_crear_sala.py
Paso 2: crear una sala (espacio) cuyo título es tu nombre_apellido.
  - GET  /rooms  -> revisa si la sala ya existe (para no duplicarla)
  - POST /rooms  -> la crea si no existe
El ID de la sala queda guardado en sala_id.txt para los pasos siguientes.
"""
from webex_utils import cargar_token, cargar_variable, llamar_api, guardar_sala

token = cargar_token()
titulo = cargar_variable("MI_NOMBRE")          # ejemplo: maria_gonzalez

# 1) ¿Ya tengo una sala con ese título?
salas = llamar_api("GET", "rooms", token,
                   params={"type": "group", "max": 100}).json()["items"]
existente = [sala for sala in salas if sala["title"] == titulo]

if existente:
    sala = existente[0]
    print("[OK] La sala '{}' ya existía; se reutiliza.".format(titulo))
else:
    # 2) Crear la sala. El cuerpo de la solicitud va como JSON.
    respuesta = llamar_api("POST", "rooms", token, json={"title": titulo})
    sala = respuesta.json()
    print("[OK] Sala creada (HTTP {})".format(respuesta.status_code))

print("     Título : {}".format(sala["title"]))
print("     ID     : {}...".format(sala["id"][:25]))

guardar_sala(sala["id"])
print("     El ID completo quedó guardado en sala_id.txt")
