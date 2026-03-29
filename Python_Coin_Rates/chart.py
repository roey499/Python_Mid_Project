#load data from db and create chart with pandas
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

conn = sqlite3.connect("USD_ILS.db")
df = pd.read_sql_query("SELECT * FROM USD_ILS", conn)
conn.close()

df = df.sort_values("Date")

sns.set_style("whitegrid")
sns.set(rc={"figure.figsize": (10, 6), "figure.dpi": 120})

# plot
sns.lineplot(data=df, x="Date", y="close_value", marker="o")
plt.xticks(rotation=45)
plt.title("USD to ILS Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Rate")
plt.tight_layout()
plt.show()



