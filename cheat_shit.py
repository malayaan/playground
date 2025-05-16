# Symboles regroupés par zone géographique
symbols_by_region = {
    "USA": ["TSLA", "F", "GM"],
    "Japon": ["TM", "HMC", "NSANY", "MZDAY", "FUJHY", "MMTOF", "SZKMY"],
    "Europe": ["STLA", "MBGYY", "BMW.DE", "RACE", "VWAGY", "RNLSY", "VLVLY"],
    "Chine": ["BYDDY", "NIO", "XPEV", "0175.HK"],
    "Corée du Sud": ["HYMTF", "KIMTF"]
}

# Période = 6 ans pour permettre une analyse glissante dès 2020
period_days = 6 * 365
interval = "1d"
end_time = int(time.time())
start_time = end_time - (period_days * 24 * 60 * 60)
headers = {"User-Agent": "Mozilla/5.0"}

region_dfs = {}

# Récupération des données par région
for region, symbols in symbols_by_region.items():
    dfs = []
    for symbol in symbols:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={interval}"
            response = requests.get(url, headers=headers)
            data = response.json()

            timestamps = data['chart']['result'][0]['timestamp']
            closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
            df = pd.DataFrame({"Date": pd.to_datetime(timestamps, unit='s'), symbol: closes})
            df.set_index("Date", inplace=True)
            dfs.append(df)
        except Exception as e:
            print(f"❌ Erreur pour {symbol}: {e}")

    if dfs:
        merged_df = pd.concat(dfs, axis=1)
        region_dfs[region] = merged_df

# Initialisation des résultats
performance_df = pd.DataFrame()
monthly_correlation_trends = {}

for region, df in region_dfs.items():
    df = df.dropna(how="all", axis=1)
    returns = df.pct_change()
    perf = (1 + returns).cumprod()
    performance_df[region] = perf.mean(axis=1)

    # Cohérence intra-zone mois par mois
    monthly_corr = {}
    for date in returns.index.to_period("M").unique():
        df_month = returns[returns.index.to_period("M") == date]
        if df_month.shape[1] > 1 and df_month.shape[0] > 1:
            corr_matrix = df_month.corr()
            # Moyenne des corrélations hors diagonale
            mean_corr = corr_matrix.where(~np.eye(len(corr_matrix), dtype=bool)).stack().mean()
            monthly_corr[date.to_timestamp()] = mean_corr

    monthly_correlation_trends[region] = pd.Series(monthly_corr)

# 📈 Performance par région
performance_df.plot(title="Performance sectorielle - Automobile", figsize=(12, 6))
plt.xlabel("Date")
plt.ylabel("Indice de performance moyen")
plt.grid()
plt.show()

# 📊 Cohérence sectorielle par mois
plt.figure(figsize=(12, 6))
for region, series in monthly_correlation_trends.items():
    plt.plot(series.index, series.values, label=region)

plt.title("Évolution mensuelle de la cohérence sectorielle (corrélation intra-zone)")
plt.xlabel("Date")
plt.ylabel("Corrélation moyenne")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
