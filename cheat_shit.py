import os
import numpy as np
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import noisereduce as nr

def extract_audio_channel(audio_files, saving_path, min_audio_duration=2, channel_to_extract="adviser"):
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

            selected_channel = channels[1] if channel_to_extract.lower() == "adviser" else channels[0]

            samples = np.array(selected_channel.get_array_of_samples()).astype(np.float32)
            reduced_noise = nr.reduce_noise(y=samples, sr=selected_channel.frame_rate)

            cleaned_segment = AudioSegment(
                np.int16(reduced_noise).tobytes(),
                frame_rate=selected_channel.frame_rate,
                sample_width=2,
                channels=1
            )

            output_file = os.path.join(saving_path, f"{os.path.splitext(os.path.basename(audio_file))[0]}_{channel_to_extract}_cleaned.wav")
            cleaned_segment.export(output_file, format="wav")

        except (CouldntDecodeError, ValueError) as e:
            missed_dict[audio_file] = str(e)
            continue

    return missed_dict