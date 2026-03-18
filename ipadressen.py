import ipaddress
import pandas as pd

df1 = pd.read_csv("data/GeoLite2-Country-Blocks-IPv4.csv")

df2 = pd.read_csv("data/GeoLite2-Country-Locations-en.csv")


def finde_netzwerk(ip_string, netz_liste):
    ip = ipaddress.IPv4Address(ip_string)

    for netz in netz_liste:
        if ip in ipaddress.IPv4Network(netz):
            return netz

    return None

netzwerke = df1["network"].tolist()

ergebnis = finde_netzwerk("41.77.144.98", netzwerke)

country = df1[df1["network"] == ergebnis]

country_test = int(country.iloc[0]["geoname_id"])

print(country_test)

land = df2[df2["geoname_id"] == country_test].iloc[0]["country_name"]

print(land)

