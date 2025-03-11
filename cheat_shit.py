# Fonction améliorée pour trouver les meilleures correspondances
def find_best_matches_optimized(name1_list, name2_list, top_n=3):
    matches = []

    for name in name1_list:
        # Comparer avec plusieurs scores pour une meilleure précision
        best_matches = process.extract(name, name2_list, scorer=fuzz.partial_ratio, limit=top_n)
        
        for match in best_matches:
            matches.append((name, match[0], match[1]))  # (Nom de Name1, Nom de Name2, Score)

    # Création du DataFrame des résultats
    result_df = pd.DataFrame(matches, columns=["Name1", "Name2", "Score"])
    return result_df

# Ajout d'un test avec "Accor" vs "Accor SA"
df_name1_extended = pd.DataFrame({"Name1": ["Boeing", "Airbus", "Lockheed Martin", "Dassault", "Accor"]})
df_name2_extended = pd.DataFrame({"Name2": ["Boeing SA", "Airbus Group", "Lockheed", "Dassault Aviation",
                                            "Boeing Industries", "EADS", "Airbus Defence", "Accor SA", "Accor Hotels"]})

# Conversion en listes
name1_list_extended = df_name1_extended["Name1"].tolist()
name2_list_extended = df_name2_extended["Name2"].tolist()

# Exécuter la fonction améliorée
result_df_optimized = find_best_matches_optimized(name1_list_extended, name2_list_extended)

# Afficher le tableau
import ace_tools as tools
tools.display_dataframe_to_user(name="Improved Matching Names", dataframe=result_df_optimized)