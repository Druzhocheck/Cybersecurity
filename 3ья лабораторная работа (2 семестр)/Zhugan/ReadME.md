# Лабораторная работа 3.1 (часть 1)
## Задача:
Настройка VPN соединения с использованием Wireguard.
## Конфигурация сервера:
Выделеный VPS сервер с ОС Ubuntu 20.04, публичный IP.
## Конфигурация клиента:
Физический хост с OC Windows Server 2012.
## Операции выполняемые на сервере:
### 1. Обновление операционной системы:
```sh
apt update
apt upgrade
```
### 2. Установка Wireguard:
```sh
apt install wireguard
```
### 3. Настройка пренаправления пакетов:
```sh
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
```
### 4. Создание приватного и публичного ключей сервера:
```sh
wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
```
### 5. Создание конфигурационного файла Wireguard (wg0.conf):
```sh
echo "[Interface]" >> wg0.conf
echo "Address = 10.0.0.1/24" >> wg0.conf				# IP-адрес сервера в VPN сети
echo "PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
echo "PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
echo "ListenPort = 51820" >> wg0.conf
echo "PrivateKey = <Server_private_key>" >> wg0.conf	# Приватный ключ сервера из файла 'privatekey'
```
### 6. Поднятие интерфейса, запуск и конфигурирование сервиса:
```sh
wg-quick up wg0						# Поднятие интерфейса wg0
systemctl start wg-quick@wg0		# Запуск сервиса Wireguard
systemctl enable wg-quick@wg0		# Конфигурирование сервиса на запуск при каждой загрузке системы
systemctl status wg-quick@wg0		# Проверка статуса сервиса
wg show wg0							# Проверка состояния Wireguard
```

### 7. Добавление клиента:
Для добавления клиента необходимо сгенерировать его приватный и публичный ключи:
```sh
wg genkey | tee /etc/wireguard/client_privatekey | wg pubkey | tee /etc/wireguard/client_publickey
```
Публичный ключ клиента и ip-адрес необходимо добавить в файл конфигурации сервера wg0.conf, для этого добавляется дополнительный раздел:
```sh
echo "[Peer]" >> wg0.conf
echo "Publickey = <Client_public_key>" >> wg0.conf 	# Публичный ключ клиента из файла 'client_publickey'
echo "AllowedIPs = 10.0.0.4/32" >> wg0.conf			# IP-адрес клиента в VPN сети
```
После изменения конфигурационного файла wg0.conf необходимо перезапустить сервис Wireguard:
```sh
systemctl restart wg-quick@wg0
```
### 8. Проверка конфигурации сервера:
Проверка статуса сервиса:
```sh
systemctl status wg-quick@wg0
```
Вывод консоли должен иметь вид:
```sh
root@1234:~# systemctl status wg-quick@wg0
● wg-quick@wg0.service - WireGuard via wg-quick(8) for wg0
     Loaded: loaded (/lib/systemd/system/wg-quick@.service; enabled; vendor pre>
     Active: active (exited) since Mon 2022-04-04 09:31:25 UTC; 3h 32min ago
       Docs: man:wg-quick(8)
             man:wg(8)
             https://www.wireguard.com/
             https://www.wireguard.com/quickstart/
             https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8
             https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8
    Process: 1813 ExecStart=/usr/bin/wg-quick up wg0 (code=exited, status=0/SUC>
   Main PID: 1813 (code=exited, status=0/SUCCESS)
```
Проверка состояния Wireguard:
```sh
wg show wg0
```
Вывод консоли должен иметь вид:
```sh
root@1234:~# wg show wg0
interface: wg0
  public key: <Server_public_key>
  private key: (hidden)
  listening port: 51820

peer: <Client_public_key>
  allowed ips: 10.0.0.4/32
```
Проверка конфигурации интерфейса:
```sh
ifconfig
```
Вывод консоли должен иметь вид:
```sh
root@1234:/etc/wireguard# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.2  netmask 255.255.255.0  broadcast 192.168.0.255
        inet6 fe80::f816:3eff:feb1:628c  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:b1:62:8c  txqueuelen 1000  (Ethernet)
        RX packets 118036  bytes 113373326 (113.3 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 114328  bytes 114165574 (114.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wg0: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1420
        inet 10.0.0.1  netmask 255.255.255.0  destination 10.0.0.1
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

## Операции выполняемые на клиенте:
### 1. Установка клиента Wireguarg:
Клиент Wireguard доступен на официальном сайте проекта: https://www.wireguard.com/install/ 
В процессе установки особых манипуляций не требуется.
### 2. Создание файла конфигурации клиента Wireguarg:
Для настройки клиента Wireguarg, создается конфигурационный файл client.conf следующего содержания:
```sh
[Interface]

