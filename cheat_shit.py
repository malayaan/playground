Voici une rédaction structurée et synthétique de la partie méthodologie, présentant clairement le workflow global (macro steps), les étapes spécifiques (micro steps) ainsi que les principales hypothèses (key assumptions) :


---

Méthodologie

Macro workflow (global)

Le workflow a été structuré en quatre grandes étapes :

1. Extraction et préparation des données audio


2. Speech-to-Text (transcription des audios)


3. Analyse NLP et scoring automatisé


4. Validation manuelle et consolidation des résultats




---

Micro steps (étapes détaillées avec scoring)

Extraction audio :

Conversion des fichiers audio via FFmpeg (format WAV).

Séparation des prises de parole Client / Conseiller à l'aide du modèle Faster Whisper.


Speech-to-Text :

Transcription automatique intégrale via Faster Whisper (GPU).

Traitement post-transcription : nettoyage des textes, normalisation.


Analyse NLP et scoring :

Identification des réclamations :

Scoring basé sur deux modèles :

Modèle de similarité sémantique avec dictionnaire DataLab (seuil : 0,8).

Modèle de sentiment négatif client (seuil : 0,5).


Classification automatique des appels potentiellement mal catégorisés.


Détection fine des thématiques (Topic Modeling) :

Modèle NLP (spaCy, scikit-learn) pour extraction des principaux sujets d'appel.

Classification automatique des appels selon thèmes prédominants (assurances, gestion docs, intérêts, support client, etc.).


Monitoring opérationnel :

Détection des temps d’attente :

Analyse de silence avec seuil critique (>50% de durée appel en silence).


Détection des comportements sensibles :

Analyse automatisée via une blacklist de mots et expressions sensibles (« assurance obligatoire », termes non professionnels).


Identification d’opportunités commerciales :

Détection automatique de « moments de vie » clients révélant un potentiel de rebond commercial.




Validation manuelle et consolidation :

Échantillonnage aléatoire pour validation manuelle (qualité scoring).

Estimation des taux d’erreur (faux positifs).




---

Key assumptions (principales hypothèses méthodologiques)

La qualité des transcriptions (Faster Whisper) est jugée suffisante pour l’analyse NLP.

Les seuils utilisés (0,8 pour réclamations, 0,5 pour sentiment négatif) représentent un équilibre pertinent entre précision et sensibilité.

La revue manuelle de validation est représentative du volume global.

L'identification automatique des opportunités commerciales présuppose que les « moments de vie » identifiés correspondent à des occasions concrètes de rebond commercial.

Le choix des mots clés sensibles (blacklist) capture l’essentiel des comportements à risque ou non professionnels.


