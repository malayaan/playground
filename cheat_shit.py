import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

# Dictionnaire des indices sectoriels avec leurs symboles
sector_indices = {
    "Technologie": "^IXT",
    "Énergie": "^GSPE",
    "Matériaux": "^IXB",
    "Industrie": "^IXI",
    "Services financiers": "^IXM",
    "Santé": "^HCX",
    "Consommation discrétionnaire": "^IXY",
    "Consommation de base": "^IXR",
    "Services de communication": "^IXC",
    "Services publics": "^IXU",
    "Immobilier": "^IXRE"
}

period_days = 6 * 365  # 6 ans
interval = "1d"
end_time = int(time.time())
start_time = end_time - (period_days * 24 * 60 * 60)
headers = {"User-Agent": "Mozilla/5.0"}

all_dfs = []

for sector, symbol in sector_indices.items():
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
        response = requests.get(url, headers=headers)
        data = response.json()

        timestamps = data['chart']['result'][0]['timestamp']
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
        df = pd.DataFrame({
            "Date": pd.to_datetime(timestamps, unit='s'),
            sector: closes
        }).set_index("Date")
        returns = df[sector].pct_change()
        perf = (1 + returns).cumprod()
        perf = perf / perf.dropna().iloc[0]
        df[sector] = perf
        all_dfs.append(df)

    except Exception as e:
        print(f"❌ Erreur pour {sector} ({symbol}): {e}")

# Fusion
if all_dfs:
    combined_df = pd.concat(all_dfs, axis=1).dropna()

    # Calcul de la moyenne
    combined_df["Moyenne"] = combined_df.mean(axis=1)

    # Affichage
    plt.figure(figsize=(14, 8))
    for col in combined_df.columns:
        if col == "Moyenne":
            plt.plot(combined_df.index, combined_df[col], label=col, linewidth=2.5, linestyle='--', color='black')
        else:
            plt.plot(combined_df.index, combined_df[col], label=col)

    plt.title("Performance comparée des indices sectoriels")
    plt.xlabel("Date")
    plt.ylabel("Performance (base 1)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()