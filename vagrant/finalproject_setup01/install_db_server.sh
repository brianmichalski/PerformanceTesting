# Install MySQL
sudo apt update
sudo apt install mysql-server-8.0 -y

#sudo ufw enable
#sudo ufw allow 3306/tcp
#sudo ufw reload
#sudo netstat -tulnp | grep 3306

# Update the bind-address in the MySQL config file
sudo sed -i "s/^bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
sudo sed -i "s/^#thread_cache_size.*/thread_cache_size = 16/" /etc/mysql/mysql.conf.d/mysqld.cnf

# Enable pdo_mysql extension in the PHP config file
#sudo sed -i "s/^;extension=pdo_mysql.*/extension=pdo_mysql/" /etc/php/8.1/apache2/php.ini

# Restart MySQL to apply changes  
sudo systemctl restart mysql.service