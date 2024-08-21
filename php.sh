#!/bin/bash

# Verificar si el script se ejecuta como root
if [ "$(id -u)" != "0" ]; then
   echo "Este script debe ejecutarse como root o con sudo." 1>&2
   exit 1
fi

# Actualizar lista de paquetes
echo "Actualizando lista de paquetes..."
apt-get update

# Instalar dependencias necesarias
echo "Instalando dependencias necesarias..."
apt-get install -y build-essential libxml2-dev libssl-dev libcurl4-openssl-dev libjpeg-dev libpng-dev libfreetype6-dev libbz2-dev libmcrypt-dev libmysqlclient-dev libreadline-dev libxslt1-dev autoconf wget

# Descargar el código fuente de PHP 5.2.4
echo "Descargando PHP 5.2.4..."
wget https://museum.php.net/php5/php-5.2.4.tar.gz -O /tmp/php-5.2.4.tar.gz

# Descomprimir el archivo descargado
echo "Descomprimiendo PHP 5.2.4..."
tar -xvzf /tmp/php-5.2.4.tar.gz -C /tmp

# Navegar al directorio descomprimido
cd /tmp/php-5.2.4

# Configurar la compilación
echo "Configurando la compilación de PHP 5.2.4..."
./configure --with-config-file-path=/etc/php5 --with-mysql --with-curl --with-zlib --with-gd --with-openssl --with-readline --enable-mbstring --enable-soap --enable-sockets --enable-zip

# Compilar e instalar PHP
echo "Compilando e instalando PHP 5.2.4..."
make
make install

# Configurar el archivo php.ini
echo "Configurando php.ini..."
mkdir -p /etc/php5
cp php.ini-dist /etc/php5/php.ini

# Verificar la instalación
echo "Verificando la instalación de PHP 5.2.4..."
php -v

echo "Instalación de PHP 5.2.4 completada."
