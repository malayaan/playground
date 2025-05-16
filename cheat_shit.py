import time
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --- Paramètres globaux ---
period_days = 90  # 3 mois ≈ janvier à mars 2025
interval = "1d"
end_time = int(time.time())
start_time = end_time - (period_days * 24 * 60 * 60)
headers = {"User-Agent": "Mozilla/5.0"}

# --- Indices par secteur ---
sector_indices = {
    "Automotive": {
        "STOXX Europe 600 Auto & Parts": "EXH1.DE",
        "S&P 500 Automobiles & Components": "SP500-40202010",
        "Dow Jones Automobiles & Parts": "^DJUSAP"
    },
    "Energie et Utilities": {
        "STOXX Europe 600 Oil & Gas": "SXEP.DE",
        "S&P 500 Energy": "XLE",
        "S&P 500 Utilities": "XLU",
        "STOXX Europe 600 Utilities": "SX6P.DE"
    },
    "Agroalimentaire": {
        "STOXX Europe 600 Food & Beverage": "SX3P.DE",
        "S&P 500 Consumer Staples": "XLP"
    }
    # Ajoute d’autres secteurs ici si besoin
}

# --- Extraction des données ---
all_dfs = []

for sector, index_dict in sector_indices.items():
    for label, symbol in index_dict.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            timestamps = data['chart']['result'][0]['timestamp']
            closes = data['chart']['result'][0]['indicators']['quote'][0]['close']

            df = pd.DataFrame({'Date': pd.to_datetime(timestamps, unit='s'), label: closes})
            df.set_index("Date", inplace=True)
            all_dfs.append(df)

        except Exception as e:
            print(f"❌ Erreur pour {label} ({symbol}): {e}")

# --- Fusion finale ---
df_combined = pd.concat(all_dfs, axis=1)
df_combined.dropna(how="all", inplace=True)

# --- Affichage test ---
df_combined.plot(figsize=(14, 6), title="Indices sectoriels (janvier–mars 2025)")
plt.grid()
plt.tight_layout()
plt.show()