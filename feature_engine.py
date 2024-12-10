import pandas as pd
import numpy as np

# Exemple de DataFrame
data = {
    'col1': [1, 2, 2, 4, 5],  # Numérique
    'col2': ['A', 'B', 'A', 'C', 'C'],  # Catégorielle
    'col3': ['X', np.nan, 'Y', 'X', 'Z'],  # Catégorielle
    'col4': [1.1, 2.2, 3.3, 4.4, 5.5],  # Numérique
    'col5': ['A', 'A', 'B', 'B', 'C'],  # Catégorielle
}
df = pd.DataFrame(data)

# Définir les colonnes catégorielles en fonction de nunique
categorical_columns = [col for col in df.columns if df[col].nunique() < 30]

# Afficher les colonnes catégorielles détectées
print("Colonnes catégorielles détectées :")
print(categorical_columns)

# Exemple : traitement des colonnes catégorielles détectées
for column in categorical_columns:
    print(f"Colonne '{column}' : {df[column].unique()}")
