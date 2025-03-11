import re

# Liste des mots-clés à supprimer (suffixes d'entreprise)
suffixes = ["SA", "Inc", "Ltd", "Group", "Corporation", "Company", "Holdings", "PLC", "NV", "AG", "LLC", "Co", "Limited", "SE", "SAS"]

# Fonction pour nettoyer les noms d'entreprise
def clean_name(name):
    words = name.split()
    words = [word for word in words if word not in suffixes]  # Supprimer les suffixes
    return " ".join(words)

# Appliquer le nettoyage
df_name1_extended["Cleaned_Name1"] = df_name1_extended["Name1"].apply(clean_name)
df_name2_extended["Cleaned_Name2"] = df_name2_extended["Name2"].apply(clean_name)

# Fonction améliorée avec plusieurs scores
def find_best_matches_advanced(name1_list, name2_list, top_n=3):
    matches = []

    for name in name1_list:
        best_matches = process.extract(name, name2_list, scorer=fuzz.WRatio, limit=top_n)  # WRatio combine plusieurs méthodes
        for match in best_matches:
            matches.append((name, match[0], match[1]))  # (Nom original, Meilleure correspondance, Score)

    # Création du DataFrame des résultats
    result_df = pd.DataFrame(matches, columns=["Name1", "Name2", "Score"])
    return result_df

# Exécuter avec les noms nettoyés
result_df_advanced = find_best_matches_advanced(
    df_name1_extended["Cleaned_Name1"].tolist(), 
    df_name2_extended["Cleaned_Name2"].tolist()
)

# Afficher le tableau
tools.display_dataframe_to_user(name="Advanced Matching Names", dataframe=result_df_advanced)