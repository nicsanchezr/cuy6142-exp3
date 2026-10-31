"""
utilidades.py
Funciones de apoyo para leer la configuración del archivo .env.
(En Colab, los valores llegan desde los Secrets como variables de entorno.)
"""
import os
import sys

try:
    from dotenv import load_dotenv  # paquete python-dotenv
    load_dotenv()
except ImportError:
    # Sin python-dotenv (por ejemplo, con el Python de la VM): se lee el .env a mano
    if os.path.exists(".env"):
        with open(".env", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    nombre, valor = linea.split("=", 1)
                    os.environ.setdefault(nombre.strip(), valor.strip())


def cargar_variable(nombre, obligatoria=True, por_defecto=""):
    """Lee una variable del .env (o del entorno) y avisa si falta."""
    valor = os.getenv(nombre, por_defecto).strip().strip('"').strip("'")
    if obligatoria and not valor:
        print(f"[ERROR] Falta la variable {nombre} en el archivo .env")
        sys.exit(1)
    return valor


def cargar_token_bot():
    """Token del bot, sin la palabra 'Bearer' si se copió con ella."""
    token = cargar_variable("WEBEX_BOT_TOKEN")
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token


def cargar_lista(nombre):
    """Convierte 'a@x.com, b@y.com' en ['a@x.com', 'b@y.com']."""
    texto = cargar_variable(nombre)
    return [parte.strip() for parte in texto.split(",") if parte.strip()]
