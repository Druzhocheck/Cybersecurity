Checking for VPN traffic:
ID package: 4
View VPN: OpenVPN
Protocol: UDP

|    | src_ip                    | dst_ip          |   packets |   bytes | app_name   | app_category_name   |
|---:|:--------------------------|:----------------|----------:|--------:|:-----------|:--------------------|
|  0 | 192.168.5.138             | 192.168.5.2     |         9 |     990 | NetBIOS    | System              |
|  1 | 192.168.5.1               | 224.0.0.251     |         4 |     400 | MDNS       | Network             |
|  2 | fe80::3df4:a1b3:c743:15bf | ff02::fb        |         4 |     480 | MDNS       | Network             |
|  3 | 192.168.5.138             | 20.54.37.73     |         8 |     878 | TLS.Azure  | Cloud               |
|  4 | 192.168.5.138             | 94.103.81.152   |       225 |   43507 | OpenVPN    | VPN                 |
|  5 | 192.168.5.138             | 239.255.255.250 |         4 |     868 | SSDP       | System              |

1. Source unique source IP-address:
	 - 192.168.5.138
	 - 192.168.5.1
	 - fe80::3df4:a1b3:c743:15bf
2. Distanation unique IP-address:
	 - 192.168.5.2
	 - 224.0.0.251
	 - ff02::fb
	 - 20.54.37.73
	 - 94.103.81.152
	 - 239.255.255.250
3. Unique application names:
	 - NetBIOS
	 - MDNS
	 - TLS.Azure
	 - OpenVPN
	 - SSDP

|    | Application   | Category   |   Bidirectional bytes |
|---:|:--------------|:-----------|----------------------:|
|  0 | NetBIOS       | System     |                   990 |
|  1 | MDNS          | Network    |                   880 |
|  2 | TLS.Azure     | Cloud      |                   878 |
|  3 | OpenVPN       | VPN        |                 43507 |
|  4 | SSDP          | System     |                   868 |