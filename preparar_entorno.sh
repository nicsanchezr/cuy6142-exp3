#!/usr/bin/env bash
# preparar_entorno.sh
# Deja listo el entorno del laboratorio 3.3.2 en la carpeta donde lo ejecutes:
#   1. instala uv (si falta), 2. instala Python 3.12,
#   3. crea el entorno virtual .venv y 4. instala las librerías de requirements.txt.
# Uso (dentro de tu carpeta lab3):  bash ~/labs/cuy6142-exp3/preparar_entorno.sh
set -e

if [ ! -f requirements.txt ]; then
    echo "[ERROR] No encuentro requirements.txt. Entra primero a tu carpeta lab3:"
    echo "        cd ~/labs/cuy6142-webex/lab3"
    exit 1
fi

if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
    echo "==> Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

echo "==> Instalando Python 3.12..."
uv python install 3.12

echo "==> Creando el entorno virtual .venv..."
python3.12 -m venv .venv

echo "==> Instalando las librerías..."
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt

echo
echo "[OK] Entorno listo con $(.venv/bin/python --version)."
echo "     Actívalo con:  source .venv/bin/activate"
