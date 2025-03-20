import numpy as np
import librosa
import json
import os
import argparse

def create_music_visualization(audio_file):
    """
    Analyser un fichier audio et générer une visualisation web
    """
    print(f"Analyse du fichier: {audio_file}")
    
    # Créer le dossier de sortie
    output_dir = "visualisation_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Charger et analyser le fichier audio
        y, sr = librosa.load(audio_file)
        
        # Calculer le spectrogramme
        D = np.abs(librosa.stft(y))
        spectrogram = librosa.amplitude_to_db(D, ref=np.max)
        
        # Obtenir le tempo et les beats
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Calculer les caractéristiques de fréquence
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Préparer les données pour le JavaScript
        data = {
            "filename": os.path.basename(audio_file),
            "duration": float(librosa.get_duration(y=y, sr=sr)),
            "tempo": float(tempo),
            "beats": beat_times.tolist(),
            "spectrogram": {
                "data": spectrogram.tolist(),
                "time_bins": spectrogram.shape[1],
                "freq_bins": spectrogram.shape[0]
            },
            "chromagram": chromagram.tolist()
        }
        
        # Convertir les données en JSON pour le JavaScript
        js_data = f"const audioData = {json.dumps(data)};"
        
        with open(f"{output_dir}/audio_data.js", "w") as f:
            f.write(js_data)
        
        # Créer les fichiers HTML, CSS et JS
        create_html_file(output_dir)
        create_css_file(output_dir)
        create_js_file(output_dir)
        
        print(f"Visualisation créée avec succès dans le dossier '{output_dir}'")
        print(f"Ouvrez 'visualisation_audio/index.html' dans votre navigateur pour voir la visualisation")
        
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier audio: {e}")