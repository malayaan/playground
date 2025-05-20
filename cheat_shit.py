Objet : Suivi de notre échange sur PrediXia – éléments complémentaires

Bonjour José-María,

Merci encore pour le temps que tu m’as accordé lundi. Pour m’assurer d’avoir bien saisi votre approche et préparer le cadrage France, je récapitule brièvement :

PrediXia utilise 4–5 ans d’historique ventes + données marché pour prédire

1. le prix de revente optimum et


2. la probabilité de vendre en ≤ 60 jours.



L’algorithme CatBoost exploite trois familles de variables :
• Auction Info (nb de traders, nb de bids, etc.)
• Sales Historical (segment, motorisation, âge, km, couleur…)
• Market Data externes.

Objectif principal : réduire ~33 % de rechannelling et les coûts associés (stockage, transport).

KPI suivis : MAPE sur le prix et taux de succès ≤ 60 jours, monitorés quotidiennement.


Peux-tu, lorsque tu auras un créneau, partager les éléments ci-dessous ?

1. Liste détaillée des features + ranking d’importance CatBoost.


2. Slides business présentant le problème, le modèle et les gains constatés.


3. Métriques de performance (MAPE, taux de succès, courbes de suivi).


4. Dictionnaire de données (sources Sales Historical, Market Data, Auction Info) + contact des data owners.


5. Si possible, un export anonymisé (échantillon) ou un notebook illustrant la préparation des données.



Ces documents nous permettront d’évaluer plus précisément la transférabilité en France et de préparer un POC aligné avec nos règles d’allocation locales.

N’hésite pas si tu vois des points à corriger dans mon résumé.
Un grand merci d’avance pour ton aide !

Bien cordialement,

[Prénom Nom]
Inspection Générale – Data Scientist
Société Générale

