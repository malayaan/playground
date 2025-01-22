import pandas as pd

# Exemple de DataFrame
data = {
    "EntityId": [1, 1, 1, 2, 2, 3],
    "InstrumentId": ["A", "A", "A", "B", "B", "C"],
    "Protection1": [10, 10, 20, 5, 5, 30],
    "Protection2": [100, 100, 100, 50, 60, 200],
    "Value": [1.1, 1.1, 1.1, 2.2, 2.2, 3.3]
}
df = pd.DataFrame(data)

# Identifiez les colonnes nécessitant une fonction d'agrégation
def columns_needing_aggregation(df, group_cols):
    # Colonnes non incluses dans le group_by
    other_cols = [col for col in df.columns if col not in group_cols]
    columns_to_aggregate = []
    
    for col in other_cols:
        # Vérifier si les valeurs sont constantes pour chaque groupe
        is_unique_per_group = df.groupby(group_cols)[col].nunique().max() == 1
        if not is_unique_per_group:
            columns_to_aggregate.append(col)
    
    return columns_to_aggregate

# Colonnes nécessitant une fonction d'agrégation
group_cols = ["EntityId", "InstrumentId"]
columns_to_aggregate = columns_needing_aggregation(df, group_cols)

print("Colonnes nécessitant une fonction d'agrégation :", columns_to_aggregate)