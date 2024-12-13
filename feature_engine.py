import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Exemple :
# Supposons que nous ayons un DataFrame `df` qui contient déjà les données.
# Les colonnes choisies sont un exemple. Adaptez en fonction de vos données réelles.
# "montant", "duree", "taux" sont des variables numériques.
# "indicateur_regle1", "indicateur_regle2" sont des booléens issus des contrôles actuels.
# Dans le cadre réel, remplacez par les features pertinentes disponibles.

# Sélection des features pertinentes
relevant_features = ["montant", "duree", "taux", "indicateur_regle1", "indicateur_regle2"]

# Extraction des données
X = df[relevant_features].copy()

# Convertir les indicateurs booléens en entiers (0/1) si nécessaire
bool_cols = ["indicateur_regle1", "indicateur_regle2"]
for col in bool_cols:
    X[col] = X[col].astype(int)

# Normalisation/Standardisation des données pour éviter les problèmes d'échelle
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Paramétrage de l'Isolation Forest
# On définit un taux de contamination un peu élevé (5% ici), compte tenu de la faible qualité globale
contamination_rate = 0.05
iso_forest = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)

# Entraînement du modèle sur l'ensemble des données
iso_forest.fit(X_scaled)

# Récupération des scores d'anomalie
# decision_function renvoie un score : plus il est faible, plus l'observation est considérée anormale
anomaly_scores = iso_forest.decision_function(X_scaled)

# Prédiction finale (-1 = anomalie, 1 = normal)
anomalies = iso_forest.predict(X_scaled)

# Ajout des résultats au DataFrame original
df["anomaly_score"] = anomaly_scores
df["anomaly_label"] = anomalies

# Tri des données par score d'anomalie (ascending=True pour avoir les plus anormales en haut)
df_sorted = df.sort_values(by="anomaly_score", ascending=True)

# Sélection d'un échantillon des cas les plus extrêmes pour inspection manuelle
top_anomalies = df_sorted.head(10)
print("Exemples d'anomalies les plus marquées :")
print(top_anomalies[relevant_features + ["anomaly_score", "anomaly_label"]])

# Visualisation de la distribution des scores d'anomalie (optionnel)
plt.hist(df["anomaly_score"], bins=50)
plt.title("Distribution des scores d'anomalie")
plt.xlabel("Score d'anomalie")
plt.ylabel("Fréquence")
plt.show()

# Étapes suivantes :
# - Présenter au métier quelques-unes de ces anomalies (top_anomalies) pour un retour qualitatif.
# - Vérifier si ces anomalies correspondent à des problèmes connus (montants incohérents, champs manquants, etc.).
# - Ajuster si besoin le paramètre 'contamination' ou tester d'autres algorithmes (LOF, DBSCAN).
# - Une fois la métrique globale (pondération métiers) disponible, utiliser celle-ci pour filtrer
#   ou prioriser les anomalies détectées et ainsi améliorer la pertinence de la détection.
