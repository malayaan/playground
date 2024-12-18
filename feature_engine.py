Voici une proposition de classification en tenant compte à la fois de la logique réglementaire (IFRS9, calculs prudentiels) et de l’importance opérationnelle. Les variables négatives sont souvent un indicateur de saisie incorrecte, surtout si ces champs sont censés représenter des montants financiers (capitaux, dettes, encours, etc.) qui ne peuvent être négatifs dans le contexte. Le niveau de criticité dépendra principalement de l’utilisation de ces données dans des calculs réglementaires (IFRS9, estimations d’exposition, off-balance calculation).

Logique de classification :

Critique (poids 10) : Champs directement utilisés dans le cadre d’IFRS9, du calcul des expositions (EAD), de la classification hors-bilan, ou ayant un impact fort sur la conformité réglementaire. Des valeurs négatives dans ces champs peuvent fausser les calculs prudentiels ou IFRS9, ce qui est inacceptable.

Majeur (poids 5) : Champs financiers importants pour l’analyse du risque (capital, dette nette, chiffre d’affaires débiteur) mais pas directement IFRS9. Des montants négatifs y sont incohérents, mais l’impact est plus sur la qualité interne de l’analyse crédit que sur la conformité réglementaire stricte.

Mineur (poids 1) : Champs moins critiques réglementairement, où un montant négatif est surtout un problème de saisie ou d’interprétation interne, avec peu d’impact sur les calculs prudentiels ou IFRS9.


Analyse des champs :

1. EQTY_PRVS<0 (T-1 capital)
Le capital (equity) est important pour évaluer la solidité financière d’un emprunteur, mais n’est pas directement un champ IFRS9. Des capitaux négatifs sont anormaux mais impactent surtout l’analyse du risque et la cohérence des données financières internes.
Catégorie : Majeur (5)


2. EQTY<0 (capital)
Même raisonnement que ci-dessus. Le capital négatif est très inhabituel, cela indique une anomalie de saisie ou une situation extrême. Ce n’est pas directement un champ IFRS9, mais un tel défaut fausse la vision du risque.
Catégorie : Majeur (5)


3. GRP_NT_DBT<0 (financial debt)
La dette nette négative (ce qui impliquerait plus de cash que de dette, ou une mauvaise saisie) n’est pas impossible dans certains contextes, mais demeure rare et incohérente si utilisée dans l’évaluation du risque. Ce n’est pas un champ IFRS9 direct, mais une incohérence financière importante.
Catégorie : Majeur (5)


4. ANNL_TRNVR_LE<0 (debtor turnover)
Un chiffre d’affaires négatif est clairement une anomalie de données (sauf situations très particulières). Si le turnover n’est pas un champ critique pour IFRS9, cela reste important pour l’analyse du risque. Toutefois, l’impact réglementaire est moindre.
Catégorie : Majeur (5)


5. ANNL_TRNVR_PRVS<0 (debtor T-1 turnover)
Idem que ci-dessus, c’est une donnée importante pour comprendre l’évolution du client, mais pas forcément IFRS9.
Catégorie : Majeur (5)


6. OFF_BLNC_SHT_AMNT_INSTRMNT<0 (Off-balance sheet amount)
Les montants hors-bilan peuvent être utilisés dans le calcul de l’exposition au risque et dans IFRS9 (potentiellement via le CCF, Exposure At Default, etc.). Un montant négatif hors-bilan est une anomalie susceptible de fausser le calcul d’exposition, donc criticité élevée.
Catégorie : Critique (10)


7. OFF_BLNC_SHT_AMNT_INSTRMNT_PRVS<0 (Previous off-balance sheet amount)
Même logique que ci-dessus. Si la valeur précédente hors-bilan est négative, cela fausse potentiellement le suivi temporel des expositions.
Catégorie : Critique (10)


8. OTSTNDNG_MNNL_AMNT_INSTRMNT<0 (Outstanding gross nominal amount)
Le montant nominal en cours est généralement une donnée clé pour IFRS9 (ECL, staging, exposition au défaut). Un montant négatif est incompatible avec les calculs prudents.
Catégorie : Critique (10)


9. OTSTNDNG_MNNL_AMNT_INSTRMNT_PRVS<0 (Previous outstanding gross nominal amount)
Même raisonnement que ci-dessus : historique d’encours négatif, problème critique du point de vue du suivi et du calcul IFRS9.
Catégorie : Critique (10)



Récapitulatif :

Critique (10) : Données hors-bilan (I104, I105) et encours nominal (I114, I115) négatives, car impact direct potentiel sur IFRS9 et le calcul des expositions.

Majeur (5) : Capital (EQTY, EQTY_PRVS), dette nette (GRP_NT_DBT) et chiffre d’affaires (ANNL_TRNVR_LE, ANNL_TRNVR_PRVS), importants pour l’analyse du risque, mais pas directement IFRS9. Des valeurs négatives faussent l’analyse du profil de risque, sans pour autant toucher immédiatement la classification réglementaire.


Aucune ligne n’est classée en Mineur ici, car toutes ces variables représentent des données financières fondamentales. Même si elles ne sont pas toutes IFRS9, elles restent cruciales pour la compréhension du risque et la cohérence interne des données.

