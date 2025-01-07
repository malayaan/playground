# Définir les seuils pour les métriques
threshold_business = 0.5
threshold_anomaly = 0.5

# Ajouter des colonnes binaires pour représenter les classes
df['business_class'] = np.where(df['business_metric'] > threshold_business, 1, 0)
df['anomaly_class'] = np.where(df['anomaly_score'] > threshold_anomaly, 1, 0)

# Calculer les faux positifs (FP) et faux négatifs (FN)
# FP : anomaly_class = 1, business_class = 0
# FN : anomaly_class = 0, business_class = 1
false_positives = df[(df['anomaly_class'] == 1) & (df['business_class'] == 0)]
false_negatives = df[(df['anomaly_class'] == 0) & (df['business_class'] == 1)]

# Ajouter une colonne de "distance" pour trier par écart entre les métriques
false_positives = false_positives.assign(difference=abs(df['business_metric'] - df['anomaly_score']))
false_negatives = false_negatives.assign(difference=abs(df['business_metric'] - df['anomaly_score']))

# Sélectionner les 10 pires cas (ceux avec la plus grande différence)
top_10_fp = false_positives.nlargest(10, 'difference')
top_10_fn = false_negatives.nlargest(10, 'difference')

# Afficher les résultats
print("Top 10 Faux Positifs :")
print(top_10_fp[['business_metric', 'anomaly_score', 'difference']])

print("\nTop 10 Faux Négatifs :")
print(top_10_fn[['business_metric', 'anomaly_score', 'difference']])