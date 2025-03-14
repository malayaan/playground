Voici la version mise à jour de extract_audio_channel qui utilise pygame.mixer pour jouer le fichier audio extrait au lieu de ffmpeg ou pydub.playback :


---

📌 Changements :

✅ Utilise pygame.mixer pour lire le fichier extrait.
✅ Supprime toute dépendance à ffmpeg.
✅ Garde la réduction de bruit noisereduce.
✅ Garde la structure try/except avec continue pour éviter les crashs.


---

📌 Installation requise

Avant d’exécuter le code, assure-toi d’installer ces bibliothèques :

pip install pygame pydub noisereduce


---

📌 Version mise à jour du code

import os
import numpy as np
import pygame
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel(
    audio_files,
    channel_to_extract="adviser",
    path_filter_list=None,
    min_duration=2,
    log_info=print,
    play_audio=False  # Ajout d'une option pour jouer l'audio après extraction
):
    """
    Extrait un canal audio d'un fichier stéréo, applique une réduction de bruit, 
    et joue le fichier extrait avec `pygame.mixer`.

    Paramètres :
    -----------
    audio_files : list of str
        Liste de chemins vers les fichiers audio (wav ou mp3).
    channel_to_extract : str
        Canal à extraire : 'adviser' = canal droit (index 1), 'user' = canal gauche (index 0).
    path_filter_list : list of str
        Liste de mots/chaînes à filtrer dans le chemin du fichier.
    min_duration : float
        Durée minimale (en secondes) en dessous de laquelle on ignore le fichier.
    log_info : callable
        Fonction de logging (ex: print, logger.info).
    play_audio : bool
        Si True, joue l'audio extrait avec `pygame.mixer`.

    Retourne :
    ---------
    missed_dict : dict
        Dictionnaire { audio_file : "raison" } pour les fichiers ignorés ou en erreur.
    """

    if path_filter_list is None:
        path_filter_list = []

    missed_dict = {}

    for audio_file in audio_files:
        # 1) Vérifier si le chemin contient un mot filtrant
        if any(filtre in audio_file for filtre in path_filter_list):
            log_info(f"[SKIP] {audio_file} (filtré par path_filter_list)")
            continue

        # 2) Vérifier l'extension
        ext = os.path.splitext(audio_file)[1].lower()
        if ext not in [".wav", ".mp3"]:
            log_info(f"[SKIP] {audio_file} (extension non prise en charge : {ext})")
            missed_dict[audio_file] = "unsupported extension"
            continue

        try:
            # 3) Charger le fichier audio
            track = AudioSegment.from_file(audio_file, format=ext[1:])  # "wav" ou "mp3"

            # 4) Vérifier que l'audio est stéréo
            if track.channels != 2:
                raise ValueError("not stereo")

            # 5) Vérifier la durée minimale
            duration_sec = len(track) / 1000.0
            if duration_sec < min_duration:
                raise ValueError("too short")

            # 6) Séparer les canaux stéréo
            channels = track.split_to_mono()
            if len(channels) < 2:
                raise ValueError("split error")

            # Sélection du canal (adviser = canal droit = index 1)
            selected_channel = channels[1] if channel_to_extract.lower() == "adviser" else channels[0]

            # 7) Réduction de bruit via noisereduce
            samples = np.array(selected_channel.get_array_of_samples()).astype(np.float32)
            reduced_noise = nr.reduce_noise(y=samples, sr=selected_channel.frame_rate)

            # 8) Reconstruire un AudioSegment
            reduced_noise_int16 = np.int16(reduced_noise)
            cleaned_segment = AudioSegment(
                reduced_noise_int16.tobytes(),
                frame_rate=selected_channel.frame_rate,
                sample_width=2,  # 16 bits
                channels=1       # On reste en mono
            )

            # 9) Exporter le fichier nettoyé
            base, _ = os.path.splitext(audio_file)
            output_file = f"{base}_{channel_to_extract}_cleaned.wav"
            cleaned_segment.export(output_file, format="wav")
            log_info(f"[OK] {channel_to_extract} channel nettoyé -> {output_file}")

            # 10) Lire le fichier extrait avec pygame.mixer (si activé)
            if play_audio:
                pygame.mixer.init()
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                log_info(f"[PLAYING] Lecture de {output_file}...")
                input("Appuie sur Entrée pour arrêter la lecture...")
                pygame.mixer.music.stop()

        except CouldntDecodeError:
            log_info(f"[ERROR] Could not decode {audio_file} => skipping")
            missed_dict[audio_file] = "decoding error"
            continue

        except ValueError as e:
            # Gère "not stereo", "too short", "split error", etc.
            log_info(f"[ERROR] {audio_file} => {e}, skipping")
            missed_dict[audio_file] = str(e)
            continue

        except Exception as e:
            # Toute autre erreur imprévue
            log_info(f"[ERROR] {audio_file} => {e}, skipping")
            missed_dict[audio_file] = str(e)
            continue

    return missed_dict


---

📌 Ce qui a changé :

✅ Remplace ffmpeg par pygame.mixer pour jouer l'audio extrait.
✅ Ajoute un paramètre play_audio pour activer/désactiver la lecture automatique.
✅ Garde noisereduce pour améliorer la qualité du son.
✅ Structure toujours basée sur try/except + continue.


---

📌 Comment l'utiliser ?

1. Exécuter avec lecture automatique :

extract_audio_channel(
    audio_files=["/chemin/vers/audio.mp3"],
    channel_to_extract="adviser",
    play_audio=True  # Lire l'audio après extraction
)


2. Exécuter sans jouer l’audio (juste extraction) :

extract_audio_channel(
    audio_files=["/chemin/vers/audio.mp3"],
    channel_to_extract="adviser",
    play_audio=False
)




---

📌 Résumé

🔹 Cette version évite complètement ffmpeg.
🔹 Utilise pygame.mixer pour jouer l’audio extrait.
🔹 Garde toutes les améliorations précédentes (réduction de bruit, logs, gestion des erreurs).
🔹 Ajoute une option pour activer/désactiver la lecture automatique.

🚀 Maintenant, tu peux extraire et écouter ton canal audio sans souci !

