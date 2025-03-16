🔥 OK, version ultra simplifiée et efficace ! 🔥

📌 1️⃣ RunBatchFasterWhisper → Transcription en batch

Prend un dossier d’audios et renvoie un JSON avec les transcriptions.

from faster_whisper import WhisperModel
import os
import json

def RunBatchFasterWhisper(audio_dir, model_path, output_path):
    """Transcrit tous les fichiers audio d'un dossier avec Faster Whisper."""
    model = WhisperModel(model_path, device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")

    results = []
    for file in os.listdir(audio_dir):
        if file.endswith(".wav"):
            segments, _ = model.transcribe(os.path.join(audio_dir, file))
            results.append({"file": file, "text": " ".join(seg.text for seg in segments)})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"✅ Transcriptions sauvegardées : {output_path}")


---

📌 2️⃣ ProcessRawTranscription → Nettoyage des transcriptions

Charge le JSON, filtre les phrases trop courtes et génère un JSON propre.

def ProcessRawTranscription(input_path, output_path, min_sentence_length=10):
    """Filtre les phrases trop courtes dans les transcriptions."""
    with open(input_path, "r", encoding="utf-8") as f:
        transcriptions = json.load(f)

    filtered = [{"file": t["file"], "filtered_text": ". ".join(s for s in t["text"].split(". ") if len(s.split()) >= min_sentence_length)}
                for t in transcriptions if len(t["text"].strip()) > 0]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=4, ensure_ascii=False)

    print(f"✅ Transcriptions filtrées : {output_path}")


---

📌 3️⃣ Exécution ultra simple

RunBatchFasterWhisper(
    audio_dir="chemin/vers/AdvisorVoice",
    model_path="chemin/vers/LARGEV3",
    output_path="transcriptions_raw.json"
)

ProcessRawTranscription(
    input_path="transcriptions_raw.json",
    output_path="transcriptions_final.json"
)

✅ Deux fonctions, ultra propres, ultra rapides.
Test et dis-moi si c'est bon ! 🚀

