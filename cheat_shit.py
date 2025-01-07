Pour créer une matrice de confusion entre les deux colonnes business_metric et anomaly_score, nous devons établir des seuils pour déterminer ce qui est considéré comme une anomalie ou non. Ensuite, nous calculons la matrice de confusion (TP, FP, FN, TN).

Code pour générer la matrice de confusion :

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Supposons que `df` soit votre DataFrame contenant `business_metric` et `anomaly_score`

# Définir des seuils pour déterminer une anomalie (par défaut : > 0.5 est une anomalie)
threshold_business = 0.5
threshold_anomaly = 0.5

# Ajouter des colonnes pour les classes "anomalie" ou "non anomalie"
df['business_class'] = np.where(df['business_metric'] > threshold_business, 1, 0)
df['anomaly_class'] = np.where(df['anomaly_score'] > threshold_anomaly, 1, 0)

# Calculer la matrice de confusion
conf_matrix = confusion_matrix(df['business_class'], df['anomaly_class'])

# Afficher la matrice de confusion
print("Matrice de confusion :")
print(conf_matrix)

# Visualiser la matrice de confusion
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=["No Anomaly", "Anomaly"])
disp.plot(cmap="Blues")


---

Explications des étapes :

1. Définir des seuils :

threshold_business et threshold_anomaly déterminent à partir de quelles valeurs une observation est considérée comme une anomalie pour chaque colonne.



2. Créer des classes binaires :

Une colonne binaire business_class est créée pour business_metric :

1 = anomalie (valeur > seuil)

0 = pas d’anomalie (valeur ≤ seuil)


Une colonne binaire anomaly_class est créée pour anomaly_score.



3. Calcul de la matrice de confusion :

confusion_matrix calcule la matrice sous la forme suivante :

[[TN, FP],
 [FN, TP]]

TN (True Negative) : Les deux colonnes conviennent qu’il n’y a pas d’anomalie.

FP (False Positive) : anomaly_score détecte une anomalie, mais pas business_metric.

FN (False Negative) : business_metric détecte une anomalie, mais pas anomaly_score.

TP (True Positive) : Les deux colonnes conviennent qu’il y a une anomalie.




4. Affichage graphique :

ConfusionMatrixDisplay génère une visualisation facile à lire de la matrice de confusion.





---

Résultat attendu :

Une matrice de confusion affichée sous forme de tableau et de graphique.

Le pourcentage d'accord/désaccord peut être calculé directement à partir des valeurs de la matrice.


Exemple de matrice de confusion :

[[TN FP]
 [FN TP]]

Cela vous permettra de mesurer directement l'accord entre les deux métriques (business_metric et anomaly_score).

