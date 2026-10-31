"""
02_bot_ia.py
El mismo bot del paso anterior, ahora con IA:
si un mensaje no es un comando, se lo pregunta a un modelo de lenguaje.
"""
from webex_bot.webex_bot import WebexBot

from comandos import CrearSala, Encuesta, Hola
from ia import AsistenteIA
from utilidades import cargar_lista, cargar_token_bot

bot = WebexBot(
    teams_bot_token=cargar_token_bot(),
    approved_users=cargar_lista("USUARIOS_PERMITIDOS"),
    bot_name="Bot CUY6142",
    bot_help_subtitle="Usa un comando o hazme cualquier pregunta.",
    threads=False,
)

bot.add_command(Hola())
bot.add_command(CrearSala())
bot.add_command(Encuesta())

# Lo que no sea un comando, va a la IA
bot.help_command = AsistenteIA(ayuda=bot.help_command)

print("Bot con IA iniciado. Escríbele desde Webex. Para detenerlo: Ctrl+C")
bot.run()
