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

import numpy as np import pandas as pd import networkx as nx import matplotlib.pyplot as plt import seaborn as sns

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

def simulate_crisis(transactions, df_corr, secteurs, initial_sector, initial_crisis_pct, propagation_rounds=3): clients = pd.unique(transactions[['source_id', 'target_id']].values.ravel()) client_sectors = {}

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

return len(crisis_clients) / len(clients)

%% [markdown]

"""

4. Analyse des résultats

Nous simulons la crise pour différentes proportions initiales de clients du secteur automobile en crise, puis nous analysons la proportion finale du groupe affectée par la crise. Cela permet de visualiser un éventuel point de bascule à partir duquel la crise devient systémique. """

%%

initial_pcts = np.linspace(0.05, 0.5, 10) final_affected_pcts = [simulate_crisis(transactions, df_corr, secteurs, "Automobile", pct) for pct in initial_pcts]

plt.figure(figsize=(10, 6)) plt.plot(initial_pcts * 100, np.array(final_affected_pcts) * 100, marker='o') plt.xlabel('Pourcentage initial du secteur Automobile en crise (%)') plt.ylabel('Pourcentage final du groupe affecté (%)') plt.title('Propagation de la crise en fonction du secteur automobile initialement affecté') plt.grid(True) plt.show()

%% [markdown]

"""

5. Limites et perspectives

Limites :

Transactions externes manquantes (sous-estimation des liens réels).

Simplification des interactions économiques complexes à de simples transactions.

L'effet aléatoire est arbitraire et pourrait être amélioré par une étude approfondie.


Perspectives :

Compléter par des données externes (Banque de France, INSEE).

Ajuster la matrice de corrélation avec des analyses sectorielles réelles.

Affiner la modélisation de l'incertitude et des mécanismes de propagation.

Étendre l’analyse à d'autres secteurs pour établir une cartographie comparative des effets systémiques potentiels. """