PrivateKey = <Client_private_key> 		# Приватный ключ клиента из файла 'client_privatekey'

Address = 10.0.0.4/32

DNS = 8.8.8.8

[Peer]

PublicKey = <Server_public_key> 		# Публичный ключ сервера из файла 'publickey'

Endpoint = <Public_IP_VPN_Server>:51820

AllowedIPs = 0.0.0.0/0

PersistentKeepalive = 20
```
### 3. Настройка и запуск клиента Wireguarg:

Для соединения с сервером в клиенте Wireguard импортируется файл client.conf:

Add Tunnel -> Import tunnel(s) from file -> В открывшемся окне выбрать файл client.conf -> Activate

### 4. Проверка конфигурации клиента Wireguarg:
Об успешном установлении соединения в клиенте Wireguard свидетельствует появление в разделе "Peer" поля "Transfer", отображающего сведения об объеме полученной и переданной информации.

Проверка статуса сервиса:
```sh
ipconfig
```
Вывод консоли должен иметь вид:
```sh
Windows IP Configuration


Unknown adapter vpn_full_11:

   Connection-specific DNS Suffix  . : 
   IPv4 Address. . . . . . . . . . . : 10.0.0.4
   Subnet Mask . . . . . . . . . . . : 255.255.255.255
   Default Gateway . . . . . . . . . : 0.0.0.0
```
Проверка доступности VPN сервера:
```sh
ping 10.0.0.1
```
Вывод консоли должен иметь вид:

```sh
Pinging 10.0.0.4 with 32 bytes of data:
Reply from 10.0.0.1: bytes=32 time<1ms TTL=128
Reply from 10.0.0.1: bytes=32 time<1ms TTL=128
Reply from 10.0.0.1: bytes=32 time<1ms TTL=128
Reply from 10.0.0.1: bytes=32 time<1ms TTL=128

Ping statistics for 10.0.0.1:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms
```	
## Проверка состояния соединения на стороне сервера:
Проверка состояния соединения на стороне сервера выполняется с помощью команды:

```sh
wg show wg0
```
Вывод консоли должен иметь вид:
```sh
root@1234:~# wg show wg0
interface: wg0
  public key: <Server_public_key>
  private key: (hidden)
  listening port: 51820

peer: <Client_public_key>
  endpoint: <IP_address_provided_to_the_client_by_the_ISP>:61514
  allowed ips: 10.0.0.4/32
  latest handshake: 19 seconds ago
  transfer: 295.53 KiB received, 911.37 KiB sent
```
Проверка доступности клиента:
```sh
ping 10.0.0.4 -с 4
```
Вывод консоли должен иметь вид:

```sh
root@1234:~# ping 10.0.0.4 -c 4
PING 10.0.0.4 (10.0.0.4) 56(84) bytes of data.
64 bytes from 10.0.0.4: icmp_seq=1 ttl=128 time=109 ms
64 bytes from 10.0.0.4: icmp_seq=2 ttl=128 time=108 ms
64 bytes from 10.0.0.4: icmp_seq=3 ttl=128 time=108 ms
64 bytes from 10.0.0.4: icmp_seq=4 ttl=128 time=108 ms

