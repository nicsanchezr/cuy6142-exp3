# CUY6142 · Experiencia 3 · Webex + Python

Repositorio oficial de materiales de la **Experiencia 3** de CUY6142 (Telepresencia y entornos innovadores de colaboración humana), Escuela de Informática y Telecomunicaciones, DUOC UC.

Aquí están los scripts de los laboratorios: clónalo en la VM DEVASC y trabaja directamente en la carpeta de cada laboratorio.

## Contenido

| Carpeta | Laboratorio |
|---|---|
| `lab1/` | 3.1.2 Creando nuestro entorno de trabajo y desarrollo |
| `lab2/` | 3.2.2 Gestionando salas, membresías y mensajes con la API de Webex |
| `lab3/` | 3.3.2 Creando un bot para Webex con Python e IA |
| `preparar_entorno.sh` | Instala Python 3.12 y las librerías del bot (laboratorio 3.3.2) |

## Al comenzar cada sesión en la VM DEVASC

Los equipos del laboratorio se restauran al reiniciar: lo que modifiques en la VM se pierde. Al comenzar cada sesión, clona el repositorio y entra a la carpeta del laboratorio (ejemplo con `lab3`):

```bash
mkdir -p ~/labs
cd ~/labs
git clone https://github.com/nicsanchezr/cuy6142-exp3.git
cd cuy6142-exp3/lab3
```

Luego crea tu `.env` a partir de `.env.ejemplo`. Los tokens nunca se suben a GitHub.

En el laboratorio 3.3.2, prepara el entorno de Python 3.12 desde la carpeta `lab3`:

```bash
bash ../preparar_entorno.sh
source .venv/bin/activate
```

## Alternativa: Windows con VS Code o VSCodium

1. Instala Python 3.12 desde https://www.python.org/downloads/ (marca **Add python.exe to PATH**) y VS Code (https://code.visualstudio.com) o VSCodium (https://vscodium.com).
2. Clona el repositorio (o usa **Code › Download ZIP**) y abre la carpeta del laboratorio con **File › Open Folder**.
3. En **Terminal › New Terminal** (PowerShell) instala las librerías. En Windows no hace falta entorno virtual:

```powershell
py -3.12 -m pip install -r requirements.txt
copy .env.ejemplo .env
py -3.12 00_bot_manual.py
```

En Windows, los scripts se ejecutan con `py -3.12` en vez de `python3`.

## Guardar tu trabajo en GitHub (opcional)

Si quieres conservar tus scripts, crea en GitHub un repositorio propio `cuy6142-webex` (con README) y, al terminar la sesión, copia tu carpeta y súbela (reemplaza `TU_USUARIO`):

```bash
cd ~/labs
git clone https://github.com/TU_USUARIO/cuy6142-webex.git
rsync -a --exclude .venv cuy6142-exp3/lab3 cuy6142-webex/
cd cuy6142-webex
git add .
git commit -m "Avance del laboratorio"
git push
```

El `.gitignore` de cada laboratorio evita que se suban el `.env` y la carpeta `.venv`.
