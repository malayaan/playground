
---

1. K-Means

Description : Partitionne les données en K clusters en minimisant la variance intra-cluster.

Complexité : O(n * k * i)

Gestion des outliers : Sensible aux outliers.

Spécification du nombre de clusters : Oui, K doit être défini à l'avance.

Types de données adaptés : Données numériques continues.


2. Clustering Hiérarchique

Description : Crée une hiérarchie de clusters (agglomérative ou divisive).

Complexité : O(n³)

Gestion des outliers : Peut gérer les outliers, mais ceux-ci influencent la structure.

Spécification du nombre de clusters : Non, peut déterminer le nombre optimal.

Types de données adaptés : Données numériques et catégoriques.


3. DBSCAN

Description : Identifie des clusters basés sur la densité des points.

Complexité : O(n log n)

Gestion des outliers : Gère efficacement les outliers comme bruit.

Spécification du nombre de clusters : Non, basé sur ε et MinPts.

Types de données adaptés : Données avec clusters de densité variable.


4. Mean-Shift

Description : Trouve les zones de densité maximale par glissement d'une fenêtre.

Complexité : O(t * n²)

Gestion des outliers : Peut gérer les outliers en excluant les zones de faible densité.

Spécification du nombre de clusters : Non, nombre déterminé automatiquement.

Types de données adaptés : Données avec modes de densité distincts.


5. Gaussian Mixture Models (GMM)

Description : Modélise les données avec des distributions gaussiennes.

Complexité : O(n * k * i)

Gestion des outliers : Sensible aux outliers.

Spécification du nombre de clusters : Oui, le nombre de composantes doit être défini.

Types de données adaptés : Données suivant une distribution normale.


6. BIRCH

Description : Construit une arborescence pour résumer les données.

Complexité : O(n)

Gestion des outliers : Peut gérer les outliers lors de la construction de l'arbre.

Spécification du nombre de clusters : Non, basé sur un seuil.

Types de données adaptés : Grandes bases de données numériques.


7. Spectral Clustering

Description : Utilise les propriétés du spectre de la matrice de similarité.

Complexité : O(n³)

Gestion des outliers : Sensible aux outliers.

Spécification du nombre de clusters : Oui, le nombre de clusters doit être défini.

Types de données adaptés : Données avec structures complexes.


8. Agglomerative Clustering

Description : Variante du clustering hiérarchique utilisant des mesures de liaison.

Complexité : O(n³)

Gestion des outliers : Peut gérer les outliers, influençant la structure.

Spécification du nombre de clusters : Non, nombre de clusters optimal possible.

Types de données adaptés : Données numériques et catégoriques.


9. Affinity Propagation

Description : Échange des messages pour identifier des exemplaires représentatifs.

Complexité : O(n² * log n)

Gestion des outliers : Peut gérer les outliers en les assignant à des exemplaires moins représentatifs.

Spécification du nombre de clusters : Non, émergent des données.

Types de données adaptés : Données avec mesures de similarité définies.


10. OPTICS

Description : Extension de DBSCAN pour densités variables sans paramètre explicite.

Complexité : O(n log n)

Gestion des outliers : Gère les outliers comme bruit.

Spécification du nombre de clusters : Non, détecte les clusters automatiquement.

Types de données adaptés : Données avec densités variables et distribution libre.



---

Tu peux facilement copier-coller ce format dans ton document ou outil préféré.

