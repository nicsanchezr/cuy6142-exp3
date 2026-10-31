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
    r.raise_for_status()
    return r.json()["items"]                       # el primero es el más reciente


def decidir(texto):
    """DECIDIR: elige la respuesta según el texto recibido."""
    texto = texto.strip().lower()
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
yo.raise_for_status()
correo_bot = yo.json()["emails"][0]

# Los mensajes que ya estaban en la conversación no se responden
vistos = {m["id"] for m in leer_mensajes()}
print("Bot manual iniciado como", correo_bot, "- conversa con", PERSONA)
print("Escríbele desde Webex. Para detenerlo: Ctrl+C")

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
