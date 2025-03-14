import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel(
    audio_files,
    channel_to_extract="adviser",
    path_filter_list=None,
    min_duration=2,
    log_info=print
):
    """
    Extrait un canal (par défaut 'adviser' = canal droit) d'un fichier audio stéréo,
    applique une réduction de bruit via noisereduce, et exporte le résultat.
    Gère les erreurs avec des except + continue, et consigne les infos via log_info.

    Paramètres :
    -----------
    audio_files : list of str
        Liste de chemins vers les fichiers audio (wav ou mp3).
    channel_to_extract : str
        Nom symbolique du canal à extraire. 'adviser' => canal droit (index 1),
        'user' => canal gauche (index 0), etc.
    path_filter_list : list of str
        Liste de mots/chaînes à filtrer dans le chemin du fichier.
    min_duration : float
        Durée minimale (en secondes) en dessous de laquelle on ignore le fichier.
    log_info : callable
        Fonction de logging (ex: print, logger.info). Reçoit un seul argument (message).

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
            if ext == ".wav":
                track = AudioSegment.from_file(audio_file, format="wav")
            else:
                track = AudioSegment.from_file(audio_file, format="mp3")

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
            if channel_to_extract.lower() == "adviser":
                selected_channel = channels[1]
            else:
                # Par exemple "user" => canal gauche
                selected_channel = channels[0]

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

            # (Optionnel) Normalisation ou autres traitements...
            # from pydub import effects
            # cleaned_segment = effects.normalize(cleaned_segment)

            # 9) Exporter le fichier nettoyé
            base, _ = os.path.splitext(audio_file)
            output_file = f"{base}_{channel_to_extract}_cleaned.wav"
            cleaned_segment.export(output_file, format="wav")
            log_info(f"[OK] {channel_to_extract} channel nettoyé -> {output_file}")

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