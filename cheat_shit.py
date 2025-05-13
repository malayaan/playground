Méthodologie (étapes) et livrables – version bullet points

Étape 1 – Sélection des journées de stress

Flag un « crisis day » chaque fois que |Δ MSCI ACWI| > 2 × volatilité mobile (90 jours).

La liste de ces dates constitue le jeu d’observation.


Étape 2 – Construction du jeu de données stress

Pour chaque date retenue :
• variation journalière (%) de tous les secteurs (GICS niveau 1) ;
• variation journalière (%) des entreprises du panel (top-capi + grands clients SG) ;
• indicateurs déclencheurs (surprise Fed/BCE, choc pétrole, publication de résultats, VIX, etc.).



---

Rendus « niveau secteur »

Matrice inter-sectorielle : corrélations des variations sectorielles sur l’ensemble des crisis days (heat-map).

Vue secteur individuelle : pour chaque branche, drawdown moyen et ranking de volatilité relative.

Modèle prédictif sectoriel : gradient boosting qui prédit la variation % d’un secteur à partir des indicateurs macro.

Variable importance : SHAP pour déterminer les facteurs déclencheurs dominants de chaque move sectoriel.



---

Rendus « niveau entreprise »

Matrice inter-companies : corrélations des variations des titres du panel sur les crisis days (heat-map).

Vue “compagnie” : pour chaque titre, drawdown moyen, volatilité relative vs ACWI, sensibilité sectorielle.

Corrélations titre-indicateurs : coefficients entre variation % d’un titre et chaque facteur macro.

Modèle prédictif entreprise : gradient boosting (par titre ou global) pour estimer le move % de l’action.

Variable importance par titre : SHAP pour classer les déclencheurs clés de la réaction boursière d’une entreprise.



---

Livrables finaux

Deux heat-maps (secteurs et entreprises) pour visualiser les corrélations en stress.

Un dashboard interactif “compagnie” récapitulant drawdowns et sensibilités.

Modèles XGBoost + rapports SHAP (secteurs et titres).

Note synthèse : secteurs/clients les plus sensibles, facteurs déclencheurs majeurs, recommandations de stress-tests ciblés.


