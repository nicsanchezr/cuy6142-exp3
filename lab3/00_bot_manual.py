"""
00_bot_manual.py
Un bot "hecho a mano": cada 5 segundos le pregunta a la API de Webex si
llegó un mensaje nuevo, decide qué responder y responde con POST /messages.
Es el ciclo recibir -> decidir -> responder, sin librerías de bots.

Funciona con el Python de la VM DEVASC: solo necesita requests.
Para detenerlo: Ctrl+C.
"""
import time
from datetime import datetime

import requests

from utilidades import cargar_lista, cargar_token_bot

API = "https://webexapis.com/v1"
ENCABEZADOS = {"Authorization": "Bearer " + cargar_token_bot()}
PERSONA = cargar_lista("USUARIOS_PERMITIDOS")[0]  # el primer correo: con quién conversa
ESPERA = 5                                         # segundos entre consultas


def leer_mensajes():
    """RECIBIR: pide los mensajes de la conversación 1 a 1 con PERSONA."""
    r = requests.get(API + "/messages/direct", headers=ENCABEZADOS,
                     params={"personEmail": PERSONA}, timeout=10)
    if r.status_code == 429:                       # demasiadas consultas
        espera = int(r.headers.get("Retry-After", 10))
        print("[429] Demasiadas consultas: espero", espera, "segundos")
        time.sleep(espera)
        return []
    if r.status_code != 200:
        explicar_error(r)
    return r.json()["items"]                       # el primero es el más reciente


def explicar_error(r):
    """Muestra qué significa el error de la API y detiene el script."""
    causas = {
        401: "El token no es válido: revisa WEBEX_BOT_TOKEN en el .env (sin espacios ni comillas).",
        403: "Todavía no hay conversación entre el bot y ese correo: escríbele \"hola\" al bot desde la app "
             "Webex y vuelve a ejecutar. Si ya le escribiste, revisa que el primer correo de USUARIOS_PERMITIDOS "
             "sea exactamente el de tu cuenta Webex.",
        404: "No hay conversación entre el bot y ese correo: escríbele primero al bot desde la app Webex "
             "y revisa que el primer correo de USUARIOS_PERMITIDOS sea el tuyo.",
    }
    try:
        detalle = r.json().get("message", "")
    except ValueError:
        detalle = r.text[:200]
    print("[ERROR] HTTP {}: {}".format(r.status_code, detalle))
    print("        " + causas.get(r.status_code, "Revisa el token y el correo del .env."))
    raise SystemExit(1)


def decidir(texto):
    """DECIDIR: elige la respuesta según el texto recibido."""
    texto = texto.strip().lower().strip("¡!¿?.,")       # sin puntuación: "Hola!" = "hola"
    if texto == "hola":
        return "¡Hola! Soy un bot hecho a mano 🤖"
    if texto == "hora":
        return "Son las " + datetime.now().strftime("%H:%M")
    return "No entiendo «{}». Prueba con: hola, hora".format(texto)


def responder(texto):
    """RESPONDER: publica la respuesta en la misma conversación."""
    cuerpo = {"toPersonEmail": PERSONA, "text": texto}
    r = requests.post(API + "/messages", headers=ENCABEZADOS, json=cuerpo, timeout=10)
    r.raise_for_status()


# ¿Quién soy? Sirve para no responder a los mensajes del propio bot
yo = requests.get(API + "/people/me", headers=ENCABEZADOS, timeout=10)
if yo.status_code != 200:
    explicar_error(yo)
if yo.json().get("type") != "bot":
    print("[ERROR] El token de WEBEX_BOT_TOKEN es de una persona ({}), no de un bot.".format(yo.json()["emails"][0]))
    print("        Copia en el .env el token de tu bot (Paso 1.2 de la guía).")
    raise SystemExit(1)
correo_bot = yo.json()["emails"][0]

# Los mensajes que ya estaban en la conversación no se responden
vistos = {m["id"] for m in leer_mensajes()}
print("Bot manual iniciado como", correo_bot, "- conversa con", PERSONA)
print("Escríbele desde Webex. Para detenerlo: Ctrl+C")

try:
    while True:
        time.sleep(ESPERA)
        for m in reversed(leer_mensajes()):            # del más antiguo al más nuevo
            if m["id"] in vistos:
                continue
            vistos.add(m["id"])
            if m["personEmail"] == correo_bot:         # lo escribió el propio bot
                continue
            texto = m.get("text", "")
            print("[RECIBIDO]", m["personEmail"], "->", texto)
            respuesta = decidir(texto)
            responder(respuesta)
            print("[ENVIADO] ", respuesta)
except KeyboardInterrupt:                      # Ctrl+C: se detiene sin mostrar el error
    print("\nBot detenido.")
