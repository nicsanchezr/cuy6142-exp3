"""
comandos.py
Los comandos que entiende el bot. Cada comando es una clase con:
  - command_keyword : la palabra que lo activa
  - help_message    : el texto que aparece en el menú de ayuda
  - execute()       : lo que hace el bot y lo que responde
"""
import requests
from webexpythonsdk.models.cards import (AdaptiveCard, Choice, ChoiceSet,
                                         FontSize, FontWeight, TextBlock)
from webexpythonsdk.models.cards.actions import Submit
from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card

from utilidades import cargar_token_bot

API = "https://webexapis.com/v1"


def quien_escribe(activity):
    """Devuelve (nombre, correo) de la persona que le habló al bot."""
    actor = activity["actor"]
    return actor.get("displayName", actor["emailAddress"]), actor["emailAddress"]


# ---------------------------------------------------------------------
class Hola(Command):
    """Responde 'hola' saludando por el nombre."""

    def __init__(self):
        super().__init__(command_keyword="hola",
                         exact_command_keyword_match=True,  # solo "hola"
                         help_message="Saludar")

    def execute(self, message, attachment_actions, activity):
        nombre, _ = quien_escribe(activity)
        return (f"Hola **{nombre}** \U0001F44B Soy un bot de CUY6142. "
                "Escribe **help** para ver lo que sé hacer.")


# ---------------------------------------------------------------------
class CrearSala(Command):
    """'crear sala <nombre>': crea una sala y agrega a quien lo pidió."""

    def __init__(self):
        super().__init__(command_keyword="crear sala",
                         help_message="Crear una sala (crear sala <nombre>)")

    def execute(self, message, attachment_actions, activity):
        titulo = message.strip()   # el texto que viene después de "crear sala"
        if not titulo:
            return "Dime el nombre de la sala. Ejemplo: **crear sala proyecto_redes**"

        _, correo = quien_escribe(activity)
        encabezados = {"Authorization": f"Bearer {cargar_token_bot()}"}

        # 1) El bot crea la sala (queda como miembro)
        r = requests.post(API + "/rooms", headers=encabezados,
                          json={"title": titulo}, timeout=20)
        if r.status_code != 200:
            return f"No pude crear la sala (HTTP {r.status_code})."
        sala = r.json()

        # 2) El bot agrega a la persona que le escribió
        cuerpo = {"roomId": sala["id"], "personEmail": correo}
        r = requests.post(API + "/memberships", headers=encabezados,
                          json=cuerpo, timeout=20)
        if r.status_code not in (200, 409):
            return f"Creé la sala, pero no pude agregarte (HTTP {r.status_code})."

        return f"Listo: creé la sala **{titulo}** y te agregué. Revisa tus espacios."


# ---------------------------------------------------------------------
class Encuesta(Command):
    """'encuesta': responde con una tarjeta interactiva (Adaptive Card)."""

    def __init__(self):
        super().__init__(command_keyword="encuesta",
                         exact_command_keyword_match=True,
                         help_message="Responder una encuesta",
                         chained_commands=[EncuestaRespuesta()])

    def execute(self, message, attachment_actions, activity):
        titulo = TextBlock("¿Cómo vas con el laboratorio?", weight=FontWeight.BOLDER,
                           size=FontSize.MEDIUM, wrap=True)
        opciones = ChoiceSet(id="respuesta", isRequired=True, choices=[
            Choice(title="Todo funciona \U0001F680", value="todo funciona"),
            Choice(title="Voy avanzando", value="voy avanzando"),
            Choice(title="Necesito ayuda", value="necesito ayuda"),
        ])
        # Al presionar Enviar, Webex le manda al bot los datos con este callback
        enviar = Submit(title="Enviar", data={"callback_keyword": "encuesta_respuesta"})
        tarjeta = AdaptiveCard(body=[titulo, opciones], actions=[enviar])
        return response_from_adaptive_card(tarjeta)


class EncuestaRespuesta(Command):
    """Recibe lo que la persona marcó en la tarjeta."""

    def __init__(self):
        super().__init__(card_callback_keyword="encuesta_respuesta",
                         delete_previous_message=True)  # borra la tarjeta respondida

    def execute(self, message, attachment_actions, activity):
        nombre, _ = quien_escribe(activity)
        respuesta = attachment_actions.inputs.get("respuesta", "sin respuesta")
        return f"Gracias, **{nombre}**. Registré tu respuesta: _{respuesta}_."
