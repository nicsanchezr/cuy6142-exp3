"""
03_agregar_companero.py
Paso 3: agregar a tu compañero(a) a la sala y listar los miembros.
  - POST /memberships  -> crea la membresía (roomId + personEmail)
  - GET  /memberships  -> lista quiénes están en la sala
"""
from webex_utils import cargar_token, cargar_variable, llamar_api, leer_sala

token = cargar_token()
room_id = leer_sala()
email_companero = cargar_variable("EMAIL_COMPANERO")

# 1) Crear la membresía. Si ya era miembro, Webex responde 409 (lo manejamos aquí).
cuerpo = {"roomId": room_id, "personEmail": email_companero}
respuesta = llamar_api("POST", "memberships", token, permitir=(409,), json=cuerpo)

if respuesta.status_code == 409:
    print("[OK] {} ya era miembro de la sala.".format(email_companero))
else:
    print("[OK] {} agregado(a) a la sala (HTTP {})".format(
        email_companero, respuesta.status_code))

# 2) Listar los miembros de la sala.
miembros = llamar_api("GET", "memberships", token,
                      params={"roomId": room_id}).json()["items"]

print("\nMiembros de la sala ({}):".format(len(miembros)))
for miembro in miembros:
    rol = "moderador" if miembro.get("isModerator") else "miembro"
    print("  - {:<25} {:<35} {}".format(
        miembro.get("personDisplayName", ""), miembro["personEmail"], rol))
