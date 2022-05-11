# Отчет по лабораторной работе № 2
## Задание
Настройка системы логирования данных трафика на основе ELK stack https://www.elastic.co/ с
правилами фильтрации через grok
## Установка и настройка Elasticsearch
Поскольку все пакеты Elastic Stack подписаны с помощью ключа Elasticsearch, чтобы защитить систему от подделки пакетов. Пакеты, прошедшие проверку подлинности с использованием ключа, будут считаться вашим менеджером пакетов доверенными.
Поэтому следует импортировать открытый ключ GPG Elasticsearch, добавить исходный список пакета Elastic и установить Elasticsearch.
```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
apt update && apt install elasticsearch
```
Затем следует отредактировать файл elasticsearch.yml:
![Файл elasticsearch.yml]()
После, можно запустить сервис:
```sh
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
```
## Установка и настройка Kibana
Поскольку исходный список Elastic уже добавлен, можно просто установить kibana:
```sh
sudo apt install kibana
sudo systemctl enable kibana
sudo systemctl start kibana
```
Для добавления авторизации необходимо немного сначала подготовить учетные данные:
```sh
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto
```
И отредактирвать файл kibana.yml:
![Файл kibana.yml]()
## Установка и настройка Logstash
Logstash позволяет собирать данные из разных источников и перобразовать и в общий формат.
```sh
sudo apt install logstash
```
В каталоге /etc/logstash/conf.d/ необходимо создать файлы input.conf и output.conf:
![Файл input.conf]()
Данные принимаются на 5044 порт
![Файл output.conf]()
В данном файле разбивается информация по типу и передается уже в elasticsearch на порт 9200.
## Установка и настройка Filebeat
Filebeat служит для сбора логов и передачи логов.
```sh
sudo apt install filebeat
sudo nano /etc/filebeat/filebeat.yml
sudo filebeat modules enable system
```
Следует отредактировать файл filebeat.yml:
![Файл filebeat.yml]()
## Установка и настройка Winlogbeat
Для настройки централизованного сервера сбора логов с Windows серверов, устанавливается сборщика системных логов winlogbeat, который можно скачать с официального сайта.
В корневой папке необходимо создать конфигурационный файл winlogbeat.yml.
![Файл winlogbeat.yml]()
## Проксирование подключений к Kibana через Nginx
Проксирование реализуется через сервис nginx:
```sh
sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
```
Создание администратора с паролем:
```sh
echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users
```
Далее создается блок server Nginx:
```sh
sudo nano /etc/nginx/sites-available/elk
```
![Файл elk]()
```sh
sudo ln -s /etc/nginx/sites-available/elk /etc/nginx/sites-enabled/elk
sudo nginx -t
sudo systemctl reload nginx
```
