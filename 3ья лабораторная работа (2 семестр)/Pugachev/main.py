from asyncore import write
from nfstream import NFStreamer
import pandas as pd

def writedown(value):
    with open("report.md", "a", encoding="utf-8") as file:
        file.write("\n"+value)

id_protocols = {1:"ICMP", 6:"TCP", 8:"EGP", 9:"IGP", 17:"UDP", 27:"RDP", 50:"ESP"}

file = open('report.md', 'w')
file.write("Checking for VPN traffic:")
file.close()

if __name__ == '__main__':
    file_path = input()
    df = NFStreamer(source=file_path).to_pandas(columns_to_anonymize=[])
    df1 = []
    df3 = []

    # Проверка на наличие VPN трафика
    vpn_counter = 0
    for id, flow in df.iterrows():
        if flow.application_category_name == 'VPN':
            writedown("ID package: {}\nView VPN: {}\nProtocol: {}".format(id, flow.application_name, id_protocols[flow.protocol]))
            vpn_counter += 1
        df1.append([flow.src_ip, 
                    flow.dst_ip,
                    flow.bidirectional_packets,     
                    flow.bidirectional_bytes,
                    flow.application_name,
                    flow.application_category_name])
        df3.append([flow.bidirectional_bytes,
                    flow.application_name,
                    flow.application_category_name])

    df1 = pd.DataFrame(df1, columns=["src_ip",
                                    "dst_ip",
                                    "packets",
                                    "bytes",
                                    "app_name",
                                    "app_category_name"])

    df3 = pd.DataFrame(df3, columns=["bidirectional_bytes",
                                    "Application",
                                    "application_category_name"])
    if vpn_counter == 0:
        writedown("No VPN traffic\n")
    writedown("")
    # Вывод информации: src_ip, dst_ip, bidirectional_packets, bidirectional_bytes, app_name, app_category_name
    writedown(df1.to_markdown())
    df2 = "\n1. Source unique source IP-address:"
    for src_ip in df1["src_ip"].unique():
        df2 += "\n"+"\t - "+src_ip
    df2 += "\n2. Distanation unique IP-address:"
    for dst_ip in df1["dst_ip"].unique():
        df2 += "\n"+"\t - "+dst_ip
    df2 += "\n3. Unique application names:"
    for app_name in df1["app_name"].unique():
        df2 += "\n"+"\t - "+app_name
    writedown(df2)
    writedown("")
    # Вывод "полезной" информации
    df3_table = []
    for app in df3['Application'].unique():
        for category in df3[df3['Application'] == app]['application_category_name'].unique():
            df3_table.append([app, category, df3["bidirectional_bytes"].where(df3["Application"]==app).sum()])

    df3_table = pd.DataFrame(df3_table, columns=["Application",
                                                "Category",
                                                "Bidirectional bytes"])
    writedown(df3_table.to_markdown())