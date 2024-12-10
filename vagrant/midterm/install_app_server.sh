sudo apt update

# Install apache2
sudo apt-get install -y apache2 mysql-client
#sudo update-alternatives --config httpd
#sudo update-alternatives --install /usr/bin/httpd httpd /usr/sbin/apache2 1
sudo a2enmod rewrite

# Install PHP
sudo apt-get install -y ca-certificates apt-transport-https software-properties-common 
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update
sudo apt-get install -y php8.1 php8.1-mysql
sudo sed -i "s/short_open_tag.*/short_open_tag = On/" /etc/php/8.1/apache2/php.ini

# Set default version of php
sudo update-alternatives --install /usr/bin/php php /usr/bin/php8.1 1
sudo update-alternatives --config php

sudo systemctl restart apache2