Analyse des résultats du clustering :

1. Structure des clusters :

Les clusters sont définis par le label HDBSCAN_label, avec plusieurs clusters identifiés, y compris un cluster pour les anomalies (-1).

Chaque cluster contient des données statistiques importantes : nombre de points par classe (0 et 1), contamination, moyenne, maximum, minimum et écart-type.



2. Contamination :

La colonne "Contamination" montre la proportion d’anomalies (1) dans chaque cluster.

Les clusters ayant une contamination proche de 100% ou 0% sont bien définis :

Clusters propres : faible contamination, comme les clusters 7, 9 et 26.

Clusters critiques : contamination élevée, comme les clusters 12, 13, et 14.




3. Anomaly Score :

Seuil d’anomalie fixé à 0.38 : les points au-dessus de ce seuil sont considérés comme des anomalies.

Cela permet de relier les clusters au seuil d’anomalie pour vérifier si les clusters contiennent réellement des points critiques.



4. Correspondance avec les classes issues des contrôles (0 et 1) :

Les clusters avec des valeurs mixtes entre 0 et 1 indiquent une mauvaise séparation des classes par les contrôles.

Par exemple :

Cluster 2 a 53% de contamination, ce qui montre un mélange important entre les deux classes.

Cluster 3 et 4 ont une contamination modérée (4.99% et 8.1%), mais pourraient contenir des points mal identifiés.




5. Clusters d’intérêt :

Cluster -1 (anomalies) :

Regroupe un grand nombre de points (26,713), avec une contamination de 34.85%.

Les statistiques (moyenne, maximum, minimum) montrent des variations significatives, ce qui indique une diversité importante parmi les anomalies détectées.


Cluster 12 et 13 :

Contamination 100%, ce qui confirme qu’ils sont constitués uniquement d’anomalies.

Ces clusters doivent être analysés plus en détail pour comprendre les caractéristiques des anomalies qu’ils regroupent.




6. Alignement avec les contrôles :

Les clusters à forte contamination (près de 100%) révèlent des zones mal couvertes ou non capturées par les contrôles (1).

Les clusters modérément contaminés ou propres montrent une séparation correcte des données mais nécessitent une validation pour garantir qu’aucune anomalie n’est ignorée.





---

Conclusion :

1. Points critiques :

Les clusters avec une contamination proche de 100% doivent être examinés pour identifier les patterns spécifiques des anomalies et les champs impliqués.

Les clusters avec des valeurs mixtes (contamination entre 30-60%) signalent des problèmes de séparation entre les classes, ce qui peut révéler des champs ou contrôles mal définis.



2. Amélioration des contrôles :

Les contrôles actuels (classes 0 et 1) ne capturent pas bien certaines zones, comme les anomalies dans les clusters modérément contaminés.

Les champs liés aux clusters les plus critiques peuvent être priorisés pour affiner les règles ou enrichir le modèle.



3. Action recommandée :

Explorer les clusters d’anomalies (-1, 12, 13) pour comprendre les caractéristiques clés des anomalies.

Réévaluer les clusters mixtes (e.g. 2, 3, 4) pour valider la pertinence des seuils et contrôles.




