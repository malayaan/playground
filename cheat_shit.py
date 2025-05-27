import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_yahoo_data(symbol, interval="1d", years_back=5):
    end_time = int(time.time())
    start_time = end_time - years_back * 365 * 24 * 60 * 60
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    data = response.json()

    try:
        timestamps = data['chart']['result'][0]['timestamp']
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
        df = pd.DataFrame({
            "Date": pd.to_datetime(timestamps, unit='s'),
            symbol: closes
        })
        df.set_index("Date", inplace=True)
        return df
    except Exception as e:
        print(f"Erreur pour {symbol}: {e}")
        return pd.DataFrame()

# Récupération des données
vix_df = get_yahoo_data("^VIX")
vstoxx_df = get_yahoo_data("^V2TX")  # VSTOXX

# Fusion
combined = pd.concat([vix_df, vstoxx_df], axis=1).dropna()

# Tracé
plt.figure(figsize=(14, 6))
plt.plot(combined.index, combined["^VIX"], label="VIX (US)")
plt.plot(combined.index, combined["^V2TX"], label="VSTOXX (EU)")
plt.title("Indices de volatilité - VIX & VSTOXX (5 ans)")
plt.xlabel("Date")
plt.ylabel("Volatilité")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()