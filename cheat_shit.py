import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Étape 1 : Préparer les données pour les variables (features)
# Initialiser un dictionnaire pour stocker la somme des anomalies pour chaque variable
variable_anomaly_sums = {}

# Parcourir chaque feature et ses variables associées
for feature, variables in features_to_columns.items():
    # Vérifier que la feature est dans le DataFrame Features
    if feature in features["Feature Name"].values:
        # Récupérer l'Anomaly Value associée à cette feature
        anomaly_value = features.loc[features["Feature Name"] == feature, "Anomaly Value"].values[0]
        
        # Ajouter cette valeur d'anomalie à chaque variable impliquée
        for variable in variables:
            if variable not in variable_anomaly_sums:
                variable_anomaly_sums[variable] = 0  # Initialiser la somme si la variable n'existe pas
            variable_anomaly_sums[variable] += anomaly_value

# Étape 2 : Construire le DataFrame FeaturesVariables
features_variables = pd.DataFrame({
    "Variable": list(variable_anomaly_sums.keys()),
    "Anomaly Value": list(variable_anomaly_sums.values())
})

# Étape 3 : Préparer les données pour les variables (contrôles)
# Initialiser un dictionnaire pour stocker la somme des risques pour chaque variable
variable_risk_sums = {}

# Parcourir chaque contrôle et ses variables associées
for control, variables in controls_to_columns.items():
    # Vérifier que le contrôle est dans le DataFrame Controls
    if control in controls["Control Name"].values:
        # Récupérer le Risk Value associée à ce contrôle
        risk_value = controls.loc[controls["Control Name"] == control, "Risk Value"].values[0]
        
        # Ajouter cette valeur de risque à chaque variable impliquée
        for variable in variables:
            if variable not in variable_risk_sums:
                variable_risk_sums[variable] = 0  # Initialiser la somme si la variable n'existe pas
            variable_risk_sums[variable] += risk_value

# Étape 4 : Construire le DataFrame ControlsVariables
controls_variables = pd.DataFrame({
    "Variable": list(variable_risk_sums.keys()),
    "Risk Value": list(variable_risk_sums.values())
})

# Étape 5 : Fusionner les deux DataFrames pour un affichage sur le même graphique
merged_data = pd.merge(
    features_variables.sort_values(by="Anomaly Value", ascending=False),
    controls_variables.sort_values(by="Risk Value", ascending=False),
    on="Variable",
    how="outer"
).fillna(0)  # Remplir les valeurs manquantes avec 0 si une variable n'apparaît que dans l'un des deux

# Étape 6 : Tracer le graphique
x = np.arange(len(merged_data["Variable"]))  # Positions des groupes
width = 0.35  # Largeur des barres

fig, ax = plt.subplots(figsize=(12, 7))

# Barres pour les anomalies (features)
bar_anomaly = ax.bar(x - width/2, merged_data["Anomaly Value"], width, label='Anomalies (Features)', color='red', alpha=0.7)

# Barres pour les risques (contrôles)
bar_risk = ax.bar(x + width/2, merged_data["Risk Value"], width, label='Risques (Controls)', color='black', alpha=0.7)

# Ajouter des labels et une légende
ax.set_ylabel('Valeurs')
ax.set_title("Comparaison des anomalies et des risques par variable")
ax.set_xticks(x)
ax.set_xticklabels(merged_data["Variable"], rotation=45, ha='right')
ax.legend()

# Ajuster la mise en page
plt.tight_layout()

# Afficher le graphique
plt.show()