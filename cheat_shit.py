# Liste élargie des mots à supprimer (suffixes et termes génériques)
stopwords = {
    "sa", "inc", "ltd", "group", "corporation", "company", "holdings", "plc", "nv", "ag", "llc", "co", "limited",
    "se", "sas", "corp", "international", "industries", "enterprise", "solutions", "systems", "services"
}

# Fonction de nettoyage avancé des noms
def clean_name_advanced(name):
    if not isinstance(name, str):
        return ""

    # Suppression des caractères spéciaux et mise en minuscule
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name).lower()

    # Suppression des mots inutiles
    words = name.split()
    words = [word for word in words if word not in stopwords and len(word) > 2]  # On garde les mots significatifs

    return " ".join(words)

# Fonction avancée pour trouver les meilleurs correspondances
def find_best_matches_robust(list1, list2, top_n=3):
    # Nettoyage des noms
    cleaned_list1 = [clean_name_advanced(name) for name in list1]
    cleaned_list2 = [clean_name_advanced(name) for name in list2]

    matches = []

    for orig_name, clean_name in zip(list1, cleaned_list1):
        best_matches = process.extract(clean_name, cleaned_list2, scorer=fuzz.WRatio, limit=top_n)
        for match in best_matches:
            matches.append((orig_name, match[0], match[1]))  # (Nom original, Meilleure correspondance, Score)

    # Création du DataFrame des résultats
    result_df = pd.DataFrame(matches, columns=["Liste1", "Liste2", "Score"])
    return result_df

# Test avec des listes d'exemple
liste1_test = ["Boeing", "Airbus", "Lockheed Martin", "Dassault", "Accor", "IBM Corporation", "Amazon Inc."]
liste2_test = ["Boeing SA", "Airbus Group", "Lockheed", "Dassault Aviation", "Boeing Industries", "EADS", "Airbus Defence", 
               "Accor SA", "Accor Hotels", "IBM", "Amazon.com", "Microsoft Corporation"]

# Appliquer la fonction améliorée
result_df_robust = find_best_matches_robust(liste1_test, liste2_test)

# Afficher le tableau
tools.display_dataframe_to_user(name="Robust Matching Results", dataframe=result_df_robust)