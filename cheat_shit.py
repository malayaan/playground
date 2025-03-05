import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel_and_clean(audio_files, 
                                    path_filter_list=None, 
                                    min_duration=2):
    """
    Extrait le canal 'adviser' (canal droit) d'un fichier audio stéréo,
    applique une réduction de bruit via noisereduce, et exporte le résultat.

    Paramètres :
    -----------
    audio_files : list
        Liste de chemins vers les fichiers audio (wav ou mp3).
    path_filter_list : list
        Liste de mots/chaînes. Si l'un de ces mots est présent dans le chemin du fichier,
        on ignore le fichier.
    min_duration : float
        Durée minimale (en secondes) en dessous de laquelle on ignore le fichier.

    Retourne :
    ---------
    missed_dict : dict
        Dictionnaire {audio_file: "raison"} pour les fichiers ignorés ou en erreur.
    """

    if path_filter_list is None:
        path_filter_list = []

    missed_dict = {}

    for audio_file in audio_files:
        # 1) Vérifier si le chemin contient un mot filtrant
        if any(filtre in audio_file for filtre in path_filter_list):
            print(f"[SKIP] {audio_file} (filtré par path_filter_list)")
            continue

        # 2) Vérifier l'extension
        ext = os.path.splitext(audio_file)[1].lower()
        if ext not in [".wav", ".mp3"]:
            print(f"[SKIP] {audio_file} (extension non prise en charge)")
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
                print(f"[SKIP] {audio_file} (pas stéréo)")
                missed_dict[audio_file] = "not stereo"
                continue

            # 5) Vérifier la durée
            duration_sec = len(track) / 1000.0
            if duration_sec < min_duration:
                print(f"[SKIP] {audio_file} (durée {duration_sec:.1f}s < {min_duration}s)")
                missed_dict[audio_file] = "too short"
                continue

            # 6) Séparer les canaux stéréo en deux pistes mono
            channels = track.split_to_mono()
            # Hypothèse : canal gauche = channels[0], canal droit = channels[1]
            adviser_channel = channels[1]

            # 7) Convertir en numpy float32 pour noisereduce
            samples = np.array(adviser_channel.get_array_of_samples()).astype(np.float32)

            # 8) Réduire le bruit avec noisereduce
            reduced_noise = nr.reduce_noise(
                y=samples,
                sr=adviser_channel.frame_rate  # le sample rate (ex: 44100 ou 16000)
            )

            # 9) Reconstruire un AudioSegment à partir du signal nettoyé
            reduced_noise_int16 = np.int16(reduced_noise)  # repasse en int16
            cleaned_segment = AudioSegment(
                reduced_noise_int16.tobytes(),
                frame_rate=adviser_channel.frame_rate,
                sample_width=2,  # int16 = 2 octets
                channels=1       # on reste en mono
            )

            # (Optionnel) Normaliser le volume
            # from pydub import effects
            # cleaned_segment = effects.normalize(cleaned_segment)

            # 10) Exporter le canal nettoyé
            output_file = os.path.splitext(audio_file)[0] + "_adviser_cleaned.wav"
            cleaned_segment.export(output_file, format="wav")
            print(f"[OK] Canal adviser nettoyé et exporté : {output_file}")

        except CouldntDecodeError:
            print(f"[ERREUR] Impossible de décoder {audio_file}")
            missed_dict[audio_file] = "decoding error"
        except Exception as e:
            print(f"[ERREUR] {audio_file} : {e}")
            missed_dict[audio_file] = str(e)

    return missed_dict