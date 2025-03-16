🚀 OK ! On va rendre ça ultra efficace et modulable pour Advisor & Client.

📌 Ce qu’on va faire :

✅ Transcrire chaque fichier audio et générer un JSON individuel
✅ Stocker les transcriptions brutes dans TranscriptionAdvisorDataRaw/
✅ Appliquer le post-traitement et stocker dans TranscriptionAdvisorResult/
✅ Déplacer les fichiers traités dans AdvisorVoiceTreated/
✅ Modulable pour AdvisorVoice et ClientVoice


---

📌 1️⃣ RunBatchFasterWhisper → Transcription individuelle & déplacement

Chaque fichier a son propre JSON et est déplacé après traitement.

import shutil
from faster_whisper import WhisperModel
import os
import json

def RunBatchFasterWhisper(audio_dir, model_path, raw_output_dir, treated_dir):
    """Transcrit chaque fichier audio et le déplace après traitement."""
    model = WhisperModel(model_path, device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")

    os.makedirs(raw_output_dir, exist_ok=True)
    os.makedirs(treated_dir, exist_ok=True)

    for file in os.listdir(audio_dir):
        if file.endswith(".wav"):
            file_path = os.path.join(audio_dir, file)
            output_file = os.path.join(raw_output_dir, f"{os.path.splitext(file)[0]}.json")

            # Transcription
            segments, _ = model.transcribe(file_path)
            transcription = " ".join(seg.text for seg in segments)

            # Sauvegarde JSON
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"file": file, "text": transcription}, f, indent=4, ensure_ascii=False)

            # Déplacement du fichier traité
            shutil.move(file_path, os.path.join(treated_dir, file))
            print(f"✅ Transcrit et déplacé : {file}")


---

📌 2️⃣ ProcessRawTranscription → Nettoyage & stockage

Applique un filtre et enregistre dans TranscriptionAdvisorResult/.

def ProcessRawTranscription(raw_input_dir, result_output_dir, min_sentence_length=10):
    """Filtre les transcriptions et les sauvegarde."""
    os.makedirs(result_output_dir, exist_ok=True)

    for file in os.listdir(raw_input_dir):
        if file.endswith(".json"):
            input_path = os.path.join(raw_input_dir, file)
            output_path = os.path.join(result_output_dir, file)

            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Filtrer les phrases trop courtes
            sentences = [s for s in data["text"].split(". ") if len(s.split()) >= min_sentence_length]
            filtered_text = ". ".join(sentences)

            if filtered_text.strip():
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump({"file": data["file"], "filtered_text": filtered_text}, f, indent=4, ensure_ascii=False)

                print(f"✅ Transcription affinée : {file}")


---

📌 3️⃣ Pipeline AudioRetranscription modulable pour Advisor/Client

Permet d’utiliser AdvisorVoice ou ClientVoice.

def AudioRetranscription(voice_type, model_path):
    """
    Exécute la pipeline pour AdvisorVoice ou ClientVoice.
    
    - voice_type : "Advisor" ou "Client"
    - model_path : Chemin du modèle Faster Whisper
    """
    base_path = "/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data"
    
    audio_dir = os.path.join(base_path, f"{voice_type}Voice")
    raw_output_dir = os.path.join(base_path, f"Transcription{voice_type}DataRaw")
    result_output_dir = os.path.join(base_path, f"Transcription{voice_type}Result")
    treated_dir = os.path.join(base_path, f"{voice_type}VoiceTreated")

    # 🔹 Étape 1 : Transcription et déplacement des fichiers
    RunBatchFasterWhisper(audio_dir, model_path, raw_output_dir, treated_dir)

    # 🔹 Étape 2 : Post-traitement des transcriptions
    ProcessRawTranscription(raw_output_dir, result_output_dir)

    print(f"🚀 Pipeline de retranscription terminée pour {voice_type} !")


---

📌 4️⃣ Exécution ultra simple

🔹 Pour Advisor :

AudioRetranscription(
    voice_type="Advisor",
    model_path="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/LARGEV3"
)

🔹 Pour Client :

AudioRetranscription(
    voice_type="Client",
    model_path="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/LARGEV3"
)


---

🚀 Ce qu'on a maintenant :

✅ Transcription en batch avec JSON individuel
✅ Stockage brut dans TranscriptionAdvisorDataRaw/
✅ Post-traitement et stockage final dans TranscriptionAdvisorResult/
✅ Déplacement des fichiers traités vers AdvisorVoiceTreated/
✅ Système totalement modulable pour Advisor et Client

👉 Teste et dis-moi si c'est parfait ! 🔥

