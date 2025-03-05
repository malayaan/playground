Voici une version modifiée de la fonction qui enveloppe la vérification du format (et d’autres tests) dans un bloc try/except, afin de lever une exception si le fichier ne respecte pas les critères attendus. Cela permet de récupérer une erreur comme dans le code d’origine.

import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel_and_clean(audio_files, path_filter_list=None, min_duration=2):
    """
    Extrait le canal 'adviser' (canal droit) d'un fichier audio stéréo,
    applique une réduction de bruit via noisereduce, et exporte le résultat.
    
    Les tests sur l'extension, la stéréo, la durée et la séparation des canaux
    sont faits via des try/except qui lèvent une erreur en cas de problème,
    de façon similaire au code d'origine.
    
    Paramètres :
    -----------
    audio_files : list
        Liste de chemins vers les fichiers audio (wav ou mp3).
    path_filter_list : list
        Liste de mots/chaînes à filtrer dans le chemin du fichier.
    min_duration : float
        Durée minimale (en secondes) en dessous de laquelle le fichier est ignoré.
    
    Retourne :
    ---------
    missed_dict : dict
        Dictionnaire {audio_file: "raison"} pour les fichiers ignorés ou en erreur.
    """
    
    if path_filter_list is None:
        path_filter_list = []

    missed_dict = {}

    for audio_file in audio_files:
        try:
            # 1) Vérifier si le chemin contient un mot filtrant
            if any(filtre in audio_file for filtre in path_filter_list):
                print(f"[SKIP] {audio_file} (filtré par path_filter_list)")
                continue

            # 2) Vérification de l'extension
            ext = os.path.splitext(audio_file)[1].lower()
            if ext not in [".wav", ".mp3"]:
                raise ValueError("unsupported extension")

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

            # 6) Séparer les canaux stéréo en deux pistes mono
            channels = track.split_to_mono()
            if len(channels) < 2:
                raise ValueError("split error")
            # Hypothèse : canal gauche = channels[0], canal droit = channels[1]
            adviser_channel = channels[1]

            # 7) Convertir le canal en tableau NumPy en float32
            samples = np.array(adviser_channel.get_array_of_samples()).astype(np.float32)

            # 8) Réduire le bruit avec noisereduce
            reduced_noise = nr.reduce_noise(
                y=samples,
                sr=adviser_channel.frame_rate  # ex: 44100 ou 16000
            )

            # 9) Reconvertir le signal en int16 pour recréer un AudioSegment
            reduced_noise_int16 = np.int16(reduced_noise)
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

Explications

Test de format et autres vérifications
Pour chaque fichier, on vérifie dans un bloc try/except :

Si le chemin contient un mot à filtrer.

Si l'extension est supportée (sinon, on lève une exception ValueError).

Si le fichier est décodable et en stéréo (sinon, on lève une exception).

Si la durée est suffisante.

Si la séparation en deux canaux est possible.


Traitement et réduction de bruit
Le canal « adviser » (ici, le canal droit, channels[1]) est converti en tableau NumPy pour appliquer noisereduce, puis reconverti en AudioSegment.

Gestion des erreurs
Les exceptions sont capturées et un message d’erreur est affiché, tout en enregistrant le fichier problématique dans le dictionnaire missed_dict.


Cette structure vous permet d’avoir un contrôle fin sur les erreurs, similaire à votre code d’origine.

