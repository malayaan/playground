Voici un exemple de fonction qui extrait la piste “adviser” (ou tout autre canal que vous souhaitez) d’un fichier audio stéréo, sans faire appel à un modèle externe (cb.rnnn). On se base exclusivement sur pydub et on supprime toute référence au modèle :

import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def extract_audio_channel(audio_files, 
                          path_filter_list=None, 
                          min_duration=2):
    """
    Extrait le canal d'un fichier audio stéréo (par ex. 'adviser' vs 'user'),
    en vérifiant la durée minimale et en gérant les erreurs éventuelles.

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

            # 6) Séparer les canaux
            #    split_to_mono() renvoie une liste de pistes mono [canal_gauche, canal_droit]
            channels = track.split_to_mono()
            if len(channels) < 2:
                print(f"[SKIP] {audio_file} (impossible de séparer 2 canaux)")
                missed_dict[audio_file] = "split error"
                continue

            # Exemple : canal 0 = user, canal 1 = adviser
            adviser_response = channels[1]

            # [Optionnel] Appliquer un "power law" ou un gain 
            # adviser_response = adviser_response ** 2
            # ou par exemple adviser_response = adviser_response.apply_gain(5)

            # 7) Exporter le canal "adviser" dans un nouveau fichier
            output_file = os.path.splitext(audio_file)[0] + "_adviser.wav"
            adviser_response.export(output_file, format="wav")
            print(f"[OK] Canal adviser extrait dans : {output_file}")

        except CouldntDecodeError:
            print(f"[ERREUR] Impossible de décoder {audio_file}")
            missed_dict[audio_file] = "decoding error"
        except Exception as e:
            print(f"[ERREUR] {audio_file} : {e}")
            missed_dict[audio_file] = str(e)

    return missed_dict

Explications principales

1. Chargement : On utilise AudioSegment.from_file(...) en spécifiant le format ("wav" ou "mp3").


2. Contrôles :

On saute les fichiers qui ne sont pas en .wav ou .mp3.

On vérifie que la piste est bien stéréo (2 canaux).

On vérifie que la durée minimale est respectée.



3. Extraction du canal :

split_to_mono() renvoie un tableau de pistes mono. Sur un fichier stéréo classique, on obtient [canal_gauche, canal_droit].

Vous pouvez choisir quel canal garder : channels[0] ou channels[1].



4. (Optionnel) Traitement du volume :

adviser_response = adviser_response ** 2 applique un exponentiel de la forme signal^2 (puissance). Cela peut modifier radicalement le volume et la dynamique du signal.

adviser_response.apply_gain(5) augmente simplement de +5 dB.



5. Export



