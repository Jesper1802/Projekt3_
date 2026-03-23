import os
import ipaddress
import pandas as pd
import bisect
import seaborn as sns
import matplotlib.pyplot as plt
import ipadressen
import zeit

df1 = pd.read_csv("data/GeoLite2-Country-Blocks-IPv4.csv")
df2 = pd.read_csv("data/GeoLite2-Country-Locations-en.csv")
df3 = pd.read_csv("data/normale_user.csv")
df4 = pd.read_csv("data/invalid_user.csv")

 
df5 = pd.concat([df3, df4], ignore_index=True)

gleich = df5["ip"].value_counts()

i = 0

while i <= 4:
    top_ip = gleich.index[i]

    zeiten = df5.groupby(by="ip")

    for key, value in zeiten:
        if key == top_ip:
            print("===", key, "===")
            anzahl = value["monat"].value_counts()

    anzahl_df = anzahl.reset_index()
    anzahl_df.columns = ["monat", "anzahl"]

    land = ipadressen.finde_land(top_ip)

    zeit.uhrzeit_diagramm_fuer_ip_und_land(top_ip, land)


    plt.figure(figsize=(12,6))

    sns.barplot(
        x="anzahl",
        y="monat",
        hue = "monat",
        data=anzahl_df,
        order=["Dec", "Jan", "Feb", "Mar"],
        palette="Reds_r"
    )

    plt.title(f'IP: {top_ip} \n Land: {land}')
    plt.xlabel("Anzahl")
    plt.ylabel("Monat")

    plt.tight_layout()
    plt.savefig(f"img/monat/anzahl_topIp_monat{i}.png", dpi=300)

    i += 1
    






