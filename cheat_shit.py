# Afficher les champs problématiques d’après les features
print("\nTop 10 Champs les Plus Problématiques (Basé sur les Features):")
print(fields_features_df[['Field', 'Total_Impact_Score', 'Feature_Count', 'Average_Impact_Score']].head(10).to_string(index=False))