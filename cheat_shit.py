import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Génération des données
np.random.seed(42)
normal_data = np.random.normal(loc=0, scale=1, size=(300, 2))  # Données normales
anomalies = np.random.uniform(low=-4, high=4, size=(30, 2))    # Anomalies
data = np.vstack((normal_data, anomalies))

# Ajout d'un flag caricatural pour les contrôles (marque quelques points normaux comme anormaux)
controls_flagged = normal_data[np.random.choice(normal_data.shape[0], size=10, replace=False)]

# Modèle Isolation Forest
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(data)
labels = iso_forest.predict(data)

# Création du graphique
plt.figure(figsize=(10, 6))

# Points normaux
plt.scatter(data[labels == 1][:, 0], data[labels == 1][:, 1], c='black', label='Normal Data')

# Points anormaux détectés par le modèle
plt.scatter(data[labels == -1][:, 0], data[labels == -1][:, 1], c='red', label='Detected Anomalies')

# Points flaggés par les contrôles métiers
plt.scatter(controls_flagged[:, 0], controls_flagged[:, 1], c='blue', edgecolor='white', s=120, label='Control-Flagged Points')

# Ajout de la frontière de décision de l'Isolation Forest
xx, yy = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100))
Z = iso_forest.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='orange', label='Decision Boundary')

# Customisation du graphique
plt.title("Illustration of Anomaly Detection and Control Flags", fontsize=14)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend(loc='upper left', fontsize=10)
plt.grid(alpha=0.3)
plt.show()