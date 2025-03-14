import pygame

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    input("Appuie sur Entrée pour arrêter...")
    pygame.mixer.music.stop()

file_path = "/chemin/vers/ton_fichier.mp3"
play_mp3(file_path)