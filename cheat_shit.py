# Étape 1 : Créer une liste des champs déjà couverts par des contrôles
# Control_list contient la liste des contrôles dans le dictionnaire dico
fields_with_controls = set()

for control in Control_liste:
    if control in dico:
        fields_with_controls.update(dico[control])  # Ajouter les champs associés aux contrôles

# Étape 2 : Identifier les champs prioritaires d'après le modèle
# Champs avec un fort Total_Impact_Score selon le modèle
high_impact_fields = fields_features_df[
    fields_features_df['Total_Impact_Score'] > fields_features_df['Total_Impact_Score'].median()
]['Field']

# Étape 3 : Identifier les champs importants qui ne sont pas couverts par des contrôles
fields_missing_controls = [field for field in high_impact_fields if field not in fields_with_controls]

# Étape 4 : Résumer les résultats dans un DataFrame
missing_controls_df = pd.DataFrame({
    'Field': fields_missing_controls,
    'Total_Impact_Score': fields_features_df[
        fields_features_df['Field'].isin(fields_missing_controls)
    ]['Total_Impact_Score']
}).sort_values(by='Total_Impact_Score', ascending=False)

# Afficher les résultats
print("\nChamps de la Loan Tape manquant de contrôles :")
print(missing_controls_df)