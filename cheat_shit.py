# Utilisation de fuzzywuzzy au lieu de rapidfuzz

from fuzzywuzzy import process, fuzz
import pandas as pd
import ace_tools as tools

# Exemple de DataFrame (on utilisera ton fichier réel)
data = {
    "Name1": ["Boeing", "Airbus", "Lockheed Martin", "Dassault"],
    "Name2": ["Boeing SA", "Airbus Group", "Lockheed", "Dassault Aviation", "Boeing Industries", "EADS", "Airbus Defence"]
}
df = pd.DataFrame(data)

# Fonction pour trouver les meilleurs correspondances
def find_best_matches(df, col1, col2, top_n=3):
    matches = []

    for name in df[col1]:
        best_matches = process.extract(name, df[col2].tolist(), scorer=fuzz.token_sort_ratio, limit=top_n)
        for match in best_matches:
            matches.append((name, match[0], match[1]))  # (Nom de Name1, Nom de Name2, Score)

    # Création du DataFrame des résultats
    result_df = pd.DataFrame(matches, columns=[col1, col2, "Score"])
    return result_df

# Appliquer la fonction
result_df = find_best_matches(df, "Name1", "Name2")

# Afficher le tableau
tools.display_dataframe_to_user(name="Matching Names", dataframe=result_df)