--- 10.0.0.4 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 108.099/108.338/108.810/0.281 ms
```
## Вывод:
В результате выполнения лабораторной работы произведена настройка VPN соединения с использованием Wireguard.


# Лабораторная работа 3.1 (часть 2)
## Задача:
Настройка VPN соединения с использованием IPSec/IKEv2.
## Конфигурация сервера:
Выделеный VPS сервер с ОС Ubuntu 20.04, публичный IP.
## Конфигурация клиента:
Физический хост с OC Windows Server 2012.
## Операции выполняемые на сервере:
### 1. Обновление операционной системы:
```sh
apt update
apt upgrade
```
### 2. Установка VPN сервера с IPSec/IKEv2:

Установка выполняется автоматического с использованием  скрипта, для установки необходимо выполнить команду:
```sh
wget https://git.io/vpnsetup -qO vpn.sh && sudo sh vpn.sh
```
Результатом работы скрипта является настройка VPN сервера с IPSec/IKEv2, генерация учетных данных для подключения, а так же файлов конфигурации клиента для различных ОС.

## Операции выполняемые на клиенте:
### 1. Настройка подключения к VPN серверу с IPSec/IKEv2:
Настройка подключения на клиенте выполняется в соответствии с инструкцией https://github.com/hwdsl2/setup-ipsec-vpn/blob/master/docs/clients.md#windows

1. Правой кнопкой кликнуть на значёк wireless/network в системном трее.
1. Выбрать **Open Network & Internet settings**, выбрать **Open Network and Sharing Center**.
1. Выбрать **Set up a new connection or network**.
1. Выбрать **Connect to a workplace**, нажать **Next**.
1. Выбрать **Use my Internet connection (VPN)**.
1. Ввести ip-адрес VPN сервера в поле **Internet address**.
1. Ввести имя подключения **Destination name** и нажать **Create**.
1. Вернуться в **Network and Sharing Center**. Перейти в меню **Change adapter settings**.
1. Правой кнопкой мыши кликнуть на вновьсозданном VPN подключении и выбрать **Properties**.
1. Перейти на вкладку **Security**. Выбрать "Layer 2 Tunneling Protocol with IPsec (L2TP/IPSec)" в поле **Type of VPN**.
1. Выбрать **Allow these protocols**. Отметить галочкой пункты "Challenge Handshake Authentication Protocol (CHAP)" и "Microsoft CHAP Version 2 (MS-CHAP v2)".
1. Перейти в **Advanced settings**.
1. Выбрать **Use preshared key for authentication** ввести VPN IPsec PSK, полученный в результате настройки сервера в поле **Key**.
1. Нажать **OK** для закрытия **Advanced settings**.
1. Нажать **OK** для сохранения настроек соединения VPN.

### 2. Подключение к VPN серверу с IPSec/IKEv2:
Для подключения к VPN:

1. Выбрать значок wireless/network в системном трее.
1. Выберать новую запись VPN и нажать «Подключиться». 
1. При появлении запроса ввести имя пользователя и пароль VPN, полученные при конфигурировании сервера, затем нажать «ОК».

### 3. Устранение проблем подключения к VPN серверу:

При возникновении ошибки 809 при подключении с использованием клиента под ОС Windows, необходимо добавить ключ реестра командой:

```sh
REG ADD HKLM\SYSTEM\CurrentControlSet\Services\PolicyAgent /v AssumeUDPEncapsulationContextOnSendRule /t REG_DWORD /d 0x2 /f
```
Более подробная информация об устранении неполадок доступна по ссылке https://github.com/hwdsl2/setup-ipsec-vpn/blob/master/docs/clients.md#windows-error-809

### 4. Проверка соединения на стороне клиента:
Необходимо убедиться что был успешно добавлен PPP адаптер, выполнив команду:
```sh
ipconfig
```
Вывод консоли должен иметь вид:
```sh
Windows IP Configuration


PPP adapter VPN Connection:

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : 192.168.42.10
   Subnet Mask . . . . . . . . . . . : 255.255.255.255
   Default Gateway . . . . . . . . . : 0.0.0.0
```

## Проверка состояния соединения на стороне сервера:
Проверка состояния соединения на стороне сервера выполняется с помощью команды:
```sh
ifconfig
```
Вывод консоли должен иметь вид:
```sh
root@1234:~# ifconfig
ppp0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1280
        inet 192.168.42.1  netmask 255.255.255.255  destination 192.168.42.10
        ppp  txqueuelen 3  (Point-to-Point Protocol)
        RX packets 15795  bytes 1748906 (1.7 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 21118  bytes 15498066 (15.4 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
## Вывод:
В результате выполнения лабораторной работы произведена настройка VPN соединения с использованием IPSec/IKEv2.




























