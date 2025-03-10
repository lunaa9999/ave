import wave
import numpy as np
import matplotlib.pyplot as plt

# Ouvrir le fichier audio WAV
file_path = 'waves.wav'

with wave.open(file_path, 'rb') as audio_file:
    # Extraire les paramètres du fichier audio
    n_channels = audio_file.getnchannels()
    sample_width = audio_file.getsampwidth()
    frame_rate = audio_file.getframerate()
    n_frames = audio_file.getnframes()

    # Lire les données audio
    audio_data = audio_file.readframes(n_frames)
    audio_samples = np.frombuffer(audio_data, dtype=np.int16)

    # Affichage des informations du fichier
    print(f"Nombre de canaux: {n_channels}")
    print(f"Largeur d'échantillon (en octets): {sample_width}")
    print(f"Fréquence d'échantillonnage: {frame_rate} Hz")
    print(f"Nombre de frames (échantillons): {n_frames}")

# Tracer un extrait des ondes (afficher les 1000 premiers échantillons)
plt.plot(audio_samples[:audio_file.getnframes()])
plt.title("Extrait des ondes sonores")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude")
plt.show()
audio_samples = audio_samples / np.max(np.abs(audio_samples))
