Voici la répartition mise à jour avec pour chaque étape :

Temps estimé (JH)

Rendu

Impact métier

Complexité technique (Low, Medium, High, Very High)



---

Étape 1 – Détection des journées de stress

Temps estimé : 4 JH

Rendu : Liste des journées de stress + score de crise (vol + variation)

Impact métier : Medium

Complexité : Medium (définition du seuil, méthode du coude, traitement de séries temporelles)



---

Étape 2 – Construction du dataset "crise"

Temps estimé : 6 JH

Rendu : Table enrichie avec secteurs, titres, indicateurs macro

Impact métier : Very High

Complexité : High (multi-sources, matching temporel, nettoyage des données, normalisation)



---

Étape 3 – Corrélations intersectorielles

Temps estimé : 4 JH

Rendu : Heatmap des corrélations sectorielles pendant les crises

Impact métier : High

Complexité : Medium (statistiques standards, visualisation métier)



---

Étape 4 – Corrélations inter-entreprises

Temps estimé : 4 JH

Rendu : Heatmap entreprises + top drawdowns

Impact métier : Medium

Complexité : Medium (analyse pairwise, sélection d’échantillons pertinents)



---

Étape 5 – Vue individuelle entreprise

Temps estimé : 5 JH

Rendu : Profils de sensibilité par entreprise / client SG

Impact métier : High

Complexité : High (matching entre typologies SG et données externes, granularité fine)



---

Étape 6 – Modèle de prédiction sectorielle

Temps estimé : 6 JH

Rendu : Modèle (XGBoost ou Lasso) + importance des variables

Impact métier : Very High

Complexité : Very High (feature engineering, tuning, interprétabilité, validation)



---

Étape 7 – Modèle prédictif entreprise

Temps estimé : 4 JH

Rendu : Modèles individuels + SHAP par titre

Impact métier : Medium

Complexité : High (multi-modélisation + faible volume par entreprise)



---

Étape 8 – Synthèse & recommandations

Temps estimé : 2 JH

Rendu : Note d’analyse + axes de stress tests à approfondir

Impact métier : High

Complexité : Low (synthèse narrative à partir des outputs)



---

Souhaites-tu un format Word/Markdown à intégrer dans un doc formel ?

