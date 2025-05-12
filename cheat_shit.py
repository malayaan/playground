Use-case name

“High-Impact Day Detector & Sector Shock Explainer”


---

Context

L’Inspection Générale souhaite un outil data-science qui repère, en temps réel, les journées où le marché global subit un mouvement anormal, puis mesure l’amplitude de la réaction sur les principaux clients corporate de SG. L’objectif est d’anticiper les expositions sectorielles les plus vulnérables et de comprendre quels facteurs macro ou micro déclenchent ces dérapages.


---

Methodology (step-by-step)

1. Global market pulse

Construire un indicateur quotidien : Δ% MSCI ACWI × volatilité intraday (ex : ATR / close).



2. Crisis-day threshold (knee method)

Appliquer l’algorithme du “coude” (kneedle) sur la distribution de l’indicateur ; seuil au-delà duquel un jour est tagué High-Impact.



3. Event bucket for manual review

Extraire la liste des dates > seuil ; fournir 3–5 jours “anormaux” par an à analyser par les équipes marchés.



4. Client stock reaction

Récupérer, pour chaque date, la variation journalière des 50 plus gros corporates SG (ticker-liste interne) ; calculer le drawdown sectoriel.



5. Feature tagging

Pour chaque date, encoder : annonce Fed/BCE, publication résultats S&P 500 > X, choc matières, headlines LEXIS.



6. Predictive model

Modèle gradient boosting pour prédire Δ% sectoriel à partir des features macro + micro + dummy “Fed”, “Earnings”, etc.



7. Variable importance / SHAP

Identifier les triggers dominants par secteur (ex : “Fed surprise” explique 35 % de la variance sur Financials, “Oil shock” 28 % sur Industrials).





---

Objective / So what

Prioritiser la surveillance des secteurs et des clients les plus sensibles aux chocs identifiés.

Fournir aux comités risques un catalogue de facteurs déclencheurs et leur impact moyen sur les encours sectoriels SG.



---

Added value

Passe d’un suivi statique des corrélations à un système d’alerte data-driven qui cible les vraies journées critiques.

Aligne les équipes marchés, coverage et risk autour d’un langage commun des “High-Impact Days” et de leurs déclencheurs.

Sert de base aux stress tests intraday et à l’ajustement rapide des limites sectorielles.


