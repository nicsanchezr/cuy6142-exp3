"""
webex_utils.py
Funciones de apoyo para los laboratorios de la Experiencia 3 (CUY6142).

Este archivo NO se ejecuta solo: lo importan los demás scripts.
Se encarga de tres cosas que se repiten en todas las llamadas:
  1. Leer el token desde el archivo .env (nunca escrito en el código).
  2. Armar la URL y el encabezado Authorization: Bearer <token>.
  3. Revisar el código de respuesta HTTP y explicar el error si algo falla.

Compatible con Python 3.8 o superior (VM DEVASC) y con Google Colab.
"""

import os
import sys
import time

import requests

# Dirección base de la API REST de Webex.
# (La variable WEBEX_API_URL solo se usa para pruebas; no la necesitas.)
API_BASE = os.getenv("WEBEX_API_URL", "https://webexapis.com/v1")

# Archivo donde guardamos el ID de la sala para no copiarlo a mano.
ARCHIVO_SALA = "sala_id.txt"

# Explicación en español de los errores más comunes.
EXPLICACION_ERRORES = {
    400: "Solicitud mal formada: revisa los datos enviados (roomId, email, JSON).",
    401: "Token inválido o expirado: copia un token nuevo en el archivo .env.",
    403: "Sin permiso: tu cuenta no puede hacer esta acción en ese recurso.",
    404: "No encontrado: el ID no existe o tú no eres miembro de esa sala.",
    405: "Método no permitido: revisa si corresponde GET, POST, PUT o DELETE.",
    409: "Conflicto: el recurso ya existe (por ejemplo, la persona ya es miembro).",
    429: "Demasiadas solicitudes: Webex pide esperar antes de reintentar.",
}


def cargar_variable(nombre, obligatoria=True):
    """Lee una variable del archivo .env (o del entorno) y la devuelve limpia."""
    try:
        from dotenv import load_dotenv  # paquete python-dotenv
        load_dotenv()
        hay_dotenv = True
    except ImportError:
        hay_dotenv = False  # en Colab las variables llegan desde los Secrets

    valor = os.getenv(nombre, "").strip().strip('"').strip("'")
    if obligatoria and not valor:
        print("[ERROR] Falta la variable {} en el archivo .env".format(nombre))
        if hay_dotenv:
            print("        Revisa que .env esté en la misma carpeta que el script.")
        else:
            print("        Instala python-dotenv:")
            print("        python3 -m pip install --user python-dotenv")
        sys.exit(1)
    return valor


def cargar_token():
    """Devuelve el token sin la palabra 'Bearer' (por si se copió con ella)."""
    token = cargar_variable("WEBEX_TOKEN")
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token


def llamar_api(metodo, recurso, token, permitir=(), **kwargs):
    """
    Hace una llamada a la API de Webex y revisa la respuesta.

    metodo   : "GET", "POST", "PUT" o "DELETE"
    recurso  : por ejemplo "rooms", "memberships" o "people/me"
    token    : el token de acceso
    permitir : códigos de error que el script quiere manejar por su cuenta (ej. 409)
    kwargs   : params=..., json=..., data=..., files=... (igual que en requests)
    """
    url = "{}/{}".format(API_BASE, recurso)
    encabezados = {"Authorization": "Bearer {}".format(token)}

    for intento in range(1, 4):
        try:
            respuesta = requests.request(metodo, url, headers=encabezados,
                                         timeout=20, **kwargs)
        except requests.exceptions.RequestException as error:
            print("[ERROR] No hubo conexión con Webex: {}".format(error))
            print("        Revisa tu conexión a Internet o el proxy de la red.")
            sys.exit(1)

        # 429: Webex indica en Retry-After cuántos segundos esperar.
        if respuesta.status_code == 429 and intento < 3:
            espera = int(respuesta.headers.get("Retry-After", "5"))
            print("[AVISO] HTTP 429: reintentando en {} s...".format(espera))
            time.sleep(espera)
            continue
        break

    if respuesta.ok or respuesta.status_code in permitir:
        return respuesta

    mostrar_error(respuesta)
    sys.exit(1)


def mostrar_error(respuesta):
    """Imprime el código HTTP, su explicación y el mensaje que devolvió Webex."""
    codigo = respuesta.status_code
    print("[ERROR] HTTP {}: {}".format(
        codigo, EXPLICACION_ERRORES.get(codigo, "Error no previsto.")))
    try:
        detalle = respuesta.json()
        print("        Mensaje de Webex: {}".format(detalle.get("message", detalle)))
        if detalle.get("trackingId"):
            print("        trackingId: {}".format(detalle["trackingId"]))
    except ValueError:
        print("        Respuesta: {}".format(respuesta.text[:200]))


def guardar_sala(room_id):
    """Guarda el ID de la sala en sala_id.txt para usarlo en los pasos siguientes."""
    with open(ARCHIVO_SALA, "w") as archivo:
        archivo.write(room_id)


def leer_sala():
    """Lee el ID de la sala guardado por 02_crear_sala.py."""
    if not os.path.exists(ARCHIVO_SALA):
        print("[ERROR] No existe {}.".format(ARCHIVO_SALA))
        print("        Ejecuta primero 02_crear_sala.py")
        sys.exit(1)
    with open(ARCHIVO_SALA) as archivo:
        return archivo.read().strip()
