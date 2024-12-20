# Dictionnaire de mapping des colonnes (exemple Dico)
# Dico : {"col_feature_1": "LoanTape_orig_col_1", "col_feature_2": "LoanTape_orig_col_2", ...}
# À adapter avec votre propre dictionnaire
Dico = {
    "feature_1": "LoanTape_col_1",
    "feature_2": "LoanTape_col_2",
    "control_1": "LoanTape_col_3",
    "control_2": "LoanTape_col_4"
}

# FeaturesNames, ControlNames, AnomalyValues, RiskValues (exemple à adapter avec vos données)
FeaturesNames = ["feature_1", "feature_2"]
ControlNames = ["control_1", "control_2"]
AnomalyValues = [0.8, 0.2]
RiskValues = [0.5, 0.7]

# Étape 1 : Relier les noms des colonnes originelles via le dictionnaire
# Relier FeaturesNames aux colonnes originelles
features_to_controls = {feature: Dico.get(feature, feature) for feature in FeaturesNames}

# Relier ControlNames aux colonnes originelles
controls_to_controls = {control: Dico.get(control, control) for control in ControlNames}

# Étape 2 : Construire les tableaux correspondants
# Table des FeaturesNames et AnomalyValues
features_table = pd.DataFrame({
    "Feature Name": FeaturesNames,
    "Original LoanTape Column": [features_to_controls[feature] for feature in FeaturesNames],
    "Anomaly Value": AnomalyValues
})

# Table des ControlNames et RiskValues
controls_table = pd.DataFrame({
    "Control Name": ControlNames,
    "Original LoanTape Column": [controls_to_controls[control] for control in ControlNames],
    "Risk Value": RiskValues
})

# Étape 3 : Afficher les résultats
print("Features vs Anomaly Values")
print(features_table)

print("\nControls vs Risk Values")
print(controls_table)