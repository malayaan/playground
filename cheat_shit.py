Très bien, je te propose une version plus structurée et lisible, qui respecte un déroulé logique d’audit tout en restant fidèle à ce que tu as vraiment fait :


---

Méthodologie

L’analyse s’est organisée en deux volets complémentaires :

1. le contrôle des pièces justificatives (avis d’imposition dans la GED),


2. l’analyse des relevés bancaires (SG) autour de la date de souscription.



1. Contrôle documentaire via les avis d’imposition

Extraction des documents depuis la GED (catégorie crédit conso).

Développement d’un algorithme interne de lecture de 2D-DOC, basé sur les clés publiques, pour extraire automatiquement nom, prénom, revenu fiscal de référence.

Comparaison des données extraites avec celles saisies dans I-Conso.

Identification des incohérences de nom/prénom (potentielle fraude documentaire).

Détection des écarts de revenus, y compris des erreurs de saisie fréquentes (ex : revenu annuel saisi comme mensuel → 12x trop élevé).



2. Analyse des charges réelles via les relevés SG

Pour les crédits souscrits entre septembre et décembre 2024, extraction des relevés bancaires SG des 3 mois précédents.

Détection automatique des charges récurrentes (loyers, autres crédits, pensions, etc.) via analyse des libellés bancaires.

Calcul du montant total de charges constatées.

Comparaison avec les charges déclarées dans I-Conso pour chaque dossier.



---

Ce double traitement a permis de détecter des incohérences sur les revenus, les charges et l’identité des emprunteurs, en appui sur des extractions automatisées et des vérifications manuelles ciblées.

