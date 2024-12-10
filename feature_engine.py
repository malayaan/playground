for column in df.columns:
    if pd.api.types.is_numeric_dtype(df[column]):  # Vérifier si la colonne est numérique
        median = df[column].median(skipna=True)  # Calculer la médiane
        df[column] = df[column].fillna(median)   # Remplacer NaN par la médiane
    else:
        # Si non numérique, convertir au type numérique si possible
        try:
            df[column] = pd.to_numeric(df[column], errors='coerce')  # Convertir en numérique
            median = df[column].median(skipna=True)  # Calculer la médiane
            df[column] = df[column].fillna(median)   # Remplacer NaN par la médiane
        except:
            print(f"Colonne '{column}' n'est pas convertible en numérique.")

# Affichage du DataFrame mis à jour
print(df)