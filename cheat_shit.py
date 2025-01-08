# Afficher les champs problématiques d’après les contrôles
print("\nTop 10 Champs les Plus Problématiques (Basé sur les Contrôles):")
print(fields_controls_df[['Field', 'Total_Impact_Score', 'Control_Count', 'Average_Impact_Score']].head(10).to_string(index=False))