🚀 OK, on va optimiser le traitement des milliers d’audios avec Joblib et Parallel !


---

📌 Optimisations à apporter :

✅ Utiliser Parallel et delayed de Joblib pour exécuter la transcription sur plusieurs fichiers en parallèle
✅ Utiliser n_jobs=-1 pour exploiter toutes les ressources GPU disponibles
✅ Optimiser le batch processing pour éviter les latences inutiles


---

📌 1️⃣ Mise à jour de RunBatchFasterWhisper

On ajoute Joblib pour exécuter plusieurs transcriptions en parallèle.

import shutil
import os
import json
from joblib import Parallel, delayed
from faster_whisper import WhisperModel

def transcribe_single_audio(file_path, model_path, raw_output_dir, treated_dir):
    """Transcrit un seul fichier audio, génère son JSON et le déplace."""
    model = WhisperModel(model_path, device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")

    output_file = os.path.join(raw_output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}.json")

    # Transcription
    segments, _ = model.transcribe(file_path)
    transcription = " ".join(seg.text for seg in segments)

    # Sauvegarde JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"file": os.path.basename(file_path), "text": transcription}, f, indent=4, ensure_ascii=False)

    # Déplacement du fichier traité
    shutil.move(file_path, os.path.join(treated_dir, os.path.basename(file_path)))

    print(f"✅ Transcrit et déplacé : {os.path.basename(file_path)}")


def RunBatchFasterWhisper(audio_dir, model_path, raw_output_dir, treated_dir, n_jobs=-1):
    """Transcrit tous les fichiers audio en parallèle et les déplace après traitement."""
    os.makedirs(raw_output_dir, exist_ok=True)
    os.makedirs(treated_dir, exist_ok=True)

    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".wav")]

    Parallel(n_jobs=n_jobs)(
        delayed(transcribe_single_audio)(file, model_path, raw_output_dir, treated_dir) for file in audio_files
    )

    print(f"🚀 Transcription en batch terminée pour {len(audio_files)} fichiers.")


---

📌 2️⃣ Optimisation de ProcessRawTranscription

Ici aussi, on parallélise le filtrage des transcriptions.

def process_single_transcription(input_path, output_dir, min_sentence_length):
    """Filtre une seule transcription et la sauvegarde."""
    output_path = os.path.join(output_dir, os.path.basename(input_path))

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sentences = [s for s in data["text"].split(". ") if len(s.split()) >= min_sentence_length]
    filtered_text = ". ".join(sentences)

    if filtered_text.strip():
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"file": data["file"], "filtered_text": filtered_text}, f, indent=4, ensure_ascii=False)

        print(f"✅ Transcription affinée : {os.path.basename(input_path)}")


def ProcessRawTranscription(raw_input_dir, result_output_dir, min_sentence_length=10, n_jobs=-1):
    """Applique le post-traitement des transcriptions en parallèle."""
    os.makedirs(result_output_dir, exist_ok=True)

    json_files = [os.path.join(raw_input_dir, f) for f in os.listdir(raw_input_dir) if f.endswith(".json")]

    Parallel(n_jobs=n_jobs)(
        delayed(process_single_transcription)(file, result_output_dir, min_sentence_length) for file in json_files
    )

    print(f"🚀 Post-traitement terminé pour {len(json_files)} fichiers.")


---

📌 3️⃣ Mise à jour de AudioRetranscription

On rend la fonction totalement optimisée et adaptable avec Joblib.

def AudioRetranscription(voice_type, model_path, n_jobs=-1):
    """
    Pipeline complète de retranscription avec Joblib pour un traitement ultra-rapide.

    - voice_type : "Advisor" ou "Client"
    - model_path : Chemin du modèle Faster Whisper
    - n_jobs : Nombre de jobs parallèles (-1 = utiliser tous les cores)
    """
    base_path = "/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data"
    
    audio_dir = os.path.join(base_path, f"{voice_type}Voice")
    raw_output_dir = os.path.join(base_path, f"Transcription{voice_type}DataRaw")
    result_output_dir = os.path.join(base_path, f"Transcription{voice_type}Result")
    treated_dir = os.path.join(base_path, f"{voice_type}VoiceTreated")

    # 🔹 Étape 1 : Transcription en parallèle
    RunBatchFasterWhisper(audio_dir, model_path, raw_output_dir, treated_dir, n_jobs)

    # 🔹 Étape 2 : Post-traitement en parallèle
    ProcessRawTranscription(raw_output_dir, result_output_dir, n_jobs=n_jobs)

    print(f"🚀 Pipeline de retranscription terminée pour {voice_type} avec {n_jobs} jobs !")


---

📌 4️⃣ Exécution ultra efficace

🔹 Pour Advisor :

AudioRetranscription(
    voice_type="Advisor",
    model_path="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/LARGEV3",
    n_jobs=-1  # Utilise tous les cores pour la vitesse maximale
)

🔹 Pour Client :

AudioRetranscription(
    voice_type="Client",
    model_path="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/LARGEV3",
    n_jobs=-1
)


---

🚀 Résumé de ce qu'on a maintenant :

✅ Traitement parallèle des fichiers audio avec Joblib
✅ Transcription et post-traitement ultra-rapide sur GPU
✅ Déplacement automatique des fichiers traités
✅ Pipeline 100% modulable pour Advisor et Client
✅ Exploitations maximales du GPU et des CPU


---

🔥 Teste et dis-moi si c'est parfait ! 🚀

