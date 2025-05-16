import pandas as pd
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Dates de janvier à mars 2025 en timestamp Unix
start_time = int(time.mktime(datetime(2025, 1, 1).timetuple()))
end_time = int(time.mktime(datetime(2025, 3, 31).timetuple()))
interval = "1d"
headers = {"User-Agent": "Mozilla/5.0"}

# Dictionnaire sectoriel : nom lisible -> ticker Yahoo Finance
sector_indices = {
    "Agroalimentaire": {
        "STOXX Europe 600 Food & Beverage": "^STOXX600F&B",
        "Euronext Food & Beverage Index": "^FBEURONEXT",
        "S&P 500 Consumer Staples": "^SP500-30",
        "NASDAQ Consumer Staples": "^IXY"
    },
    "Automobile": {
        "STOXX Europe 600 Automobiles & Parts": "SXAP.SW",
        "S&P 500 Automobiles & Components": "^SP500-25",
        "Dow Jones Automobiles & Parts": "DJUSAP"
    },
    "Énergie & Utilities": {
        "STOXX Europe 600 Oil & Gas": "SXEP.SW",
        "S&P 500 Energy": "^SP500-10",
        "S&P 500 Utilities": "^SP500-55",
        "STOXX Europe 600 Utilities": "SX6P.SW"
    },
    "Industries Manufacturières": {
        "STOXX Europe 600 Industrial Goods & Services": "SXNP.SW",
        "STOXX Europe 600 Chemicals": "SX4P.SW",
        "FTSE 350 Industrial Metals & Mining": "^FT350IMM",
        "S&P 500 Industrials": "^SP500-20",
        "Dow Jones U.S. Basic Materials": "DJUSBM"
    },
    "Technologies & Médias": {
        "STOXX Europe 600 Technology": "SX8P.SW",
        "STOXX Europe 600 Telecommunications": "SXKP.SW",
        "FTSE TechMARK 100": "^FTTM100",
        "NASDAQ Composite": "^IXIC",
        "S&P 500 Information Technology": "^SP500-45",
        "Dow Jones U.S. Telecommunications": "DJUSTL"
    },
    "Santé": {
        "STOXX Europe 600 Health Care": "SXDP.SW",
        "FTSE 350 Pharmaceuticals & Biotechnology": "^FT350PB",
        "S&P 500 Health Care": "^SP500-35",
        "NASDAQ Biotechnology": "^NBI"
    },
    "Transport": {
        "FTSE 350 Industrial Transportation": "^FT350IT",
        "Dow Jones Transportation Average": "^DJT"
    },
    "Distribution & Consommation": {
        "STOXX Europe 600 Retail": "SXRP.SW",
        "FTSE 100 Consumer Discretionary": "^FT100CD",
        "S&P 500 Consumer Discretionary": "^SP500-25",
        "NASDAQ Retail Trade Index": "^RETAIL"
    },
    "Construction & Matériaux": {
        "STOXX Europe 600 Construction & Materials": "SXOP.SW",
        "S&P 500 Materials": "^SP500-15",
        "Dow Jones U.S. Construction & Materials": "DJUSCN"
    }
}

# Récupération
all_series = {}
for sector, indices in sector_indices.items():
    for name, symbol in indices.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
            response = requests.get(url, headers=headers)
            data = response.json()

            timestamps = data['chart']['result'][0]['timestamp']
            closes = data['chart']['result'][0]['indicators']['quote'][0]['close']

            df = pd.DataFrame({
                "Date": pd.to_datetime(timestamps, unit='s'),
                f"{sector} - {name}": closes
            }).set_index("Date")

            all_series[f"{sector} - {name}"] = df
            print(f"✅ {name} téléchargé")
        except Exception as e:
            print(f"❌ Erreur pour {name} ({symbol}): {e}")

# Fusion
df_all = pd.concat(all_series.values(), axis=1)
df_all = df_all.sort_index()
df_all.to_csv("indices_sectoriels_janv_mars_2025.csv")
print("✅ Export terminé")

# Exemple d’affichage
df_all.plot(figsize=(16, 8), title="Indices sectoriels - Janv à Mars 2025")
plt.grid()
plt.tight_layout()
plt.show()