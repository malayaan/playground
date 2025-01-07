import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Supposons que `df` soit votre DataFrame contenant `business_metric` et `anomaly_score`

# Définir des seuils pour déterminer une anomalie
threshold_business = 0.5
threshold_anomaly = 0.5

# Ajouter des colonnes pour les classes "anomalie" ou "non anomalie"
df['business_class'] = np.where(df['business_metric'] > threshold_business, 1, 0)
df['model_class'] = np.where(df['anomaly_score'] > threshold_anomaly, 1, 0)

# Calculer la matrice de confusion
conf_matrix = confusion_matrix(df['business_class'], df['model_class'])

# Visualiser la matrice de confusion avec des labels personnalisés
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=["No Anomaly", "Anomaly"])
disp.plot(cmap="Blues")

# Modifier les labels pour refléter "Model Label" et "Business Label"
plt.xlabel("Model Label", fontsize=12)
plt.ylabel("Business Label", fontsize=12)
plt.title("Confusion Matrix: Model vs Business", fontsize=14)

# Afficher la matrice de confusion
plt.show()