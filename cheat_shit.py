import pandas as pd

# Étape 1 : Initialiser les DataFrames avec les index de LoanTape
LongTapeAnomaliesCore = pd.DataFrame(index=loan_tape.index, columns=feature_names)
LongTapeRiskValues = pd.DataFrame(index=loan_tape.index, columns=control_names)

# Étape 2 : Parcourir chaque ligne de LoanTape pour calculer les anomalies et les risques
for idx, row in loan_tape.iterrows():
    # Initialiser les valeurs d'anomalie et de risque pour la ligne courante
    anomalies_row = {}
    risks_row = {}

    # Calculer les anomalies pour chaque feature
    for feature in feature_names:
        # Vérifier si la feature est dans features_to_columns et récupérer les variables associées
        if feature in features_to_columns:
            variables = features_to_columns[feature]
            anomaly_value = 0  # Initialiser l'anomalie à 0
            for variable in variables:
                # Vérifier si la variable est dans la ligne et ajouter sa valeur
                anomaly_value += row[variable] if variable in row else 0
            anomalies_row[feature] = anomaly_value

    # Calculer les risques pour chaque contrôle
    for control in control_names:
        # Vérifier si le contrôle est dans controls_to_columns et récupérer les variables associées
        if control in controls_to_columns:
            variables = controls_to_columns[control]
            risk_value = 0  # Initialiser le risque à 0
            for variable in variables:
                # Vérifier si la variable est dans la ligne et ajouter sa valeur
                risk_value += row[variable] if variable in row else 0
            risks_row[control] = risk_value

    # Ajouter les résultats de la ligne courante aux DataFrames
    LongTapeAnomaliesCore.loc[idx] = anomalies_row
    LongTapeRiskValues.loc[idx] = risks_row

# Étape 3 : Remplir les valeurs manquantes avec 0
LongTapeAnomaliesCore = LongTapeAnomaliesCore.fillna(0)
LongTapeRiskValues = LongTapeRiskValues.fillna(0)

# Étape 4 : Afficher les DataFrames pour vérification
print("LongTapeAnomaliesCore:")
print(LongTapeAnomaliesCore)

print("\nLongTapeRiskValues:")
print(LongTapeRiskValues)