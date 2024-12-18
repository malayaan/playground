Ci-dessous une proposition de classification de chaque contrôle en fonction de son impact réglementaire (IFRS9, exigences BCE, etc.), de l’importance des variables (EIR, IFRS9_COT, statuts de défaut), et de la gravité des conséquences en cas d’absence ou d’incohérence. Les catégories sont :

Critique (poids 10) : Affecte directement la conformité réglementaire (IFRS9, classification, EIR en défaut, off-balance crucial)

Majeur (poids 5) : Cohérence interne de données importantes pour l’analyse du risque, sans être une exigence réglementaire absolue

Mineur (poids 1) : Informations complémentaires, cohérences secondaires, non essentielles à la conformité réglementaire ou au calcul prudentiel


Hypothèses générales :

Toute incohérence ou absence touchant directement IFRS9 (classification, provisioning, off-balance, EIR sur prêts en défaut) est Critique.

Les incohérences sur les statuts internes (développement, construction) ou sur la présence de protections (collatéral) sont importantes, mais moins critiques que l’absence de champs IFRS9, donc Majeur.

Les points de détail non directement liés aux règles de classification réglementaire ou à une exigence forte sont Mineurs.


Classification ligne par ligne (d’après la logique des contrôles décrits) :

1. (EIR=NULL et NPMNT_STTS=25) : Prêt en défaut sans EIR effectif. Absence d’EIR sur un prêt en défaut (stade 3 IFRS9) est une non-conformité majeure réglementaire.
Critique (10)


2. Contrats avec un CCF ≠ 0% sur des lignes hors-bilan : Le CCF impacte le calcul des expositions pondérées en risque (RWA) et IFRS9. Mauvaise classification = souci réglementaire.
Critique (10)


3. Contrôle sur l’IFRS9, RWA MFN=2, standard method : Implication sur le calcul prudentiel et IFRS9.
Critique (10)


4. IFRS9 classification off-balance incohérente ou manquante : IFRS9 est une norme comptable réglementaire clé.
Critique (10)


5. Incohérence IFRS9 vs NPMNT_STTS : L’état de paiement (défaut, stade 2, 3) doit être cohérent avec IFRS9.
Critique (10)


6. DVLPYMT_STTS et CNSTCTN_STTS incohérence : Affecte la cohérence des données opérationnelles, pas directement IFRS9.
Majeur (5)


7. TYPE_PRCTN (type de protection) vs DVLPYMT_STTS / CNSTCTN_STTS : Protection incohérente avec le stade de développement. Important pour l’analyse du risque, mais pas IFRS9 strict.
Majeur (5)


8. Variations sur DVLPYMT_STTS / CNSTCTN_STTS : Cohérence interne, pas de mention IFRS9.
Majeur (5)


9. Autre incohérence DVLPYMT_STTS / CNSTCTN_STTS
Majeur (5)


10. Encore une incohérence sur statuts internes
Majeur (5)


11. TYPE_PRCTN et statuts internes (DVLPYMT, CNSTCTN)
Majeur (5)


12. Absence de protection réelle (cohérence entre champs) : Important pour l’estimation du risque mais pas nécessairement IFRS9 direct.
Majeur (5)


13. Incohérence sur un statut de paiement non clairement IFRS9 ? : Sans info contraire, semble interne.
Majeur (5)


14. Contrôle sur un champ annexe (Yearly express, etc.) sans lien direct IFRS9
Majeur (5) ou Mineur (1) selon l’impact. S’il n’y a aucun lien réglementaire, on privilégiera Mineur.
Mineur (1)


15. Plan d’amortissement non configuré correctement, sans lien IFRS9 direct
Mineur (1)


16. Non-provisionnement IFRS9 d’un contrat : Provision IFRS9 manquante est une non-conformité majeure.
Critique (10)


17. Distinction instruments FV P&L ou Held for Trading IFRS9 : Classification IFRS9 incorrecte.
Critique (10)


18. Collatéral / Méthode d’évaluation pratique non conforme IFRS9 ? : La valorisation correcte du collatéral est clé dans IFRS9 (ECL).
Si ce contrôle identifie l’absence d’évaluation conforme, c’est critique.
Critique (10)


19. Absence de méthode d’évaluation externe (expert) si exigé par IFRS9 : L’évaluation des actifs financiers doit suivre IFRS9.
Critique (10)


20. Off Balance mais IFRS9_COT non applicable ou manquant : IFRS9 classification manquante.
Critique (10)



(Si le fichier contient plus de 20 lignes, appliquer la même logique. Les champs strictement IFRS9 ou réglementaires sont Critiques, la cohérence interne du cycle de vie du prêt est Majeure, les détails de format ou non réglementaires sont Mineurs.)

Récapitulatif :

Critique (poids 10) : Lignes 1, 2, 3, 4, 5, 16, 17, 18, 19, 20

Majeur (poids 5) : Lignes 6, 7, 8, 9, 10, 11, 12, 13

Mineur (poids 1) : Lignes 14, 15


Ainsi, on obtient un classement clair qui reflète la priorité d’action : corriger en premier les contrôles Critiques (affectant IFRS9, EIR défaut, provisionnement, classification), ensuite les Majeurs (cohérence interne des statuts), et enfin les Mineurs (détails de paramétrage interne ou formatage).

