import numpy as np import pandas as pd import networkx as nx import matplotlib.pyplot as plt import seaborn as sns

Définition des secteurs

secteurs = ["Automobile", "BTP", "Énergie", "Transport", "Distribution", "Tech", "Finance"]

Création matrice de corrélation intersectorielle fictive

np.random.seed(42) corr_matrix = np.random.uniform(low=0.1, high=1.0, size=(len(secteurs), len(secteurs))) np.fill_diagonal(corr_matrix, 1) corr_matrix = (corr_matrix + corr_matrix.T) / 2 df_corr = pd.DataFrame(corr_matrix, index=secteurs, columns=secteurs)

Base fictive de transactions

nb_transactions = 2000 transactions = pd.DataFrame({ "source_id": np.random.randint(1, 500, nb_transactions), "target_id": np.random.randint(501, 1000, nb_transactions), "amount": np.round(np.random.uniform(100, 50000, nb_transactions), 2), "source_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]), "target_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]), })

transactions["source_sector"] = np.where(transactions["source_internal"], np.random.choice(secteurs, nb_transactions), None)

transactions["target_sector"] = np.where(transactions["target_internal"], np.random.choice(secteurs, nb_transactions), None)

Construction du graphe pondéré

G = nx.Graph()

Ajout des nœuds

for idx, row in transactions.iterrows(): G.add_node(row["source_id"], sector=row["source_sector"]) G.add_node(row["target_id"], sector=row["target_sector"])

Ajout des liens avec vérification explicite des secteurs

for idx, row in transactions.iterrows(): poids = row["amount"] / 1000 if row["source_sector"] in secteurs and row["target_sector"] in secteurs: poids *= df_corr.loc[row["source_sector"], row["target_sector"]] G.add_edge(row["source_id"], row["target_id"], weight=poids)

Visualisation des résultats

fig, axes = plt.subplots(1, 2, figsize=(20, 8))

Matrice de corrélation

sns.heatmap(df_corr, annot=True, cmap="coolwarm", ax=axes[0]) axes[0].set_title('Matrice de Corrélation Intersectorielle')

Graphe simplifié

pos = nx.spring_layout(G, k=0.15, seed=42) nx.draw(G, pos, ax=axes[1], node_size=10, edge_color='grey', alpha=0.5) axes[1].set_title('Graphe des Transactions Pondérées')

plt.tight_layout() plt.show()

