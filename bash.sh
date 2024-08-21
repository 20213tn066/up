#!/bin/bash

# Clonar el repositorio
git clone https://github.com/20213tn066/up
cd up/Hacking-main/

# Crear un entorno virtual
python3 -m venv env

# Activar el entorno virtual
source env/bin/activate

# Instalar gunicorn
pip install gunicorn

# Instalar dependencias del sistema
sudo apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Actualizar pip y setuptools
pip install --upgrade pip setuptools

# Instalar dependencias de Python
pip install -r requirements.txt

# Configurar la variable de entorno PASSWORD
echo "export PASSWORD=1234" >> .env

# Activar el entorno virtual nuevamente (para asegurarse de que la variable de entorno esté disponible)
source env/bin/activate

pip install gunicorn

# Iniciar la aplicación con gunicorn
gunicorn -b 0.0.0.0:8000 manage:app
