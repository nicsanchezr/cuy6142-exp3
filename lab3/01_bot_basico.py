"""
01_bot_basico.py
Bot de Webex que responde solo. Se conecta a Webex por websocket:
no necesita una URL pública ni webhooks.

Detener el bot: Ctrl+C en la terminal (o el botón de detener en Colab).
"""
from webex_bot.webex_bot import WebexBot

from comandos import CrearSala, Encuesta, Hola
from utilidades import cargar_lista, cargar_token_bot

bot = WebexBot(
    teams_bot_token=cargar_token_bot(),
    approved_users=cargar_lista("USUARIOS_PERMITIDOS"),  # solo ellos lo usan
    bot_name="Bot CUY6142",
    bot_help_subtitle="Estos son mis comandos. Haz clic en uno o escríbelo.",
    threads=False,                     # responde en la conversación, no en hilos
)

# Comandos del bot (el comando "help" viene incluido)
bot.add_command(Hola())
bot.add_command(CrearSala())
bot.add_command(Encuesta())

print("Bot iniciado. Escríbele desde Webex. Para detenerlo: Ctrl+C")
bot.run()
