Pour un nettoyage audio (réduction de bruit, amélioration de la qualité) en Python sans utiliser de modèle externe compliqué, vous pouvez essayer l’approche suivante :

1. Charger l’audio via pydub.


2. Convertir en tableau NumPy pour appliquer un traitement.


3. Utiliser une librairie de réduction de bruit (par exemple noisereduce), qui emploie un algorithme de type « spectral gating » (plus simple qu’un réseau de neurones, mais déjà efficace).


4. Reconstruire un AudioSegment à partir du signal nettoyé.


5. (Optionnel) Appliquer une normalisation du volume.



Voici un exemple de code :

import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def clean_audio(input_file, output_file):
    """
    Réduit le bruit d'un fichier audio et exporte le résultat.
    Utilise pydub + noisereduce (spectral gating).
    """
    try:
        # 1) Charger l'audio (wav/mp3/...)
        audio = AudioSegment.from_file(input_file)
        
        # 2) (Optionnel) convertir en mono
        #    Cela facilite parfois la réduction de bruit.
        audio = audio.set_channels(1)

        # 3) Extraire les échantillons sous forme de tableau NumPy
        #    pydub renvoie des int16 (ou int32, selon le format). 
        #    On les convertit en float32 pour l'algo noisereduce.
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # 4) Appliquer la réduction de bruit
        #    noisereduce réduit le bruit de fond sur le signal
        reduced_noise = nr.reduce_noise(y=samples, sr=audio.frame_rate)

        # 5) Convertir le résultat en int16 (pour recréer un AudioSegment)
        reduced_noise_int16 = np.int16(reduced_noise)

        # 6) Reconstruire un AudioSegment
        cleaned_segment = AudioSegment(
            reduced_noise_int16.tobytes(), 
            frame_rate=audio.frame_rate,
            sample_width=2,      # 16 bits = 2 octets
            channels=1
        )

        # 7) (Optionnel) normaliser le volume
        #    from pydub import effects
        #    cleaned_segment = effects.normalize(cleaned_segment)

        # 8) Exporter le résultat
        cleaned_segment.export(output_file, format="wav")
        print(f"[OK] Audio nettoyé exporté : {output_file}")

    except CouldntDecodeError:
        print(f"[ERREUR] Impossible de décoder {input_file}")
    except Exception as e:
        print(f"[ERREUR] {input_file} : {e}")

# Exemple d'utilisation :
# clean_audio("mon_fichier_stereo.wav", "mon_fichier_cleaned.wav")

Installation de noisereduce

Assurez-vous d’installer la librairie :

pip install noisereduce

Points importants

1. Réduction de bruit basée sur la « spectral gating » : c’est une méthode assez simple et rapide, qui convient bien à beaucoup de cas de figure.


2. Mono vs. Stéréo :

Pour simplifier, on convertit souvent en mono avant d’appliquer la réduction de bruit.

Si vous voulez garder la stéréo, vous pouvez traiter chaque canal séparément :

# split_to_mono() renvoie [canal_gauche, canal_droit]
left, right = audio.split_to_mono()
# Convertir chacun en NumPy, réduire le bruit, puis recombiner



3. Normalisation : pydub.effects.normalize() peut aider à uniformiser le volume après la réduction de bruit.


4. Qualité de l’algorithme :

noisereduce donne des résultats corrects pour du bruit de fond constant (ventilation, statique, etc.).

Pour des bruits plus complexes (voix multiples, bruits impulsionnels), il faudra peut-être des algorithmes plus poussés (par exemple des modèles deep learning type RNNoise, Demucs, etc.), mais c’est plus lourd à mettre en place.




En résumé, ce code vous permet de faire un nettoyage basique de vos pistes audio en Python, sans dépendre d’un modèle externe compliqué comme cb.rnnn.

