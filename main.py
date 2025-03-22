import numpy as np
import librosa
import json
import os
import argparse
import webbrowser
from pathlib import Path
import subprocess
import platform

from src.music_finder import MusicFinder
from src.music_processor import MusicProcessor


#SUPPORTED_EXTENSIONS = ".wav/.mp3"
HTML_PATH = "site/index.html"

def process_audio(json_info: str):
    info = None
    with open(json_info, "r") as f:
        info = json.load(f)

    if not info:
        print("Fatal Error: No info was found in the JSON file. Exiting...") # TODO: make it more beautiful? this is not that kinda error handling i'd like to see
        exit()

    music_processor = MusicProcessor(info["audio_path"])
    tempo = music_processor.calculate_tempo()
    duration = music_processor.calculate_duration()

    info['sample_duration'] = duration

    if "tempo" in info:
        tempo = info["tempo"]
        print(f"Actual tempo provided: {tempo} BPM")
    else:
        info['tempo'] = tempo

    tempo_description = "Very slow" if tempo < 70 else "Slow" if tempo < 90 else "Moderate" if tempo < 120 else "Fast" if tempo < 150 else "Very fast"
    info["tempo_description"] = tempo_description

    bar_values = music_processor.create_frequency_bars() # TODO: Make number of bars configurable for the user?
    spectrogram_uri = music_processor.create_spectrogram(tempo) # TODO: Make the arguments configurable?

    info['barValues'] = bar_values
    info['spectrogramUri'] = spectrogram_uri

    js_data = f"const audioData = {json.dumps(info)};"
    with open(f"site/audio_data.js", "w") as f:
        f.write(js_data)

    webbrowser.open(Path(HTML_PATH).absolute().as_uri())


def search_song():
    """" Searches for a song and downloads it, as well as other useful info. Returns the path to the downloaded song or None if no song was downloaded. """
    finder = MusicFinder()

    try:
        query = input("Enter song name to search: ")
    except ValueError:
        print("Invalid input.")
        exit()

    results = finder.search_song(query)
    if not results:
        print("No results found.")
        return None

    finder.display_results()

    while True:
        try:
            finder.display_results()
            choice = input("\nEnter number to get song info (or 'q' to quit): ")
            if choice.lower() == 'q':
                print("Exiting program.")
                exit()

            choice = int(choice)

            if 1 <= choice <= len(results):
                selected = results[choice-1]
                print(f"\nSelected: {selected['title']} by {selected['artist']}")

                audio_file = finder.download(selected)
                if not audio_file:
                    print("No audio file was downloaded.")
                    return None

                file_path = Path(audio_file).absolute()
                selected['audio_uri'] = file_path.as_uri()
                selected['audio_path'] = str(file_path)

                return finder.save_result_info(selected)
            else:
                print(f"Please enter a number between 1 and {len(results)}.")

        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nExiting program.")
            exit()

    return audio_file

if __name__ == "__main__":
    #print(f"Looking for audio files in the current and 'downloads' directory (supported extensions: {SUPPORTED_EXTENSIONS})...")
    print(f"Looking for audio files in the 'downloads' directory...")

    data_files = []
    data_file = ""

    #for ext in SUPPORTED_EXTENSIONS.split("/"):
        # audio_files.extend(list(Path(".").glob(f"*{ext}"))) I dont wanna longer support this, downloading is easier
        #audio_files.extend(list(Path("./downloads").glob(f"*{ext}")))

    data_files.extend(list(Path("./downloads").glob(f"*json")))

    if not data_files:
        print("No audio files found in the current nor 'downloads' directory.")
        print("Would you like to download a song?")

        while True:
            try:
                answer = input("Y/es or N/o: ").lower()
                if answer == "y" or answer == "yes":
                    data_file = search_song()
                    if data_file:
                        process_audio(data_file)
                else:
                    print("Exiting program.")
                    exit()
            except ValueError:
                print("Invalid input.")
                exit()
            except KeyboardInterrupt:
                print("\nExiting program.")
                exit()

    print("Found audio files in the current directory:\n")
    for i, file in enumerate(data_files):
        print(f"{i+1}. {Path(file).stem}")

    print("0. Download a song!")

    while True:
        try:
            choice = input("\nMake your choice (or 'q' to quit): ")
            if choice.lower() == "q":
                print("Exiting program.")
                exit()

            choice = int(choice)

            if not (0 <= choice <= len(data_files)):
                print(f"Please enter a number between 0 and {len(data_files)}.")
            else: break

        except ValueError:
            print(f"Please enter a number between 0 and {len(data_files)}.")
        except KeyboardInterrupt:
            print("\nExiting program.")
            exit()

    audio_file = ""

    if choice == 0:
        audio_file = search_song()
    elif 1 <= choice <= len(data_files):
        audio_file = str(data_files[choice - 1])
    else:
        print("Invalid input.")

    if audio_file:
        process_audio(audio_file)
    else:
        print("No song was downloaded or selected, exiting...")
        exit()

else:
    print("This script is not meant to be imported.")
