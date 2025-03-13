import pandas as pd

# Fonction pour sélectionner le meilleur match
def select_best_match(df):
    best_matches = []

    # Grouper par "Liste1" pour trouver le meilleur match pour chaque élément
    for name1, group in df.groupby("Liste1"):
        # Trouver le meilleur score
        max_score = group["Score"].max()
        best_candidates = group[group["Score"] == max_score]

        if len(best_candidates) == 1:
            # Si un seul match a le meilleur score, on le garde
            best_match = best_candidates.iloc[0]
        else:
            # Si plusieurs ont le même score, on choisit celui avec le plus de lettres en commun
            best_candidates["Common_Letters"] = best_candidates.apply(
                lambda row: len(set(row["Liste1"]) & set(row["Liste2"])), axis=1
            )
            best_match = best_candidates.loc[best_candidates["Common_Letters"].idxmax()]

        best_matches.append(best_match)

    # Créer un nouveau DataFrame avec les meilleurs résultats
    best_df = pd.DataFrame(best_matches).drop(columns=["Common_Letters"], errors="ignore")
    return best_df

# Appliquer la sélection des meilleurs matchs sur ton DataFrame existant
df_best_match = select_best_match(df)

# Afficher le résultat final
print(df_best_match)

# Sauvegarder en Excel (si besoin)
df_best_match.to_excel("best_matching_results.xlsx", index=False)