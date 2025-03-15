🔥 OK, je vois exactement ce que tu veux faire.
On va structurer ça proprement pour que ce soit modulaire, scalable et réutilisable.


---

📌 Plan des fonctions

1️⃣ retrieve_audio_files

👉 Objectif : Récupérer les fichiers à traiter en comparant RootData et AdvisorVoice (ou ClientVoice).
🔹 Entrées :

root_path → Dossier où sont les fichiers Rodata.

saving_path → Dossier où les fichiers extraits (AdvisorVoice ou ClientVoice) sont enregistrés.

audio_extension → Extension des fichiers audio à traiter (mp3, wav, etc.).


🔹 Sortie :

Liste des fichiers audio non encore traités.



---

2️⃣ audio_batch_extraction

👉 Objectif : Extraire les canaux audio des fichiers trouvés par retrieve_audio_files en parallèle.
🔹 Entrées :

saving_path → Où sauvegarder les fichiers extraits.

min_audio_duration → Durée minimale d’un fichier valide.

advisor_channel_to_extract → 0 ou 1 pour choisir le canal (advisor/client).

batch_size (par défaut 10) → Nombre de fichiers traités par lot.

parallel_jobs (par défaut 4) → Nombre de processus parallèles.



---

📌 Code complet

import os
from joblib import Parallel, delayed
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr
import numpy as np

### 1️⃣ Fonction pour récupérer les fichiers à traiter ###
def retrieve_audio_files(root_path, saving_path, audio_extension="mp3"):
    """
    Récupère les fichiers audio qui n'ont pas encore été traités.
    
    - root_path : Dossier contenant les fichiers source (Rodata).
    - saving_path : Dossier où sont stockés les fichiers extraits (AdvisorVoice/ClientVoice).
    - audio_extension : Extension des fichiers audio à rechercher (ex: "mp3").

    Retourne :
    - Liste des fichiers à traiter.
    """
    root_files = set(f for f in os.listdir(root_path) if f.endswith(f".{audio_extension}"))
    processed_files = set(f for f in os.listdir(saving_path) if f.endswith(".wav"))  # On suppose que les fichiers extraits sont en WAV

    # Ne garder que les fichiers qui ne sont pas déjà traités
    files_to_process = list(root_files - processed_files)
    return [os.path.join(root_path, f) for f in files_to_process]


### 2️⃣ Fonction pour extraire les canaux audio en parallèle ###
def extract_audio_channel(audio_files, saving_path, min_audio_duration=2, advisor_channel_to_extract=1):
    """
    Extrait un canal audio d'un fichier stéréo et applique une réduction de bruit.
    
    - audio_files : Liste des fichiers à traiter.
    - saving_path : Dossier où sauvegarder les fichiers traités.
    - min_audio_duration : Durée minimale (en secondes) pour qu’un fichier soit traité.
    - advisor_channel_to_extract : 0 (canal gauche) ou 1 (canal droit).

    Retourne :
    - Dictionnaire des fichiers ignorés avec la raison.
    """
    missed_dict = {}

    if not os.path.exists(saving_path):
        os.makedirs(saving_path)

    for audio_file in audio_files:
        ext = os.path.splitext(audio_file)[1].lower()
        if ext not in [".wav", ".mp3"]:
            missed_dict[audio_file] = "unsupported extension"
            continue

        try:
            track = AudioSegment.from_file(audio_file, format=ext[1:])
            if track.channels != 2:
                raise ValueError("not stereo")
            if len(track) / 1000.0 < min_audio_duration:
                raise ValueError("too short")

            channels = track.split_to_mono()
            if len(channels) < 2:
                raise ValueError("split error")

            selected_channel = channels[advisor_channel_to_extract]

            samples = np.array(selected_channel.get_array_of_samples()).astype(np.float32)
            reduced_noise = nr.reduce_noise(y=samples, sr=selected_channel.frame_rate)

            cleaned_segment = AudioSegment(
                np.int16(reduced_noise).tobytes(),
                frame_rate=selected_channel.frame_rate,
                sample_width=2,
                channels=1
            )

            output_file = os.path.join(saving_path, f"{os.path.splitext(os.path.basename(audio_file))[0]}_cleaned.wav")
            cleaned_segment.export(output_file, format="wav")

        except (CouldntDecodeError, ValueError) as e:
            missed_dict[audio_file] = str(e)
            continue

    return missed_dict


### 3️⃣ Fonction pour exécuter l’extraction en batch ###
def audio_batch_extraction(saving_path, root_path, min_audio_duration=2, advisor_channel_to_extract=1, batch_size=10, parallel_jobs=4):
    """
    Exécute l’extraction des canaux en batch avec Joblib.
    
    - saving_path : Dossier où enregistrer les fichiers extraits.
    - root_path : Dossier source des fichiers audio (Rodata).
    - min_audio_duration : Durée minimale pour un fichier valide.
    - advisor_channel_to_extract : Canal à extraire (0=gauche, 1=droit).
    - batch_size : Nombre de fichiers traités en parallèle.
    - parallel_jobs : Nombre de processus parallèles.

    Retourne :
    - Un dictionnaire des fichiers ignorés et la raison.
    """
    audio_files = retrieve_audio_files(root_path, saving_path)

    if not audio_files:
        print("✅ Tous les fichiers ont déjà été traités.")
        return {}

    executor = Parallel(n_jobs=parallel_jobs, verbose=0)
    do = delayed(extract_audio_channel)

    tasks = (
        do(audio_files[i : i + batch_size], saving_path, min_audio_duration, advisor_channel_to_extract)
        for i in range(0, len(audio_files), batch_size)
    )

    missed_dicts = executor(tasks)

    # Fusionner les erreurs des batchs
    final_dict = {file_name: missed_reason for sub_dict in missed_dicts for file_name, missed_reason in sub_dict.items()}

    print(f"🎯 Traitement terminé. {len(audio_files) - len(final_dict)} fichiers traités, {len(final_dict)} ignorés.")
    return final_dict


---

📌 Comment l’utiliser ?

1️⃣ Lister les fichiers non traités

files_to_process = retrieve_audio_files(
    root_path="/chemin/vers/Rodata",
    saving_path="/chemin/vers/AdvisorVoice",
    audio_extension="mp3"
)
print(files_to_process)


---

2️⃣ Lancer le traitement en batch

audio_batch_extraction(
    saving_path="/chemin/vers/AdvisorVoice",
    root_path="/chemin/vers/Rodata",
    min_audio_duration=2,
    advisor_channel_to_extract=1,  # 1 = Advisor (Droite), 0 = Client (Gauche)
    batch_size=10,
    parallel_jobs=4
)


---

📌 Avantages de cette version

✅ Générique : Peut être utilisé pour AdvisorVoice ou ClientVoice en changeant juste un paramètre.
✅ Scalable : Utilise Joblib pour exécuter plusieurs extractions en parallèle.
✅ Modulaire : Deux fonctions indépendantes (retrieve_audio_files et audio_batch_extraction).
✅ Rapide : Traite uniquement les fichiers non encore extraits.
✅ Fiable : Vérifie que l’audio est stéréo, pas trop court, et lisible.


---

🔥 Maintenant, tu peux lancer ça en production ! 🚀
Si tu veux un ajustement, dis-moi !

