Voici un petit script minimaliste en Python qui lit un fichier MP3 en utilisant pydub et le joue directement dans un notebook Jupyter.

Installation nécessaire (si ce n'est pas déjà fait) :

pip install pydub simpleaudio


---

Code pour lire un fichier MP3 avec AudioSegment

from pydub import AudioSegment
from pydub.playback import play

def play_mp3(file_path):
    """
    Joue un fichier MP3 donné via pydub.
    
    Paramètre :
    ----------
    file_path : str
        Chemin complet du fichier MP3 à lire.
    """
    try:
        # Charger l'audio
        audio = AudioSegment.from_file(file_path, format="mp3")
        
        # Jouer l'audio
        play(audio)

    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
file_path = "/chemin/vers/ton_fichier.mp3"  # Remplace avec le bon chemin
play_mp3(file_path)


---

Explications :

1. Chargement de l’audio

On utilise AudioSegment.from_file(file_path, format="mp3") pour charger le fichier MP3.



2. Lecture de l’audio

play(audio) utilise simpleaudio (fourni avec pydub) pour jouer le son.





---

Test rapide dans un Notebook :

Si vous êtes sous Jupyter, vous pouvez utiliser cette version avec un champ de saisie interactif :

from ipywidgets import widgets
from IPython.display import display

# Créer une boîte de texte pour saisir le chemin du fichier
file_input = widgets.Text(
    value="",
    placeholder="Entrez le chemin du fichier MP3",
    description="MP3:",
    layout=widgets.Layout(width="80%")
)

# Bouton pour exécuter la lecture
button = widgets.Button(description="Lire l'Audio")

# Action quand on clique sur le bouton
def on_button_clicked(b):
    file_path = file_input.value
    if file_path:
        play_mp3(file_path)
    else:
        print("Veuillez entrer un chemin valide.")

# Lier l'événement du bouton
button.on_click(on_button_clicked)

# Afficher les widgets
display(file_input, button)


---

Avantages :

✅ Simple et rapide
✅ Compatible Jupyter Notebook
✅ Lit directement les fichiers MP3
✅ Ne bloque pas l’exécution du notebook

Essaie-le avec le chemin exact de ton MP3, et dis-moi si ça fonctionne ! 🚀

