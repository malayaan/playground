Voici un exemple de code qui reprend la structure “try / except” avec des continue pour chaque exception, afin de imiter le fonctionnement du code d’origine. On applique en plus un nettoyage du canal droit via noisereduce :

import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel_and_clean(audio_files, path_filter_list=None, min_duration=2):
    """
    Extrait le canal 'adviser' (canal droit) d'un fichier audio stéréo,
    applique une réduction de bruit via noisereduce, et exporte le résultat.

    On gère les erreurs avec des except + continue, de façon similaire à l'exemple d'origine.
    """

    if path_filter_list is None:
        path_filter_list = []

    missed_dict = {}

    for audio_file in audio_files:
        # -- Étape 1 : Filtrer le chemin s'il contient un mot interdit --
        if any(filtre in audio_file for filtre in path_filter_list):
            print(f"[SKIP] {audio_file} (filtré par path_filter_list)")
            continue

        # -- Étape 2 : Vérifier l'extension --
        ext = os.path.splitext(audio_file)[1].lower()
        if ext not in [".wav", ".mp3"]:
            print(f"[SKIP] {audio_file} (extension non prise en charge)")
            missed_dict[audio_file] = "unsupported extension"
            continue

        try:
            # -- Étape 3 : Charger le fichier audio --
            if ext == ".wav":
                track = AudioSegment.from_file(audio_file, format="wav")
            else:
                track = AudioSegment.from_file(audio_file, format="mp3")

            # -- Étape 4 : Vérifier la stéréo --
            if track.channels != 2:
                # On lève une ValueError pour gérer ça dans un except distinct
                raise ValueError("not stereo")

            # -- Étape 5 : Vérifier la durée minimale --
            duration_sec = len(track) / 1000.0
            if duration_sec < min_duration:
                raise ValueError("too short")

            # -- Étape 6 : Séparer les canaux stéréo --
            channels = track.split_to_mono()
            if len(channels) < 2:
                raise ValueError("split error")

            # Canal adviser = canal droit (index 1)
            adviser_channel = channels[1]

            # -- Étape 7 : Réduction de bruit --
            # Convertir en numpy float32 pour noisereduce
            samples = np.array(adviser_channel.get_array_of_samples()).astype(np.float32)
            reduced_noise = nr.reduce_noise(
                y=samples,
                sr=adviser_channel.frame_rate
            )

            # -- Étape 8 : Recréer un AudioSegment à partir du signal nettoyé --
            reduced_noise_int16 = np.int16(reduced_noise)
            cleaned_segment = AudioSegment(
                reduced_noise_int16.tobytes(),
                frame_rate=adviser_channel.frame_rate,
                sample_width=2,  # 16 bits
                channels=1
            )

            # (Optionnel) Normalisation
            # from pydub import effects
            # cleaned_segment = effects.normalize(cleaned_segment)

            # -- Étape 9 : Exporter le canal nettoyé --
            output_file = os.path.splitext(audio_file)[0] + "_adviser_cleaned.wav"
            cleaned_segment.export(output_file, format="wav")
            print(f"[OK] Canal adviser nettoyé et exporté : {output_file}")

        except CouldntDecodeError:
            # Cas d'erreur de décodage (fichier corrompu, etc.)
            print(f"[ERREUR] Impossible de décoder {audio_file}")
            missed_dict[audio_file] = "decoding error"
            continue

        except ValueError as e:
            # Cas d'erreur pour "not stereo", "too short", "split error", etc.
            print(f"[ERREUR] {audio_file} : {e}")
            missed_dict[audio_file] = str(e)
            continue

        except Exception as e:
            # Toute autre erreur imprévue
            print(f"[ERREUR] {audio_file} : {e}")
            missed_dict[audio_file] = str(e)
            continue

    return missed_dict

Explications

1. Bloc try/except :

Tout le cœur du traitement (chargement, vérifications, réduction de bruit, export) est dans un seul bloc try.

Les exceptions sont gérées séparément :

CouldntDecodeError : erreur de décodage audio.

ValueError : on lève nous-mêmes cette exception pour les cas « not stereo », « too short », etc.

Exception : tout le reste.


Dans chaque bloc except, on enregistre le fichier fautif dans missed_dict[audio_file] = "raison" puis on fait un continue pour passer au fichier suivant.



2. Structure “inspirée du code d’origine” :

On reprend l’idée de faire des continue après avoir enregistré l’erreur (ou le skip) dans un dictionnaire.

On a un “if extension not in [...] : skip + continue” avant même le try, comme dans beaucoup de scripts originaux qui trient vite le format.



3. Réduction de bruit :

On utilise noisereduce.reduce_noise(...) avec le canal droit converti en NumPy.

On reconstitue ensuite un AudioSegment mono.



4. Export :

On exporte sous la forme fichier_adviser_cleaned.wav.




Cette approche combine donc la structure d’erreurs (try/except + continue) que vous souhaitiez conserver, et la logique de réduction de bruit noisereduce.

