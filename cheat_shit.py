import matplotlib.pyplot as plt
import seaborn as sns

# Étape 1.1 : Calculer les scores globaux pour les features
# Somme et moyenne des poids
feature_scores = features_csv.sum(axis=0).reset_index()
feature_scores.columns = ['Feature', 'Total_Weight']
feature_scores['Average_Weight'] = features_csv.mean(axis=0).values

# Ajouter une métrique combinée : Score d'importance (Total * Moyenne)
feature_scores['Impact_Score'] = feature_scores['Total_Weight'] * feature_scores['Average_Weight']

# Trier les features par Impact Score
feature_scores = feature_scores.sort_values(by='Impact_Score', ascending=False)

# Étape 1.2 : Calculer les scores globaux pour les contrôles
# Somme et moyenne des poids
control_scores = controles_csv.sum(axis=0).reset_index()
control_scores.columns = ['Control', 'Total_Weight']
control_scores['Average_Weight'] = controles_csv.mean(axis=0).values

# Ajouter une métrique combinée : Score d'importance (Total * Moyenne)
control_scores['Impact_Score'] = control_scores['Total_Weight'] * control_scores['Average_Weight']

# Trier les contrôles par Impact Score
control_scores = control_scores.sort_values(by='Impact_Score', ascending=False)

# Afficher les résultats sous forme de tableau
print("Top 10 Features les plus problématiques :")
print(feature_scores[['Feature', 'Total_Weight', 'Average_Weight', 'Impact_Score']].head(10))

print("\nTop 10 Contrôles les plus problématiques :")
print(control_scores[['Control', 'Total_Weight', 'Average_Weight', 'Impact_Score']].head(10))

# Étape 1.3 : Visualiser les résultats
# Top 10 Features
plt.figure(figsize=(12, 6))
sns.barplot(
    data=feature_scores.head(10),
    x='Impact_Score',
    y='Feature',
    palette='Blues_d'
)
plt.title("Top 10 Features les Plus Problématiques (Impact Score)")
plt.xlabel("Impact Score (Total Weight x Average Weight)")
plt.ylabel("Feature")
plt.show()

# Top 10 Contrôles
plt.figure(figsize=(12, 6))
sns.barplot(
    data=control_scores.head(10),
    x='Impact_Score',
    y='Control',
    palette='Reds_d'
)
plt.title("Top 10 Contrôles les Plus Problématiques (Impact Score)")
plt.xlabel("Impact Score (Total Weight x Average Weight)")
plt.ylabel("Control")
plt.show()