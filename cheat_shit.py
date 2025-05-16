import pandas as pd
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Période : Janvier à Mars 2025
start_time = int(time.mktime(datetime(2025, 1, 1).timetuple()))
end_time = int(time.mktime(datetime(2025, 3, 31).timetuple()))
interval = "1d"
headers = {"User-Agent": "Mozilla/5.0"}

# Tickers à récupérer
indices = {
    "S&P 500": "^GSPC",
    "S&P 500 Auto": "^SP500-25",
    "EuroStoxx 50": "^STOXX50E",
    "STOXX Europe 600": "^STOXX"
}
currency_pair = "EURUSD=X"

# Fonction de récupération
def get_yahoo_data(symbol, name):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
    response = requests.get(url, headers=headers)
    data = response.json()
    timestamps = data['chart']['result'][0]['timestamp']
    closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
    df = pd.DataFrame({
        "Date": pd.to_datetime(timestamps, unit='s').floor('D'),
        name: closes
    }).set_index("Date")
    return df

# Récupération des données indices
series = {}
for name, symbol in indices.items():
    try:
        series[name] = get_yahoo_data(symbol, name)
        print(f"✅ {name} récupéré")
    except Exception as e:
        print(f"❌ Erreur pour {name}: {e}")

# Récupération du taux EUR/USD
try:
    fx_df = get_yahoo_data(currency_pair, "EUR/USD")
    print("✅ Taux EUR/USD récupéré")
except Exception as e:
    print(f"❌ Erreur taux de change: {e}")
    fx_df = pd.DataFrame()

# Fusion des indices
df = pd.concat(series.values(), axis=1)
df = df.join(fx_df)  # ajout du taux de change
df = df.groupby(df.index).first()
df = df.sort_index()
df = df.dropna()

# Conversion des indices US en euro
for col in ["S&P 500", "S&P 500 Auto"]:
    df[col] = df[col] / df["EUR/USD"]

df = df.drop(columns=["EUR/USD"])

# Base 100
df_base100 = df / df.iloc[0] * 100

# Affichage
df_base100.plot(figsize=(12, 6), title="Indices (Base 100, convertis en EUR) - Janv à Mars 2025")
plt.grid()
plt.tight_layout()
plt.show()

# Export Excel
excel_path = "/mnt/data/indices_base100_euro.xlsx"
with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    for col in df_base100.columns:
        df_base100[[col]].to_excel(writer, sheet_name=col[:31])

print(f"✅ Export Excel terminé : {excel_path}")