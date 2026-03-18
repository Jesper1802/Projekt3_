import pandas as pd

df1 = pd.read_csv("data/normale_user.csv")

print(df1["ip"].value_counts())

