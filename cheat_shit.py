import pandas as pd

# Chargement des données
# Assurez-vous que features_reduced_detected contient les colonnes :
# 'anomaly_score', 'anomaly_class', 'business_metric', 'business_class', et les champs pertinents.
features_reduced_detected = pd.read_csv('features_reduced_detected.csv')

# Dictionnaire des champs et catégories
categories = {
    "Pays": ["CNTRY"],
    "Statut de défaut": ["DT_DFLT_STTS"],
    "Statut financier": ["DT_FNNCL_STTMS"],
    "Notation externe": ["EXTRNL_RTNG_NM"],
    "Taille de l'entreprise": ["ENTRPRS_SZ_LE"],
    "Type de produit": ["TYP_AMRTSTN", "TYP_INTRST_RT", "TYP_MRTGG"],
    "Classification IFRS9": ["IFRS9_Classification"],
    "Capacité de remboursement": ["DBT_RPYMNT_CPCTY_SNR_DBT", "DBT_RPYMNT_CPCTY_TTL"],
}

# Étape 1 : Identifier les champs sous-contrôlés
def identify_undercontrolled_fields(features_df, categories_dict):
    controlled_fields = set(features_df.columns)  # Champs dans features_reduced_detected
    all_fields = set([field for fields in categories_dict.values() for field in fields])  # Tous les champs du dictionnaire
    missing_controls = all_fields - controlled_fields  # Champs sans contrôle
    return missing_controls

missing_controls = identify_undercontrolled_fields(features_reduced_detected, categories)

# Étape 2 : Distribution des anomalies par catégorie
def anomaly_distribution_by_category(features_df, categories_dict):
    results = {}
    for category, fields in categories_dict.items():
        fields_in_data = [field for field in fields if field in features_df.columns]
        if fields_in_data:
            anomalies = features_df[fields_in_data].notna().sum(axis=1)  # Nombre de champs non-NA
            anomaly_class_distribution = features_df['anomaly_class'].value_counts(normalize=True)
            results[category] = {
                'Total_Fields': len(fields_in_data),
                'Anomaly_Class_Distribution': anomaly_class_distribution.to_dict(),
                'Average_Anomaly_Score': features_df[fields_in_data].mean(axis=1).mean()
            }
    return pd.DataFrame(results).transpose()

anomaly_distribution = anomaly_distribution_by_category(features_reduced_detected, categories)

# Étape 3 : Analyse des champs les plus impactés
def impact_analysis(features_df, categories_dict):
    impact_scores = {}
    for category, fields in categories_dict.items():
        fields_in_data = [field for field in fields if field in features_df.columns]
        if fields_in_data:
            for field in fields_in_data:
                avg_anomaly_score = features_df['anomaly_score'][features_df[field].notna()].mean()
                avg_business_metric = features_df['business_metric'][features_df[field].notna()].mean()
                impact_scores[field] = {
                    'Average_Anomaly_Score': avg_anomaly_score,
                    'Average_Business_Metric': avg_business_metric
                }
    return pd.DataFrame(impact_scores).transpose()

field_impact_scores = impact_analysis(features_reduced_detected, categories)

# Étape 4 : Résultats synthétiques
def summary_results(missing_controls, anomaly_distribution, field_impact_scores):
    print("\nChamps sans contrôle :")
    print(missing_controls)

    print("\nDistribution des anomalies par catégorie :")
    print(anomaly_distribution)

    print("\nScores d'impact des champs :")
    print(field_impact_scores.sort_values(by='Average_Anomaly_Score', ascending=False))

summary_results(missing_controls, anomaly_distribution, field_impact_scores)