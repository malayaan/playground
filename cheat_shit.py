import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dictionnaire des ETF sectoriels
etf_symbols = {
    'Automobile': 'EXV1.DE',
    'Banques': 'EXH1.DE',
    'Services Financiers': 'EXH2.DE',
    'Santé': 'EXH3.DE',
    'Industrie': 'EXH4.DE',
    'Technologie': 'EXH5.DE'
}

# Téléchargement des données
data = yf.download(list(etf_symbols.values()), start="2010-01-01", end="2024-12-31")['Adj Close']
data.columns = etf_symbols.keys()

# Calcul des rendements hebdomadaires
weekly_returns = data.resample('W').last().pct_change().dropna()

# Matrice de corrélation
corr_matrix = weekly_returns.corr()

# Affichage de la heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Matrice de corrélation intersectorielle basée sur les ETF (2010–2024)")
plt.show()