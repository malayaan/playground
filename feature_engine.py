# Étape 1 : Préparer les données pour les variables
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

# Afficher le DataFrame pour vérification
print("Features Variables DataFrame:")
print(features_variables)