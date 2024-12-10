import pandas as pd

# Exemple de DataFrame
data = {
    'col1': [1, 2, None, 'N/A', 5],
    'col2': ['N/A', 3, None, 4, 5],
    'col3': [None, 'N/A', 3, 4, None]
}
df = pd.DataFrame(data)

# Listes des valeurs à traiter
missing_values = [None, float('nan')]
not_applicable_values = ['N/A']

# Boucle sur les colonnes
for column in df.columns:
    # Nom de la colonne flag
    flag_column_name = f"quality_flag_{column}"
    
    # Création de la colonne flag
    df[flag_column_name] = df[column].apply(
        lambda x: -1 if x in missing_values else (1 if x in not_applicable_values else 0)
    )

# Affichage du DataFrame mis à jour
print(df)
