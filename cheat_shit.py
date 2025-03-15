Voici un petit script minimaliste qui prend un fichier MP3, sépare les canaux gauche et droit, et les joue un après l’autre avec pygame.mixer.


---

📌 Installation requise

pip install pygame pydub


---

📌 Code rapide pour tester

import pygame
from pydub import AudioSegment

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    input(f"Lecture de {file_path}... Appuie sur Entrée pour continuer.")
    pygame.mixer.music.stop()

def split_and_play(mp3_path):
    # Charger l'audio
    track = AudioSegment.from_file(mp3_path, format="mp3")

    # Vérifier que l'audio est bien en stéréo
    if track.channels != 2:
        print("Erreur : le fichier n'est pas stéréo.")
        return

    # Séparer les canaux
    left_channel, right_channel = track.split_to_mono()

    # Sauvegarder temporairement chaque canal
    left_path = "left_channel.wav"
    right_path = "right_channel.wav"

    left_channel.export(left_path, format="wav")
    right_channel.export(right_path, format="wav")

    # Jouer le canal gauche
    print("Lecture du canal GAUCHE...")
    play_audio(left_path)

    # Jouer le canal droit
    print("Lecture du canal DROIT...")
    play_audio(right_path)

# Exemple d'utilisation
mp3_path = "/chemin/vers/ton_fichier.mp3"  # Remplace par ton fichier
split_and_play(mp3_path)


---

📌 Explication

1. Charge le MP3 avec pydub.


2. Vérifie qu’il est bien en stéréo.


3. Sépare les canaux gauche et droit (split_to_mono()).


4. Sauvegarde chaque canal temporairement en WAV.


5. Joue chaque canal avec pygame.mixer.


6. Attends l’entrée utilisateur avant de passer au canal suivant.




---

📌 Exécution

split_and_play("/chemin/vers/ton_fichier.mp3")


---

🚀 Maintenant, tu peux entendre chaque canal séparément en un seul essai rapide !

