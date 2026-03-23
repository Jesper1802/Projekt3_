import pandas as pd

logs = []

with open("data/failed_ssh until 2026-2-13.log", "r") as file:
    for line in file:
        parts = line.split()

        # Check ob invalid user
        if parts[8] == "invalid":
            user = parts[10]
            invalid = True
            ip = parts[12]
            port = parts[14]
        else:
            user = parts[8]
            invalid = False
            ip = parts[10]
            port = parts[12]

        log = {
            "monat": parts[0],
            "tag": parts[1],
            "zeit": parts[2],
            "host": parts[3],
            "user": user,
            "invalid": invalid,
            "ip": ip,
            "port": port,
            "raw": line.strip()
        }

        logs.append(log)

df = pd.DataFrame(logs)

df1 = df[df["invalid"] == False] 
df2 = df[df["invalid"] == True] 
  
print("Normale User:")
print(df1.head())

print("\nInvalid User:")
print(df2.head())

print(df2["ip"].value_counts())

df1.to_csv("data/normale_user.csv", index=False, encoding="utf-8")
df2.to_csv("data/invalid_user.csv", index=False, encoding="utf-8")