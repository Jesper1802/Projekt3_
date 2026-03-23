import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from zoneinfo import ZoneInfo

df3 = pd.read_csv("data/normale_user.csv")
df4 = pd.read_csv("data/invalid_user.csv")
df5 = pd.concat([df3, df4], ignore_index=True)


df_tz = pd.read_csv("data/laender_zeitzonen.csv")


def finde_zeitzone(land):
    treffer = df_tz[df_tz["country_name"] == land]

    if treffer.empty:
        print(f"Keine Zeitzone für {land} gefunden.")
        return None

    return treffer.iloc[0]["timezone"]


def uhrzeit_diagramm_fuer_ip_und_land(ip_adresse, land):
    ziel_zeitzone = finde_zeitzone(land)

    if ziel_zeitzone is None:
        return

    df_ip = df5[df5["ip"] == ip_adresse].copy()

    if df_ip.empty:
        print(f"Keine Einträge für die IP {ip_adresse} gefunden.")
        return

    liste = []

    for i in df_ip["zeit"]:
        dt = datetime.strptime(i, "%H:%M:%S").replace(tzinfo=ZoneInfo("UTC"))
        dt_andere_zeit = dt.astimezone(ZoneInfo(ziel_zeitzone))
        liste.append(dt_andere_zeit.strftime("%H"))

    df6 = pd.DataFrame(liste, columns=["Uhrzeit"])

    zeit_geordnet = df6.groupby("Uhrzeit").size().reset_index(name="Anzahl")

    zeit_geordnet["Uhrzeit"] = zeit_geordnet["Uhrzeit"].astype(int)
    zeit_geordnet = zeit_geordnet.sort_values("Uhrzeit")
    zeit_geordnet["Uhrzeit"] = zeit_geordnet["Uhrzeit"].astype(str).str.zfill(2)

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        x="Uhrzeit",
        y="Anzahl",
        hue="Uhrzeit",
        data=zeit_geordnet,
        ax=ax,
        palette="magma"
    )

    plt.title(f"Login-Zeiten für IP {ip_adresse} in {land}")
    plt.xlabel("Uhrzeit")
    plt.ylabel("Anzahl")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(f"img/uhrzeit/uhrzeit_bar{i}.png", dpi=300)
    