"""
ia.py
Conecta el bot con un modelo de lenguaje a través de OpenRouter.
OpenRouter usa el mismo formato que la API de OpenAI:
  POST https://openrouter.ai/api/v1/chat/completions
"""
import requests
from webex_bot.models.command import Command

from utilidades import cargar_variable

URL_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"

# El "rol" le dice al modelo cómo comportarse. Puedes cambiarlo (Paso 6.4).
ROL = ("Eres el asistente de un curso de telepresencia y colaboración de Duoc UC. "
       "Respondes en español de Chile, de forma breve (máximo 5 líneas) y amable. "
       "Si no sabes algo, lo dices.")


def consultar_modelo(texto, rol):
    """Hace una solicitud a OpenRouter y devuelve la respuesta HTTP."""
    return requests.post(
        URL_OPENROUTER,
        headers={"Authorization": f"Bearer {cargar_variable('OPENROUTER_API_KEY')}"},
        json={
            "model": cargar_variable("OPENROUTER_MODELO", obligatoria=False,
                                     por_defecto="openrouter/free"),
            "messages": [
                {"role": "system", "content": rol},
                {"role": "user", "content": texto},
            ],
            "max_tokens": 1500,
            # Algunos modelos gratuitos "razonan" antes de responder y ese
            # razonamiento gasta tokens: se limita para que quede espacio
            # para la respuesta, y no se incluye en lo que devuelve la API.
            "reasoning": {"effort": "low", "exclude": True},
        },
        timeout=60,
    )


def preguntar_ia(texto, rol=ROL, intentos=2):
    """Envía el texto al modelo y devuelve su respuesta como texto.
    rol: instrucciones para el modelo (por defecto, el ROL del asistente).
    Si el modelo responde vacío, lo intenta una vez más."""
    for intento in range(1, intentos + 1):
        try:
            respuesta = consultar_modelo(texto, rol)
        except requests.exceptions.RequestException as error:
            print("[IA] Error de conexión:", error)
            return "No pude conectarme con la IA. Intenta de nuevo en un momento."

        if respuesta.status_code == 401:
            return "La API key de OpenRouter no es válida: revisa el archivo .env."
        if respuesta.status_code == 429:
            return "Llegué al límite de consultas gratuitas. Intenta en un rato."
        if respuesta.status_code != 200:
            return f"La IA no respondió (HTTP {respuesta.status_code}). Intenta de nuevo."

        datos = respuesta.json()
        eleccion = datos["choices"][0]
        # El texto viene en choices[0].message.content. A veces llega vacío
        # (None), por ejemplo si el modelo gastó todos sus tokens "pensando".
        texto_respuesta = eleccion["message"].get("content") or ""
        if texto_respuesta.strip():
            return texto_respuesta.strip()
        print("[IA] Respuesta vacía (intento {} de {}). Modelo: {}, motivo: {}".format(
            intento, intentos, datos.get("model"), eleccion.get("finish_reason")))

    return "La IA no generó una respuesta esta vez. Vuelve a preguntar."


class AsistenteIA(Command):
    """
    Se usa cuando el mensaje no coincide con ningún comando:
    en vez de mostrar la ayuda, el bot le pasa la pregunta a la IA.
    Si escriben 'ayuda' o un mensaje vacío, muestra el menú de ayuda.
    """

    def __init__(self, ayuda):
        super().__init__(help_message="Preguntarle a la IA")
        self.ayuda = ayuda          # el comando de ayuda original del bot

    def pre_execute(self, message, attachment_actions, activity):
        if not self.es_ayuda(message):
            return "Pensando... \U0001F914"   # aviso mientras la IA responde

    def execute(self, message, attachment_actions, activity):
        if self.es_ayuda(message):
            return self.ayuda.build_card(message, attachment_actions, activity)
        return preguntar_ia(message)

    @staticmethod
    def es_ayuda(message):
        return message.strip().lower() in ("", "ayuda")
