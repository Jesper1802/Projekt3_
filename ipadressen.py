import os
import ipaddress
import pandas as pd
import bisect
import seaborn as sns
import matplotlib.pyplot as plt

df1 = pd.read_csv("data/GeoLite2-Country-Blocks-IPv4.csv")
df2 = pd.read_csv("data/GeoLite2-Country-Locations-en.csv")
df3 = pd.read_csv("data/normale_user.csv")
df4 = pd.read_csv("data/invalid_user.csv")


df5 = pd.concat([df3, df4], ignore_index=True)

df1["start_ip"] = df1["network"].apply(lambda x: int(ipaddress.IPv4Network(x).network_address))
df1["end_ip"] = df1["network"].apply(lambda x: int(ipaddress.IPv4Network(x).broadcast_address))

df1 = df1.sort_values("start_ip").reset_index(drop=True)
start_ips = df1["start_ip"].tolist()

country_map = df2.set_index("geoname_id")["country_name"].to_dict()

def finde_land(ip_string):
    try:
        ip_int = int(ipaddress.IPv4Address(ip_string))
    except ValueError:
        return "Ungültige IP"

    index = bisect.bisect_right(start_ips, ip_int) - 1

    if index >= 0:
        row = df1.iloc[index]
        if row["start_ip"] <= ip_int <= row["end_ip"]:
            geoname_id = row["geoname_id"]
            return country_map.get(geoname_id, "Unbekannt")

    return "Kein Land gefunden"

unique_ips = df5["ip"].drop_duplicates()
ip_to_country = {ip: finde_land(ip) for ip in unique_ips}
df5["country_name"] = df5["ip"].map(ip_to_country)

count_df = df5["country_name"].value_counts().reset_index()
count_df.columns = ["country_name", "anzahl"]

top_df = count_df.head(5)

sns.set_style("whitegrid")
os.makedirs("img", exist_ok=True)

plt.figure(figsize=(10, 10))
plt.pie(
    top_df["anzahl"],
    labels=top_df["country_name"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Top 5 Länder")
plt.axis("equal")
plt.savefig("img/laender_plot_pie.png", dpi=300)
plt.show()

plt.figure(figsize=(12,6))

sns.barplot(
    x="country_name",
    y="anzahl",
    data=top_df
)

plt.title("Top 5 Länder (Säulendiagramm)")
plt.xlabel("Land")
plt.ylabel("Anzahl")

plt.xticks(rotation=45) 

plt.tight_layout()

plt.savefig("img/laender_plot_bar.png", dpi=300)

plt.show()



