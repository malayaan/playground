# Étape 1 : Identifier les features associées aux champs manquant de contrôles
# Dico contient les associations entre features et les champs de la LT
missing_fields = list(missing_controls_df['Field'])  # Champs manquant de contrôles
features_associated = []

for feature, fields in dico.items():
    if any(field in missing_fields for field in fields):
        features_associated.append(feature)

# Filtrer les features problématiques
features_associated = list(set(features_associated))  # Supprimer les doublons

print("\nFeatures associées aux champs manquant de contrôles :")
print(features_associated)

# Étape 2 : Analyser les valeurs extrêmes dans la table de features
# Supposons que 'features_csv' contient les valeurs des features pour chaque ligne
features_problematic = features_csv[features_associated]

# Calculer les quantiles pour détecter les valeurs extrêmes
quantiles = features_problematic.quantile([0.01, 0.99])

# Identifier les lignes avec des valeurs extrêmes (en dehors des quantiles 1% et 99%)
extreme_rows = features_problematic[
    (features_problematic < quantiles.loc[0.01]) | (features_problematic > quantiles.loc[0.99])
].dropna(how='all')  # Garder uniquement les lignes ayant des valeurs extrêmes

# Étape 3 : Classer les lignes selon le nombre de valeurs extrêmes
extreme_rows['Extreme_Count'] = extreme_rows.notna().sum(axis=1)  # Compter les features extrêmes par ligne
top_5_extreme_rows = extreme_rows.sort_values(by='Extreme_Count', ascending=False).head(5)

# Étape 4 : Afficher les résultats
# Filtrer pour montrer uniquement les features problématiques pour chaque ligne
for index, row in top_5_extreme_rows.iterrows():
    problematic_features = row.dropna().index.tolist()  # Features problématiques pour cette ligne
    print(f"\nLigne {index} :")
    print(features_csv.loc[index, problematic_features])