# Fonction améliorée prenant en entrée deux listes
def find_best_matches_from_lists(list1, list2, top_n=3):
    # Nettoyage des noms dans les listes
    cleaned_list1 = [clean_name(name) for name in list1]
    cleaned_list2 = [clean_name(name) for name in list2]

    matches = []

    for name in cleaned_list1:
        best_matches = process.extract(name, cleaned_list2, scorer=fuzz.WRatio, limit=top_n)  # WRatio combine plusieurs méthodes
        for match in best_matches:
            matches.append((name, match[0], match[1]))  # (Nom original, Meilleure correspondance, Score)

    # Création du DataFrame des résultats
    result_df = pd.DataFrame(matches, columns=["Liste1", "Liste2", "Score"])
    return result_df

# Test avec des listes d'exemple
liste1 = ["Boeing", "Airbus", "Lockheed Martin", "Dassault", "Accor"]
liste2 = ["Boeing SA", "Airbus Group", "Lockheed", "Dassault Aviation", "Boeing Industries", "EADS", "Airbus Defence", "Accor SA", "Accor Hotels"]

# Appliquer la fonction
result_df_lists = find_best_matches_from_lists(liste1, liste2)

# Afficher le tableau
tools.display_dataframe_to_user(name="Matching Results from Lists", dataframe=result_df_lists)