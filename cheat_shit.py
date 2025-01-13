# Étape 1 : Liste des champs manquant de contrôles
missing_fields = list(missing_controls_df['Field'])  # Champs identifiés comme manquant de contrôles

# Étape 2 : Itérer sur chaque champ manquant de contrôles et identifier les top 5 valeurs distinctes extrêmes
for field in missing_fields:
    if field in loan_tape_reduced_detected.columns:
        # Calculer les valeurs extrêmes basées sur les quantiles 1% et 99%
        quantiles = loan_tape_reduced_detected[field].quantile([0.01, 0.99])
        low_threshold = quantiles.loc[0.01]
        high_threshold = quantiles.loc[0.99]

        # Identifier les valeurs en dehors de ces seuils
        extreme_values = loan_tape_reduced_detected[
            (loan_tape_reduced_detected[field] < low_threshold) | 
            (loan_tape_reduced_detected[field] > high_threshold)
        ][field]

        # Trier les valeurs extrêmes par leur écart absolu à la moyenne
        extreme_values_sorted = extreme_values.abs().sort_values(ascending=False)

        # Filtrer les valeurs pour garantir qu'elles soient distinctes
        distinct_extreme_values = extreme_values_sorted.drop_duplicates().head(5)

        # Afficher les résultats
        print(f"\nTop 5 valeurs extrêmes distinctes pour le champ : {field}")
        print(distinct_extreme_values)

    else:
        print(f"\nLe champ {field} n'existe pas dans la Loan Tape.")