# Étape 1 : Identifier les champs peu impactants selon le modèle
low_impact_fields = fields_features_df[fields_features_df['Total_Impact_Score'] < fields_features_df['Total_Impact_Score'].median()]

# Étape 2 : Identifier les contrôles associés à ces champs via le dictionnaire
low_impact_controls = []

for control, fields in dico.items():
    # Vérifier si le contrôle est lié à un champ peu impactant
    if any(field in low_impact_fields['Field'].values for field in fields):
        total_control_impact = fields_controls_df.loc[
            fields_controls_df['Field'].isin(fields), 'Total_Impact_Score'
        ].sum()
        low_impact_controls.append({
            'Control': control,
            'Fields': fields,
            'Control_Impact_Score': total_control_impact
        })

# Étape 3 : Créer un DataFrame pour analyser les contrôles peu impactants
low_impact_controls_df = pd.DataFrame(low_impact_controls)

# Trier par score d’impact des contrôles
low_impact_controls_df = low_impact_controls_df.sort_values(by='Control_Impact_Score', ascending=True)

# Afficher les 10 contrôles les moins impactants
print("\nTop 10 Contrôles Peu Impactants :")
print(low_impact_controls_df.head(10))