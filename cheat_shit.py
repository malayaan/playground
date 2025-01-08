# Initialiser un dictionnaire pour les champs issus des features
fields_from_features = {}

# Initialiser un dictionnaire pour les champs issus des contrôles
fields_from_controls = {}

# Parcourir chaque feature et ses champs associés
for feature, fields in dico.items():
    if feature in feature_scores['Feature'].values:  # Vérifier que la feature est problématique
        impact_score = feature_scores.loc[feature_scores['Feature'] == feature, 'Impact_Score'].values[0]
        for field in fields:
            if field not in fields_from_features:
                fields_from_features[field] = {'Total_Impact_Score': 0, 'Feature_Count': 0}
            fields_from_features[field]['Total_Impact_Score'] += impact_score
            fields_from_features[field]['Feature_Count'] += 1

# Parcourir chaque contrôle et ses champs associés
for control, fields in dico.items():
    if control in control_scores['Control'].values:  # Vérifier que le contrôle est problématique
        impact_score = control_scores.loc[control_scores['Control'] == control, 'Impact_Score'].values[0]
        for field in fields:
            if field not in fields_from_controls:
                fields_from_controls[field] = {'Total_Impact_Score': 0, 'Control_Count': 0}
            fields_from_controls[field]['Total_Impact_Score'] += impact_score
            fields_from_controls[field]['Control_Count'] += 1

# Convertir le dictionnaire des features en DataFrame
fields_features_df = pd.DataFrame.from_dict(fields_from_features, orient='index')
fields_features_df.index.name = 'Field'
fields_features_df.reset_index(inplace=True)
fields_features_df['Average_Impact_Score'] = fields_features_df['Total_Impact_Score'] / fields_features_df['Feature_Count']

# Trier les champs des features par impact total décroissant
fields_features_df = fields_features_df.sort_values(by='Total_Impact_Score', ascending=False)

# Convertir le dictionnaire des contrôles en DataFrame
fields_controls_df = pd.DataFrame.from_dict(fields_from_controls, orient='index')
fields_controls_df.index.name = 'Field'
fields_controls_df.reset_index(inplace=True)
fields_controls_df['Average_Impact_Score'] = fields_controls_df['Total_Impact_Score'] / fields_controls_df['Control_Count']

# Trier les champs des contrôles par impact total décroissant
fields_controls_df = fields_controls_df.sort_values(by='Total_Impact_Score', ascending=False)
import matplotlib.pyplot as plt
import seaborn as sns

# Visualiser les champs problématiques d’après les features
plt.figure(figsize=(12, 6))
sns.barplot(
    data=fields_features_df.head(10),
    x='Total_Impact_Score',
    y='Field',
    palette='Blues_d'
)
plt.title("Top 10 Champs les Plus Problématiques (Basé sur les Features)")
plt.xlabel("Total Impact Score")
plt.ylabel("Field")
plt.show()

# Visualiser les champs problématiques d’après les contrôles
plt.figure(figsize=(12, 6))
sns.barplot(
    data=fields_controls_df.head(10),
    x='Total_Impact_Score',
    y='Field',
    palette='Reds_d'
)
plt.title("Top 10 Champs les Plus Problématiques (Basé sur les Contrôles)")
plt.xlabel("Total Impact Score")
plt.ylabel("Field")
plt.show()