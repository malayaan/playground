🚀 Parfait, Faster Whisper fonctionne !
Maintenant, on va créer la fonction AudioRetranscription qui orchestre deux étapes principales :

1️⃣ Transcrire les fichiers audio en batch
2️⃣ Post-traiter les transcriptions (nettoyage, filtrage, etc.)


---

📌 1️⃣ Création de la fonction AudioRetranscription

Cette fonction va :

Récupérer les fichiers audio traités (advisor_processed_audio_dir)

Transcrire en batch avec Faster Whisper

Appliquer un post-traitement aux transcriptions

Sauvegarder le résultat final


from faster_whisper import WhisperModel
import os
import json

def run_batch_faster_whisper(audio_dir, output_path, model_path, compute_type="float16", batch_size=4, vad_filter=False):
    """
    Transcrit tous les fichiers audio d'un dossier en batch avec Faster Whisper.
    
    - audio_dir : Dossier contenant les fichiers audio (déjà prétraités)
    - output_path : Fichier JSON pour sauvegarder les transcriptions
    - model_path : Chemin du modèle Faster Whisper
    - compute_type : "float16" (GPU) ou "int8" (CPU)
    - batch_size : Nombre de fichiers traités en parallèle
    - vad_filter : Applique un Voice Activity Detection (VAD) si activé

    Retourne :
    - Liste des transcriptions
    """
    model = WhisperModel(model_path, device="cuda" if torch.cuda.is_available() else "cpu", compute_type=compute_type)

    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".wav")]

    results = []
    for audio_file in audio_files:
        segments, _ = model.transcribe(audio_file, vad_filter=vad_filter)
        transcription = " ".join(segment.text for segment in segments)
        results.append({"file": audio_file, "text": transcription})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"✅ Transcriptions sauvegardées dans {output_path}")
    return results


---

📌 2️⃣ Fonction de post-traitement process_raw_transcription

Cette fonction :

Filtre les transcriptions

Supprime les mots trop courts

Garde les phrases pertinentes


def process_raw_transcription(input_path, output_path, word_threshold=3, sentence_threshold=10):
    """
    Applique un post-traitement aux transcriptions pour améliorer la qualité.
    
    - input_path : Fichier JSON des transcriptions brutes
    - output_path : Fichier JSON des transcriptions filtrées
    - word_threshold : Longueur minimale des mots acceptés
    - sentence_threshold : Longueur minimale des phrases acceptées

    Retourne :
    - Liste des transcriptions filtrées
    """
    with open(input_path, "r", encoding="utf-8") as f:
        transcriptions = json.load(f)

    filtered_transcriptions = []
    for entry in transcriptions:
        sentences = entry["text"].split(". ")
        sentences = [s for s in sentences if len(s.split()) >= sentence_threshold]
        filtered_text = ". ".join(sentences)
        
        if len(filtered_text) > 0:
            filtered_transcriptions.append({"file": entry["file"], "filtered_text": filtered_text})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_transcriptions, f, indent=4, ensure_ascii=False)

    print(f"✅ Transcriptions post-traitées sauvegardées dans {output_path}")
    return filtered_transcriptions


---

📌 3️⃣ Pipeline AudioRetranscription

Maintenant, on assemble tout ça dans AudioRetranscription.

def AudioRetranscription(audio_dir, model_path, transcription_output, final_output):
    """
    Pipeline complète de retranscription audio :
    1️⃣ Transcription en batch avec Faster Whisper
    2️⃣ Post-traitement des transcriptions
    
    - audio_dir : Dossier contenant les fichiers audio prétraités
    - model_path : Chemin du modèle Faster Whisper
    - transcription_output : Fichier JSON temporaire des transcriptions
    - final_output : Fichier JSON final des transcriptions post-traitées
    """
    # 🔹 Étape 1 : Transcription des fichiers audio
    transcriptions = run_batch_faster_whisper(audio_dir, transcription_output, model_path)

    # 🔹 Étape 2 : Post-traitement des transcriptions
    process_raw_transcription(transcription_output, final_output)

    print("🚀 Pipeline de retranscription terminée avec succès !")


---

📌 4️⃣ Exécution de la pipeline

Tu peux maintenant lancer la pipeline complète :

AudioRetranscription(
    audio_dir="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/AdvisorVoice",
    model_path="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/LARGEV3",
    transcription_output="transcriptions_raw.json",
    final_output="transcriptions_final.json"
)


---

🚀 Résumé de ce qu'on a fait :

✅ run_batch_faster_whisper : Transcrit les fichiers audio en batch
✅ process_raw_transcription : Filtre les transcriptions
✅ AudioRetranscription : Lance tout d’un coup et génère le JSON final

👉 Teste et dis-moi si tout fonctionne ! 🔥

