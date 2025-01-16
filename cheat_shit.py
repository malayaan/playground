import pandas as pd

# Charger les données
lt_sgrf = pd.read_csv("lt_sgrf.csv")  # Loan Tape complète
features_reduced_detected = pd.read_csv("features_reduced_detected.csv")  # Données réduites avec scores et classes
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

# Initialiser un dictionnaire pour stocker les résultats
category_analysis = {}

# Parcourir chaque catégorie et ses colonnes associées
for category, fields in categories.items():
    print(f"\nAnalyse pour la catégorie : {category}")
    category_results = {}
    
    # Parcourir chaque champ de la catégorie
    for field in fields:
        if field in lt_sgrf.columns:
            # Récupérer les valeurs uniques du champ
            unique_values = lt_sgrf[field].dropna().unique()
            
            # Initialiser un dictionnaire pour les résultats par valeur unique
            field_results = {}
            
            for value in unique_values:
                # Filtrer les lignes de lt_sgrf correspondant à la valeur unique
                matching_indices = lt_sgrf[lt_sgrf[field] == value].index
                
                # Aller dans features_reduced_detected pour récupérer les classes métier
                if not matching_indices.empty:
                    business_classes = features_reduced_detected.loc[matching_indices, 'business_class']
                    class_distribution = business_classes.value_counts(normalize=True).to_dict()
                    
                    # Sauvegarder la répartition des classes
                    field_results[value] = {
                        "Matching_Lines": len(matching_indices),
                        "Business_Class_Distribution": class_distribution
                    }
            
            category_results[field] = field_results
    
    category_analysis[category] = category_results

# Afficher les résultats
for category, fields_results in category_analysis.items():
    print(f"\nRésultats pour la catégorie : {category}")
    for field, values_results in fields_results.items():
        print(f"\nChamp : {field}")
        for value, analysis in values_results.items():
            print(f"Valeur unique : {value}")
            print(f"  Lignes correspondantes : {analysis['Matching_Lines']}")
            print(f"  Répartition des classes métier : {analysis['Business_Class_Distribution']}")