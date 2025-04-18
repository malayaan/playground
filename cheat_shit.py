%% [markdown]

"""

Analyse de la propagation d'une crise sectorielle à la Société Générale

Ce notebook présente une méthodologie concrète pour simuler et analyser la propagation potentielle d'une crise initiée dans un secteur spécifique (ici, le secteur automobile) au sein du portefeuille client de la Société Générale. L'objectif est d'identifier à partir de quel seuil initial une crise locale peut potentiellement devenir systémique à travers différents secteurs économiques interconnectés.

Hypothèses principales :

Chaque client appartient à un secteur économique clairement identifié.

Les interactions entre clients sont représentées par des transactions financières.

Une matrice de corrélation intersectorielle est utilisée pour modéliser les liens économiques positifs et négatifs.

Un client entre en crise sous l'effet direct (transactions) ou indirect (corrélation sectorielle) d'autres clients déjà en crise. """


%%

import numpy as np import pandas as pd import networkx as nx import matplotlib.pyplot as plt import seaborn as sns import time from IPython.display import clear_output

%% [markdown]

"""

1. Génération des données fictives et matrice de corrélation sectorielle

La matrice de corrélation contient des valeurs positives et négatives, reflétant ainsi la réalité économique : certains secteurs bénéficient de la baisse d'autres secteurs. """

%%

secteurs = ["Automobile", "BTP", "Énergie", "Transport", "Distribution", "Tech", "Finance"]

np.random.seed(42) corr_matrix = np.random.uniform(-1, 1, (len(secteurs), len(secteurs))) np.fill_diagonal(corr_matrix, 1) corr_matrix = (corr_matrix + corr_matrix.T) / 2

df_corr = pd.DataFrame(corr_matrix, index=secteurs, columns=secteurs)

plt.figure(figsize=(8, 6)) sns.heatmap(df_corr, annot=True, cmap="coolwarm") plt.title('Matrice de Corrélation Intersectorielle') plt.show()

%% [markdown]

"""

2. Création du réseau de transactions

Nous simulons 2000 transactions entre clients internes et externes à la Société Générale. Les clients internes ont un secteur connu, les externes ont une origine ou destination inconnue (secteur indéterminé). """

%%

nb_transactions = 2000 transactions = pd.DataFrame({ "source_id": np.random.randint(1, 500, nb_transactions), "target_id": np.random.randint(501, 1000, nb_transactions), "amount": np.round(np.random.uniform(100, 50000, nb_transactions), 2), "source_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]), "target_internal": np.random.choice([True, False], nb_transactions, p=[0.7, 0.3]), })

transactions["source_sector"] = np.where(transactions["source_internal"], np.random.choice(secteurs, nb_transactions), None) transactions["target_sector"] = np.where(transactions["target_internal"], np.random.choice(secteurs, nb_transactions), None)

%% [markdown]

"""

3. Simulation de la propagation d'une crise

Nous définissons une fonction claire qui simule la propagation d'une crise initialisée dans le secteur automobile. La propagation dépend :

Des transactions entre clients

Des corrélations intersectorielles

D'un facteur aléatoire modéré pour simuler l'incertitude réelle


Le modèle repose sur un nombre de cycles de propagation simulés, chacun évaluant les effets d'une propagation indirecte ou d'un choc corrélé. """

%%

def simulate_crisis_and_return_nodes(transactions, df_corr, secteurs, initial_sector, initial_crisis_pct, propagation_rounds=3): clients = pd.unique(transactions[['source_id', 'target_id']].values.ravel()) client_sectors = {}

for _, row in transactions.iterrows():
    if row["source_sector"]:
        client_sectors[row["source_id"]] = row["source_sector"]
    if row["target_sector"]:
        client_sectors[row["target_id"]] = row["target_sector"]

crisis_clients = set(np.random.choice(
    [client for client, sector in client_sectors.items() if sector == initial_sector],
    size=int(len([c for c in client_sectors.values() if c == initial_sector]) * initial_crisis_pct),
    replace=False
))

for _ in range(propagation_rounds):
    new_crisis_clients = set()
    for _, row in transactions.iterrows():
        if row["source_id"] in crisis_clients and row["target_id"] not in crisis_clients:
            sector_source = client_sectors.get(row["source_id"])
            sector_target = client_sectors.get(row["target_id"])
            correlation = df_corr.loc[sector_source, sector_target] if sector_source and sector_target else 0

            proba_crisis = 0.1 + (0.4 * correlation) + np.random.uniform(-0.05, 0.05)
            if proba_crisis > 0.2:
                new_crisis_clients.add(row["target_id"])

    crisis_clients.update(new_crisis_clients)

return crisis_clients, client_sectors

%% [markdown]

"""

4. Affichage dynamique de la propagation

Nous affichons de manière dynamique l’évolution de la propagation d’une crise sectorielle à différents niveaux d’activation initiale du secteur automobile. Chaque état est visible quelques secondes, permettant d’apprécier la contagion progressive dans le réseau. """

%%

G = nx.Graph() for _, row in transactions.iterrows(): G.add_node(row["source_id"]) G.add_node(row["target_id"]) poids = row["amount"] / 1000 if row["source_sector"] in secteurs and row["target_sector"] in secteurs: poids *= df_corr.loc[row["source_sector"], row["target_sector"]] G.add_edge(row["source_id"], row["target_id"], weight=poids)

pos = nx.spring_layout(G, k=0.15, seed=42)

delays = np.linspace(2, 10, 10) initial_pcts = np.linspace(0.05, 0.5, 10)

for i, pct in enumerate(initial_pcts): crisis_nodes, client_sectors = simulate_crisis_and_return_nodes(transactions, df_corr, secteurs, "Automobile", pct) node_colors = ['red' if node in crisis_nodes else 'lightgrey' for node in G.nodes()]

plt.figure(figsize=(10, 6))
nx.draw(G, pos, node_color=node_colors, edge_color='lightgrey', node_size=15, alpha=0.6)
plt.title(f"Propagation - {int(pct * 100)}% initialement en crise (Automobile)")
plt.show()
time.sleep(delays[i])

