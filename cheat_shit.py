Compte rendu – Entretien avec José-María Lucas (Data Scientist, Ayvens Espagne)

Contexte opérationnel
• Canaux de revente : B2B, B2C, Second Lease.
• Problème : ~1 / 3 des véhicules sont rechannellisés (> 60 j sans vente) ⇒ frais stockage + transport.
• Objectif data : réduire ce rechannelling et améliorer le choix initial de canal.

Modèle PrediXia
• Algorithme : CatBoost (catégorielles natives).
• Données : 4-5 ans d’historique ventes + market data ; date encodée pour pondération fraîcheur.
• Trois familles de features : Auction Info (nb traders, nb bids…), Sales Historical (couleur, modèle, âge, km…), Market Data.
• Sorties : prix de revente prédit + proba de vente ≤ 60 j.
• KPI : MAPE sur prix, taux de réussite ≤ 60 j ; monitoring quotidien.
• Usage : les équipes remarketing lancent chaque jour les enchères au prix PrediXia.

Applicabilité France / points de vigilance
• Règles d’allocation françaises à documenter ; modèle à ré-entraîner.
• Besoin d’un historique FR équivalent (4-5 ans) et des mêmes market data.
• Second Lease moins développé en France, impact à évaluer.
• Garder les mêmes indicateurs (MAPE, taux ≤ 60 j) pour comparer.

Demandes adressées à José-María
• Détail complet des features + feature importance CatBoost.
• Métriques de performance et courbes de suivi.
• Slides business (objectif & impact).
• Dictionnaire de données : Sales Historical, Market Data, Auction Info.
• Contacts data owners ou export anonymisé.

Prochaines étapes
• Réception du package documentaire & data-dictionary (José-María, sous 1 semaine).
• Analyse de transposabilité pour le périmètre France (Inspection, sous 3 semaines).
• Validation métier avec Remarketing France et décision Go/No-Go POC (sous 5 semaines).


Cette synthèse met en évidence le potentiel du modèle espagnol et les conditions essentielles pour un déploiement en France.

