Méthodologie complète (avec rendus associés à chaque étape)


---

Étape 1 : Détection des « crisis days »

Calcul du score stress quotidien

|Δ clôture| (variation jour / jour du MSCI ACWI).

Volatilité intraday = (High − Low) / Close.

Score = |Δ clôture| + Volatilité intraday.


Seuil automatique

Moyenne mobile + 2 σ (90 jours) ou algorithme du coude.

Flag « crisis day » quand Score > seuil.


Rendu : liste datée des stress days + histogramme des scores avec la barre-seuil.



---

Étape 2 : Construction du dataset « stress »

Pour chaque date flaggée :

Variation journalière (%) des secteurs GICS (>70 % capi).

Variation journalière (%) des entreprises : panel top-capi + grands clients SG.

Indicateurs déclencheurs : tag Fed/BCE, choc pétrole, surprises de résultats, VIX, gros titres.


Rendu : table consolidée prête pour analyse + descriptif statistique (moyenne, médiane, max des moves).



---

Étape 3 : Vue inter-sectorielle

Matrice de corrélation des variations sectorielles sur l’ensemble des crisis days.

Rendu : heat-map « inter-sector correlations in stress ».



---

Étape 4 : Vue inter-entreprises

Matrice de corrélation des variations des titres du panel sur les crisis days.

Rendu : heat-map « inter-companies correlations in stress ».



---

Étape 5 : Analyse “vue compagnie”

Pour chaque titre : drawdown moyen, volatilité relative (vs ACWI), sensibilité secteur.

Rendu : dashboard interactif company-level (Plotly / Power BI).



---

Étape 6 : Modélisation prédictive sectorielle

Modèle Gradient Boosting (XGBoost).

Cible : variation % sectorielle.

Features : indicateurs macro/news.


Rendu :

Courbe réelle vs prédite (RMSE).

Graphe SHAP « variable importance par secteur ».




---

Étape 7 : Modélisation prédictive entreprise

Modèle Gradient Boosting par titre (ou modèle global avec ID_titre).

Rendu :

Courbe réelle vs prédite pour chaque entreprise sensible.

SHAP par titre : top déclencheurs des moves d’action.




---

Livrables finaux

Deux heat-maps (secteurs, entreprises) + liste explicite des crisis days.

Dashboard interactif « vue compagnie ».

Rapports SHAP (secteurs & titres) + synthèse facteurs déclencheurs.

Note d’interprétation : secteurs/clients les plus sensibles, triggers dominants, axes de stress-test recommandés.


