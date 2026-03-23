import pandas as pd

df1 = pd.read_csv("data/normale_user.csv")
df2 = pd.read_csv("data/invalid_user.csv")

df3 = pd.concat([df1, df2], ignore_index=True)


print(df3["monat"].value_counts()) 

