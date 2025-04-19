%% [markdown]

"""

Analyse dynamique des corrélations intersectorielles

Ce notebook a pour objectif d'étudier les corrélations entre les performances des différents secteurs économiques à partir d'indices sectoriels européens (STOXX Europe 600). L'idée est de produire :

Une matrice de corrélation sur l'ensemble de la période (ex. 2010–2024)

Des matrices de corrélations glissantes pour visualiser l'évolution des dépendances sectorielles dans le temps


Cela permet notamment de détecter des périodes de synchronisation (crises, cycles) ou de divergence structurelle. """

%%

import yfinance as yf import pandas as pd import matplotlib.pyplot as plt import seaborn as sns

%% [markdown]

"""

1. Chargement des données sectorielles STOXX Europe 600

On télécharge les données depuis Yahoo Finance pour une quinzaine de secteurs, depuis 2010 si possible. """

%%

symbols = { 'Automobile': '^STOXXAP', 'Construction': '^STOXXOP', 'Matériaux': '^STOXXPP', 'Industrie': '^STOXXNP', 'Énergie': '^STOXXEP', 'Finances': '^STOXXFP', 'Immobilier': '^STOXX86P', 'Santé': '^STOXXDP', 'Technologie': '^STOXX8P', 'Télécoms': '^STOXXKP', 'Services publics': '^STOXX6P', 'Conso discrétionnaire': '^STOXXQP', 'Conso de base': '^STOXX3P', 'Médias': '^STOXXMP', 'Voyages & Loisirs': '^STOXXTP' }

%%

raw_data = yf.download(list(symbols.values()), start="2010-01-01", end="2024-12-31")['Adj Close'] data = raw_data.rename(columns={v: k for k, v in symbols.items()}) data = data.dropna(axis=1, how='any')  # retire les colonnes incomplètes

%% [markdown]

"""

2. Visualisation de la matrice de corrélation globale (2010–2024)

"""

%%

weekly_returns = data.resample('W').last().pct_change().dropna() corr_matrix_full = weekly_returns.corr()

plt.figure(figsize=(14, 10)) sns.heatmap(corr_matrix_full, annot=True, cmap='coolwarm', center=0) plt.title("Matrice de corrélation intersectorielle (2010–2024)") plt.show()

%% [markdown]

"""

3. Corrélations glissantes dans le temps (exemple : Automobile vs Énergie)

"""

%%

rolling_corr = weekly_returns['Automobile'].rolling(52).corr(weekly_returns['Énergie'])

plt.figure(figsize=(12, 5)) rolling_corr.plot() plt.title("Corrélation glissante (1 an) – Automobile vs Énergie") plt.ylabel("Corrélation") plt.grid(True) plt.show()

%% [markdown]

"""

4. Construction d'une série de matrices de corrélation annuelles

Permet de voir l'évolution structurelle des corrélations intersectorielles année par année. """

%%

matrices = {} for year in range(2012, 2024): yearly = weekly_returns[str(year)] corr = yearly.corr() matrices[year] = corr

%% [markdown]

"""

5. Visualisation d'exemples d'années clés (ex : Covid, inflation, guerre en Ukraine)

"""

%%

fig, axes = plt.subplots(2, 2, figsize=(16, 12)) years_to_plot = [2019, 2020, 2022, 2023] for ax, year in zip(axes.flat, years_to_plot): sns.heatmap(matrices[year], ax=ax, cmap='coolwarm', center=0, annot=False) ax.set_title(f"Corrélations intersectorielles – {year}")

plt.tight_layout() plt.show()

