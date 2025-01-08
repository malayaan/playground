# Associer les features aux champs originaux
feature_scores['Original_Fields'] = feature_scores['Feature'].map(dico)

# Associer les contrôles aux champs originaux
# On suppose que `control_to_columns` est un dictionnaire similaire pour les contrôles
control_to_columns = {
    'control_1': ['field_1', 'field_3'],
    'control_2': ['field_4', 'field_5'],
    # Ajouter vos correspondances pour les contrôles ici
}
control_scores['Original_Fields'] = control_scores['Control'].map(control_to_columns)

# Initialiser un dictionnaire pour les champs des features
fields_from_features = {}

# Parcourir chaque feature et ses champs associés
for feature, fields in dico.items():
    if feature in feature_scores['Feature'].values:  # Vérifier que la feature est problématique
        impact_score = feature_scores.loc[feature_scores['Feature'] == feature, 'Impact_Score'].values[0]
        for field in fields:
            if field not in fields_from_features:
                fields_from_features[field] = {'Total_Impact_Score': 0, 'Feature_Count': 0}
            fields_from_features[field]['Total_Impact_Score'] += impact_score
            fields_from_features[field]['Feature_Count'] += 1

# Transformer en DataFrame
fields_features_df = pd.DataFrame.from_dict(fields_from_features, orient='index')
fields_features_df.index.name = 'Field'
fields_features_df.reset_index(inplace=True)
fields_features_df['Average_Impact_Score'] = fields_features_df['Total_Impact_Score'] / fields_features_df['Feature_Count']

# Trier par impact total décroissant
fields_features_df = fields_features_df.sort_values(by='Total_Impact_Score', ascending=False)

# Initialiser un dictionnaire pour les champs des contrôles
fields_from_controls = {}

# Parcourir chaque contrôle et ses champs associés
for control, fields in control_to_columns.items():
    if control in control_scores['Control'].values:  # Vérifier que le contrôle est problématique
        impact_score = control_scores.loc[control_scores['Control'] == control, 'Impact_Score'].values[0]
        for field in fields:
            if field not in fields_from_controls:
                fields_from_controls[field] = {'Total_Impact_Score': 0, 'Control_Count': 0}
            fields_from_controls[field]['Total_Impact_Score'] += impact_score
            fields_from_controls[field]['Control_Count'] += 1

# Transformer en DataFrame
fields_controls_df = pd.DataFrame.from_dict(fields_from_controls, orient='index')
fields_controls_df.index.name = 'Field'
fields_controls_df.reset_index(inplace=True)
fields_controls_df['Average_Impact_Score'] = fields_controls_df['Total_Impact_Score'] / fields_controls_df['Control_Count']

# Trier par impact total décroissant
fields_controls_df = fields_controls_df.sort_values(by='Total_Impact_Score', ascending=False)

import matplotlib.pyplot as plt
import seaborn as sns

# Top 10 champs d'après les features
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

# Top 10 champs d'après les contrôles
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