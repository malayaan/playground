Étape 1 – Sélection des “stress days”

Charge : 6 JH

Complexité : Medium

Impact : Medium

Tâche : utiliser VIX & VSTOXX (> 2 σ mobile 90 j) pour établir la liste officielle des journées de crise.


Étape 2 – Constitution du jeu de données “crise”

Charge : 10 JH

Complexité : High

Impact : Very High

Tâche :   – extraire les Y (indices secteurs + titres) ;
– collecter les X macro (taux, pétrole, flags Fed/BCE, etc.) ;
– nettoyer, aligner calendriers, vérifier la pertinence des indicateurs.


Étape 3 – Analyses de corrélation

Charge : 9 JH

Complexité : Medium

Impact : High

Tâche :   – heat-map inter-secteurs ;
– heat-map inter-entreprises ;
– corrélations secteurs/titres ↔ indicateurs, comparaison au benchmark ACWI.


Étape 4 – Modèle XGBoost + SHAP (facteurs déclencheurs)

Charge : 10 JH

Complexité : High

Impact : Very High

Tâche :   – entraîner XGBoost pour prédire chaque variation secteur / titre ;
– calculer l’importance SHAP (top-3 facteurs) par secteur, par entreprise et pour les expositions auto SG ;
– livrer tableaux facteurs + mini-graphiques prévu vs réel.



