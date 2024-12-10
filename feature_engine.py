def clean_dataframe(df, cleaning_dict):
    """
    Nettoie le DataFrame en remplaçant les valeurs par défaut dans les colonnes spécifiées.
    
    :param df: Le DataFrame à nettoyer
    :param cleaning_dict: Dictionnaire contenant :
        - "data_field" : Liste des noms de colonnes à nettoyer
        - "default_value_na" : Valeur par défaut à remplacer par "NA"
        - "default_value_missing" : Valeur par défaut à remplacer par "MISS"
    :return: Le DataFrame nettoyé
    """
    # Parcourir chaque colonne spécifiée dans le dictionnaire
    for col, defaults in cleaning_dict.items():
        if col in df.columns:
            # Remplacer les valeurs par défaut des champs "non applicables" par "NA"
            if "default_value_na" in defaults:
                df[col] = df[col].replace(defaults["default_value_na"], "NA")
            
            # Remplacer les valeurs par défaut des données manquantes par "MISS"
            if "default_value_missing" in defaults:
                df[col] = df[col].replace(defaults["default_value_missing"], "MISS")
    return df
