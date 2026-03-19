import pandas as pd

with open("data/all-failed-logins.txt") as f:
    df = pd.DataFrame(f.readlines(), columns=["log"])

df["zeit"] = pd.to_datetime(df["log"].str[:15] + " 2024")

df["diff"] = df["zeit"].diff().dt.total_seconds()

durchschnitt = df["diff"].mean()

minimum = df["diff"].min()

maximum = df["diff"].max()

print(f"Der durchschnittliche Zeitabstand beträgt {durchschnitt:.2f} Sekunden, der minimale {minimum:.2f} Sekunden und der maximale {maximum:.2f} Sekunden.")