Analyse concise :

1. Relation entre contamination et scores d’anomalie (modèle) :

La contamination (issues des contrôles) indique la proportion d’anomalies (1) selon les règles.

Les colonnes mean, max, min, et std reflètent la distribution des scores d’anomalie (modèle).

Un écart entre la contamination et les scores d’anomalie peut révéler des points mal capturés ou des zones d’ombre dans les contrôles.





---

Exemples à regarder en détail :

1. Cluster -1 (anomalies) :

Contamination : 34.85%.

Scores d’anomalie :

Moyenne (mean) : 0.25 → proche du seuil (0.38).

Maximum (max) : 0.94 → contient des anomalies très marquées.


Conclusion : Ce cluster contient une grande proportion d'anomalies avec des écarts significatifs. Il faut inspecter ses champs pour comprendre pourquoi certaines anomalies sont capturées par les contrôles et d’autres non.



2. Cluster 12 et 13 :

Contamination : 100%.

Scores d’anomalie :

Moyenne (mean) : très faible (0.03-0.04).

Maximum (max) : faible (0.14-0.17).


Conclusion : Ces clusters sont considérés comme anomalies par les contrôles, mais leurs scores d’anomalie (modèle) sont faibles. Cela suggère des faux positifs ou des règles trop strictes.



3. Cluster 2 :

Contamination : 53.67%.

Scores d’anomalie :

Moyenne (mean) : 0.12.

Maximum (max) : 0.27.


Conclusion : Mélange entre 0 et 1, avec des scores moyens faibles. Cela indique un cluster ambigu où les contrôles et le modèle ne s’alignent pas bien.





---

Points à tirer de l’inspection :

1. Inspecter les clusters mixtes (e.g., Cluster 2) :

Identifier pourquoi les contrôles et le modèle ne s’accordent pas sur la classification.



2. Réévaluer les clusters avec faible score d’anomalie mais forte contamination (e.g., Cluster 12 et 13) :

Vérifier si les contrôles sont trop stricts et génèrent des faux positifs.



3. Prioriser les clusters avec de fortes anomalies (max élevé) :

Exemple : Cluster -1 → Focus sur les champs associés pour ajuster les contrôles et affiner le modèle.





---

Conclusion :

Les clusters montrent des

