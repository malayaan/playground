import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dictionnaire des ETF sectoriels
etf_symbols = {
    'Automobile': 'EXV1.DE',
    'Banques': 'EXH1.DE',
    'Services Financiers': 'EXH2.DE',
    'Alimentation & Boissons': 'EXH3.DE',
    'Santé': 'EXH4.DE',
    'Assurances': 'EXH5.DE',
    'Biens Industriels': 'EXH6.DE',
    'Pétrole & Gaz': 'EXH7.DE',
    'Distribution': 'EXH8.DE',
    'Services Publics': 'EXH9.DE'
}

# Téléchargement des données
data = yf.download(list(etf_symbols.values()), start="2010-01-01", end="2024-12-31")['Adj Close']
data.columns = etf_symbols.keys()

# Calcul des rendements hebdomadaires
weekly_returns = data.resample('W').last().pct_change().dropna()

# Matrice de corrélation
corr_matrix = weekly_returns.corr()

# Affichage de la heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Matrice de corrélation intersectorielle basée sur les ETF (2010–2024)")
plt.show()