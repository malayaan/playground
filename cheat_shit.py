# %% [markdown]
"""
# Analyse de la propagation d'une crise sectorielle à la Société Générale

Ce notebook présente une méthodologie concrète pour simuler et analyser la propagation potentielle d'une crise initiée dans un secteur spécifique (ici, le secteur automobile) au sein du portefeuille client de la Société Générale. L'objectif est d'identifier à partir de quel seuil initial une crise locale peut potentiellement devenir systémique à travers différents secteurs économiques interconnectés.

## Hypothèses principales :

- Chaque client appartient à un secteur économique clairement identifié.
- Les interactions entre clients sont représentées par des transactions financières.
- Une matrice de corrélation intersectorielle est utilisée pour modéliser les liens économiques positifs et négatifs.
- Un client entre en crise sous l'effet direct (transactions) ou indirect (corrélation sectorielle) d'autres clients déjà en crise.
"""

# %%
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
"""
## 1. Génération des données fictives et matrice de corrélation sectorielle

La matrice de corrélation contient des valeurs positives et négatives, reflétant ainsi la réalité économique : certains secteurs bénéficient de la baisse d'autres secteurs.
"""

# %%
secteurs = ["Automobile", "BTP", "Énergie", "Transport", "Distribution", "Tech", "Finance"]

np.random.seed(42)
corr_matrix = np.random.uniform(-1, 1, (len(secteurs), len(secteurs)))
np.fill_diagonal(corr_matrix, 1)
corr_matrix = (corr_matrix + corr_matrix.T) / 2

df_corr = pd.DataFrame(corr_matrix, index=secteurs, columns=secteurs)

plt.figure(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap="coolwarm")
plt.title('Matrice de Corrélation Intersectorielle')
plt.show()

# %% [markdown]
"""
## 2. Création du réseau de transactions

Nous simulons 2000 transactions entre clients internes et externes à la Société Générale. Les clients internes ont un secteur connu, les externes ont une origine ou destination inconnue (secteur indéterminé).
"""

# %%
nb_transactions = 2000
transactions = pd.DataFrame({
    "source_id": np.random.randint(1, 500, nb_transactions),
    "target_id": np.random.randint(501, 1000, nb_transactions),
    "amount": np.round(np.random.uniform(100, 50000, nb_transactions), 2),
    "source_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]),
    "target_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]),
})

transactions["source_sector"] = np.where(transactions["source_internal"],
                                         np.random.choice(secteurs, nb_transactions), None)
transactions["target_sector"] = np.where(transactions["target_internal"],
                                         np.random.choice(