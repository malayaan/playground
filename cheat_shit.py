Voici une version synthétique de ta fonction sans path_filter_list, log_info, et play_audio. Elle est plus courte et garde uniquement l’essentiel : extraire un canal, nettoyer avec noisereduce, et exporter.


---

📌 Version simplifiée

import os
import numpy as np
import pygame
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel(audio_files, channel_to_extract="adviser", min_duration=2):
    missed_dict = {}

    for audio_file in audio_files:
        ext = os.path.splitext(audio_file)[1].lower()
        if ext not in [".wav", ".mp3"]:
            missed_dict[audio_file] = "unsupported extension"
            continue

        try:
            track = AudioSegment.from_file(audio_file, format=ext[1:])
            if track.channels != 2:
                raise ValueError("not stereo")

            if len(track) / 1000.0 < min_duration:
                raise ValueError("too short")

            channels = track.split_to_mono()
            if len(channels) < 2:
                raise ValueError("split error")

            selected_channel = channels[1] if channel_to_extract.lower() == "adviser" else channels[0]

            samples = np.array(selected_channel.get_array_of_samples()).astype(np.float32)
            reduced_noise = nr.reduce_noise(y=samples, sr=selected_channel.frame_rate)

            cleaned_segment = AudioSegment(
                np.int16(reduced_noise).tobytes(),
                frame_rate=selected_channel.frame_rate,
                sample_width=2,
                channels=1
            )

            output_file = f"{os.path.splitext(audio_file)[0]}_{channel_to_extract}_cleaned.wav"
            cleaned_segment.export(output_file, format="wav")

        except (CouldntDecodeError, ValueError) as e:
            missed_dict[audio_file] = str(e)
            continue

    return missed_dict


---

📌 Changements et optimisations

✅ Suppression de log_info → Plus de print(), les erreurs sont juste stockées dans missed_dict.
✅ Suppression de path_filter_list → Tous les fichiers sont traités, pas de filtrage en amont.
✅ Suppression de play_audio → La fonction ne joue plus l’audio extrait.
✅ Structure compacte et lisible → Toutes les étapes essentielles sont là, sans redondance.


---

📌 Comment l'utiliser ?

extract_audio_channel(["/chemin/vers/audio.mp3"])


---

🚀 C'est maintenant ultra-simple et efficace !

