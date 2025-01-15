import matplotlib.pyplot as plt

# Étape 1 : Créer deux DataFrames séparés pour les champs couverts et non couverts
covered_fields_df = fields_features_df[fields_features_df["Field"].isin(fields_with_controls)]
missing_controls_df = fields_features_df[~fields_features_df["Field"].isin(fields_with_controls)]

# Étape 2 : Créer un graphique pour comparer les deux
plt.figure(figsize=(10, 6))

# Barres pour les champs couverts
plt.bar(
    covered_fields_df["Field"],
    covered_fields_df["Total_Impact_Score"],
    color='black',
    label="Champs couverts par des contrôles"
)

# Barres pour les champs non couverts
plt.bar(
    missing_controls_df["Field"],
    missing_controls_df["Total_Impact_Score"],
    color='red',
    label="Champs non couverts par des contrôles"
)

# Ajustements de la mise en page
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylabel("Total Impact Score")
plt.title("Impact des Champs Couverts vs Non Couverts par des Contrôles", fontsize=14)
plt.legend()
plt.tight_layout()

# Affichage du graphique
plt.show()