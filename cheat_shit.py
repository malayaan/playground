Très bonne démarche, et bravo pour cette approche robuste et concrète ! Pour structurer une slide claire, explicite et percutante, tu peux organiser ta présentation en 4 blocs, chacun correspondant à un sous-ensemble technique de ton approche (OCR, 2D-Doc, matching revenu, matching identité), et faire ressortir la valeur ajoutée audit, les résultats quanti, et la cible de risque.


---

Titre de la slide :

Approche data sur la détection de fraude documentaire – Audit XGRS


---

Structure recommandée de la slide (4 volets) :

1. Extraction des données : OCR & 2D-Doc

Objectif : Extraire les données fiscales depuis les avis d’imposition clients, via :

OCR (texte libre) : zones prénom, nom, revenus

Lecture 2D-Doc (zone sécurisée) : données authentifiées + signature


Technique :

OCR optimisé avec post-traitement (normalisation des accents, nettoyage des caractères)

Décodage des DataMatrix 2D-Doc avec validation de la signature cryptographique (authentification du document)


Résultat :

+90% de taux de lecture exploitable

Sécurisation des données d’entrée avant comparaison



---

2. Matching identité : nom / prénom

Objectif : Identifier les cas où le nom/prénom déclaré dans Doctoire de Crédit ne correspond pas au document justificatif fourni

Méthodologie :

Nettoyage des noms (casse, accents, tirets, prénoms multiples)

Matching textuel avec seuils de tolérance

Identification des cas de divergence document / demandeur


Résultat :

136 dossiers suspects identifiés

~1 M€ d’encours potentiellement frauduleux

Suspicions de fraude par usurpation ou substitution de documents



---

3. Matching revenu : montant fiscal déclaré

Objectif : Vérifier que le revenu fiscal utilisé dans l’analyse de crédit correspond bien à celui figurant sur le justificatif (2D-Doc)

Méthodologie :

Extraction du revenu fiscal via OCR et 2D-Doc

Comparaison avec les données saisies dans Doctoire de Crédit

Repérage des écarts anormaux ou manipulation de données


Résultat :

8 500 dossiers avec anomalies de revenu détectées

~100 M€ d’encours associés à des dossiers incohérents



---

4. Fiabilisation par audit manuel / statistique

Objectif : Mesurer la qualité des alertes générées par les approches automatiques

Méthodologie :

Échantillonnage aléatoire (approche statistique)

Révision manuelle des documents identifiés comme K.O

Taux d’erreur ou de "faux positifs" documenté


Résultat attendu :

Affinage des seuils de matching (éviter les faux positifs)

Définition d’un protocole de revue systématique (pouvant être industrialisé)



---

Bas de slide – zone conclusion / message clé

Approche robuste combinant OCR + cryptographie + matching automatique, avec détection effective de fraude documentaire à fort impact financier.
Mise en lumière de risques opérationnels peu visibles jusqu’ici, sur des volumes significatifs.
Candidature à industrialisation partielle ou intégration dans le process de contrôle crédit.


---

Souhaites-tu une version graphique ou PowerPoint mockup de cette slide ? Je peux t’en générer une maquette si besoin !

