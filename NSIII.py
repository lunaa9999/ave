# Créé par saliha.ucmak, le 20/02/2025 avec EduPython
from pydub import AudioSegment

# Charger un fichier audio
sound = AudioSegment.from_file("ton_fichier_audio.mp3")

# Afficher des informations sur l'audio (durée en ms, nombre de canaux, etc.)
print("Durée en ms:", len(sound))
print("Canaux:", sound.channels)
print("Fréquence d'échantillonnage:", sound.frame_rate)

# Obtenir un tableau d'échantillons sonores
samples = sound.get_array_of_samples()

# Afficher quelques valeurs des échantillons
print(samples[:10])  # Affiche les 10 premiers échantillons

import librosa

# Charger un fichier audio
audio_path = 'ton_fichier_audio.wav'
y, sr = librosa.load(audio_path)

# Afficher les informations
print("Durée en secondes:", librosa.get_duration(y=y, sr=sr))
print("Fréquence d'échantillonnage:", sr)

# y contient les échantillons audio sous forme d'un tableau numpy
print("Quelques valeurs des échantillons:", y[:10])

