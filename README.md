# CUY6142 · Experiencia 3 · Webex + Python

Repositorio oficial de materiales de la **Experiencia 3** de CUY6142 (Telepresencia y entornos innovadores de colaboración humana), Escuela de Informática y Telecomunicaciones, DUOC UC.

Aquí están los scripts de los laboratorios. **Tu trabajo no se guarda aquí**: lo guardas en tu propio repositorio `cuy6142-webex`.

## Contenido

| Carpeta | Laboratorio |
|---|---|
| `lab1/` | 3.1.2 Creando nuestro entorno de trabajo y desarrollo |
| `lab2/` | 3.2.2 Gestionando salas, membresías y mensajes con la API de Webex |
| `lab3/` | 3.3.2 Creando un bot para Webex con Python e IA |
| `preparar_entorno.sh` | Instala Python 3.12 y las librerías del bot (laboratorio 3.3.2) |

## Al comenzar cada sesión en la VM DEVASC

Los equipos del laboratorio se restauran al reiniciar: lo que no esté en GitHub se pierde. Por eso, al comenzar, clonas los dos repositorios y copias la carpeta del laboratorio a tu repositorio (ejemplo con `lab3`; reemplaza `TU_USUARIO`):

```bash
mkdir -p ~/labs
cd ~/labs
git clone https://github.com/nicsanchezr/cuy6142-exp3.git
git clone https://github.com/TU_USUARIO/cuy6142-webex.git
cp -rn cuy6142-exp3/lab3 cuy6142-webex/
cd cuy6142-webex/lab3
```

`cp -rn` copia los archivos que te falten **sin sobrescribir** los que ya modificaste en sesiones anteriores.

Luego crea tu `.env` a partir de `.env.ejemplo` (los tokens nunca se suben a GitHub).

## Al terminar cada sesión

```bash
cd ~/labs/cuy6142-webex
git add .
git commit -m "Avance del laboratorio"
git push
```

## Nunca subas a GitHub

- El archivo `.env` (tus tokens y API keys).
- La carpeta `.venv`.

El `.gitignore` de cada laboratorio ya los excluye.
