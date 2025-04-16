FRS Audio Analysis – Repository

Ce repository regroupe le travail réalisé pour la mission d'analyse audio du Service Après-Vente (SAV) Franfinance dans le cadre de l'audit FRS. L'objectif est d'utiliser les données audio issues des appels clients pour identifier des opportunités d'amélioration du pilotage du SAV.

Structure du Repository

1. conf

Contient les paramètres de configuration des différentes pipelines Kedro.

2. data

Dossier central regroupant l'ensemble des données nécessaires à l'analyse :

audio_data : Audios bruts issus d'Odigo (appels SAV).

data_mission : Outils métier et fichiers d'interaction avec auditeurs/audités.

embedding : Modèles d'embedding NLP.

saved_model : Modèles sauvegardés pour réutilisation directe.

transcription_data : Transcriptions générées et traitées par les pipelines Kedro.


3. notebooks

Notebooks principaux pour les analyses spécifiques :

Liens avec les données utilisées par Mathéo

Topic modeling et analyses NLP

Production des graphiques et des CSV finaux pour les livrables aux audités


4. src

Pipelines Kedro structurés par étape de traitement :

audio_processing : Prétraitement et traitement des fichiers audio.

audio_retranscription : Transcription des audios en texte.

sentiment_analysis : Analyse automatique du sentiment des échanges.


Installation

Cloner le repo

Installer les dépendances via le fichier requirements.txt


pip install -r requirements.txt

Usage

Les pipelines Kedro sont exécutés via les commandes standards Kedro :

kedro run --pipeline=<pipeline_name>

Exemple :

kedro run --pipeline=audio_retranscription

Les résultats finaux sont principalement disponibles dans le dossier data/transcription_data et générés par les notebooks associés.

Contributions

Ce projet est principalement maintenu par l'équipe audit FRS. Pour toute question ou contribution, contactez directement l'équipe projet.


---

Ce README vise à faciliter la prise en main rapide du projet et à assurer une bonne compréhension des données, outils et livrables disponibles.

