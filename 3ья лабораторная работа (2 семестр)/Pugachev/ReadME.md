# Отчет по лабораторной работе № 3 (Часть 1)
## Задание:
Настройка VPN подключений Wireguard и IPSec/IKEv2.
Для каждого типа VPN подключения необходимо настроить отдельный сервер или виртуальную 
машину с Ubuntu/CentOS/Fedora.
## Настройка WireGuard
### Серверная часть
В качестве сервера используется Ubuntu Server 20.04.
Обновляем пакеты и устанавливаем WireGuard
```sh
sudo apt update
sudo apt install wireguard
```
Создаем приватный и публичный ключи
```sh
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey
```
Настройка конфига выглядит следующим образом:
```sh
sudo nano /etc/wireguard/wg0.conf
```
```sh
[Interface]
Address = 10.0.0.1/24
SaveConfig = true
ListenPort = 51820
PrivateKey = </etc/wireguard/privatekey>
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t ens3 -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t ens3 -D POSTROUTING -o ens3 -j MASQUERADE
```
Поднимаем интерфейс
```sh
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
sudo wg-quick up wg0
sudo wg show wg0
sudo systemctl enable wg-quick@wg0
sudo ufw allow 51820/udp
```
### Клиентская часть
ОС клиента - Windows 10. Необходимо установить WireGuard, скачав с официального сайта.
Добавить пустой туннель и заполнить:
```sh
[Interface]
PrivateKey = CLIENT_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = SERVER_IP_ADDRESS:51820
AllowedIPs = 0.0.0.0/0
```
После в сервеной части необходимо добавить клиента:
```sh
[Peer]
PublicKey = <СLIENT-PUBLIC-KEY>
AllowedIPs = 10.0.0.2/32
```
В конечном итоге серверная часть юудет иметь вид:
![Файл wg0.conf](https://github.com/Druzhocheck/Cybersecurity/blob/main/3%D1%8C%D1%8F%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20(2%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80)/Pugachev/img/wg0.png)
Перезапустить сервис:
```sh
systemctl restart wg-quick@wg0
```
И в клиентской части подключить туннель.
Подключение примет вид:
![Подключение](https://github.com/Druzhocheck/Cybersecurity/blob/main/3%D1%8C%D1%8F%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20(2%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80)/Pugachev/img/connect.jpg)
## IPSec/IKEv2
### Настройка серверной части
В качестве сервера используется Ubuntu Server 20.04.
После обновления пакетов, необходимо сгенерировать учетные данные VPN:
```sh
wget https://git.io/vpnsetup -qO vpn.sh && sudo sh vpn.sh
```
Затем следует добавить клиента.
Необходимы файлы на клиентской стороне:
![IPSec](https://github.com/Druzhocheck/Cybersecurity/tree/main/3%D1%8C%D1%8F%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20(2%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80)/Pugachev/img/ipsec.png)
### Настройка клиентской части
Необходимо перенести файл с сервера *.p12(клиент). Запустить специальный файл сценария, который находящийся в той же папке, что и *.p12. Заполнить информацию о учетныйх данных VPN и подключиться.
