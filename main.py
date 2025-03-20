import numpy as np
import librosa
import json
import os
import argparse
import webbrowser
from pathlib import Path
import subprocess
import platform

def create_music_visualization(audio_file):
    """
    Analyser un fichier audio et générer une visualisation web complète
    """
    print(f"Analyse du fichier: {audio_file}")
    
    try:
        # Charger et analyser le fichier audio
        print("Chargement du fichier audio...")
        y, sr = librosa.load(audio_file)
        print(f"Fichier audio chargé. Taux d'échantillonnage: {sr}Hz")
        
        print("Extraction des caractéristiques audio...")
        # Calculer le spectrogramme
        D = np.abs(librosa.stft(y))
        spectrogram = librosa.amplitude_to_db(D, ref=np.max)
        
        # Obtenir le tempo et les beats
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Calculer les caractéristiques de fréquence
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Extraire l'énergie par segments
        frame_length = 1024
        hop_length = 512
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Préparer les données pour le JavaScript
        print("Préparation des données pour la visualisation...")
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
            "chromagram": chromagram.tolist(),
            "energy": rms.tolist()
        }
        
        # Convertir les données en JSON pour le JavaScript
        js_data = f"const audioData = {json.dumps(data)};"
        
        # Écrire les données dans le fichier JS
        print("Écriture des données dans audio_data.js...")
        with open(f"site/audio_data.js", "w") as f:
            f.write(js_data)
        
        # Chemin complet vers le fichier HTML
        html_path = os.path.abspath(f"site/index.html")
        
        print(f"Ouverture de la visualisation dans votre navigateur...")
        
        # Ouvrir le fichier HTML dans le navigateur
        # webbrowser.open('file://' + html_path)
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier audio: {e}")
        return False


def install_required_packages():
    """Vérifie et installe les packages requis si nécessaire"""
    try:
        import pip
        
        required_packages = ["numpy", "librosa", "soundfile"]
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"Le package {package} est déjà installé.")
            except ImportError:
                print(f"Installation du package {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Package {package} installé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation des packages: {e}")
        print("Veuillez installer manuellement les packages requis avec la commande:")
        print("pip install numpy librosa soundfile")

if __name__ == "__main__":
    # Vérifier si des arguments ont été fournis
    if len(os.sys.argv) < 2:
        print("Utilisation: python visualiseur_audio.py chemin/vers/fichier_audio.mp3")
        
        # Liste des extensions audio supportées
        supported_extensions = [".wav", ".mp3", ".ogg", ".flac", ".m4a"]
        
        # Chercher automatiquement des fichiers audio dans le répertoire courant
        print("\nRecherche de fichiers audio dans le répertoire courant...")
        audio_files = []
        for ext in supported_extensions:
            audio_files.extend(list(Path(".").glob(f"*{ext}")))
        
        if audio_files:
            print("\nFichiers audio trouvés:")
            for i, file in enumerate(audio_files):
                print(f"{i+1}. {file}")
            
            try:
                choice = int(input("\nSélectionnez un fichier par son numéro (ou 0 pour quitter): "))
                if 1 <= choice <= len(audio_files):
                    audio_file = str(audio_files[choice-1])
                    print(f"\nTraitement du fichier: {audio_file}")
                    create_music_visualization(audio_file)
                else:
                    print("Sélection invalide ou annulée.")
            except ValueError:
                print("Entrée invalide.")
        else:
            print("Aucun fichier audio trouvé dans le répertoire courant.")
    else:
        audio_file = os.sys.argv[1]
        
        # Vérifier si le fichier existe
        if not os.path.exists(audio_file):
            print(f"Erreur: Le fichier '{audio_file}' n'existe pas.")
        else:
            # Essayer d'installer les packages requis
            import sys
            install_required_packages()
            
            # Créer la visualisation
            create_music_visualization(audio_file)