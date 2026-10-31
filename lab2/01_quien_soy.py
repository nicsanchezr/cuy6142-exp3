"""
01_quien_soy.py
Paso 1: comprobar que el token funciona.
Llama a GET /people/me, que devuelve los datos de la persona dueña del token.
"""
from webex_utils import cargar_token, llamar_api

token = cargar_token()

respuesta = llamar_api("GET", "people/me", token)
yo = respuesta.json()

print("[OK] Token válido (HTTP {})".format(respuesta.status_code))
print("     Nombre : {}".format(yo["displayName"]))
print("     Correo : {}".format(yo["emails"][0]))
print("     ID     : {}...".format(yo["id"][:25]))
