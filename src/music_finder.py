import os
import sys
import json
import argparse
import base64
import requests
import webbrowser
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

class MusicFinder:
    def __init__(self):
        self.search_results = []
        self.output_dir = "downloads" # TODO: Make it configurable? Requires changes at the level of the main.py (as we search for audio files in 'downloads' by default)

    def search_with_deezer(self, query, limit=5):
        url = f"https://api.deezer.com/search?q={quote(query)}&limit={limit}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_result = response.json()

            results = []
            for i, item in enumerate(json_result.get("data", [])):
                results.append({
                    'id': i + 1,
                    'title': item["title"],
                    'artist': item["artist"]["name"],
                    'album': item["album"]["title"],
                    'duration': item.get("duration"),
                    'preview_url': item.get("preview"),
                    'deezer_id': item["id"],
                })
            return results
        except Exception as e:
            print(f"Error searching with Deezer: {str(e)}")
            return []

    def get_deezer_track_info(self, track_id):
        """Get detailed track info from Deezer API"""
        url = f"https://api.deezer.com/track/{track_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting Deezer track info: {str(e)}")
            return None

    def search_song(self, query):
        print(f"Searching for: {query}")

        self.search_results = self.search_with_deezer(query)

        if not self.search_results:
            print("No results were found.")
            return []

        return self.search_results

    def display_results(self):
        if not self.search_results:
            return

        print("\nSearch Results:")
        print("-" * 80)

        for result in self.search_results:
            print(f"{result['id']}. {result['title']} - {result['artist']} ({result['album']})")

        print("-" * 80)

    def download(self, result):
        if not result.get('preview_url'):
            print("No URL available for this track.")
            return None

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            print(f"Downloading preview for: {result['title']} - {result['artist']}")
            filename = f"{self.output_dir}/{result['artist']} - {result['title']}.mp3"
            filename = ''.join(c for c in filename if c.isalnum() or c in "_ -./")

            response = requests.get(result['preview_url'], stream=True)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            print(f"Preview downloaded: {filename}")
            return filename
        except Exception as e:
            print(f"Error downloading preview: {str(e)}")
            return None

    def get_enhanced_info(self, result):
        enhanced_info = result.copy()

        if result.get('deezer_id'):
            track_info = self.get_deezer_track_info(result['deezer_id'])
            if track_info:
                if track_info.get('bpm'):
                    enhanced_info['tempo'] = track_info.get('bpm')

                if track_info.get('release_date'):
                    enhanced_info['release_date'] = track_info.get('release_date')

        return enhanced_info

    def save_result_info(self, result):
        """Save song information to a JSON file"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            # Get enhanced information
            result = self.get_enhanced_info(result)

            filename = f"{self.output_dir}/{result['artist']} - {result['title']}.json"
            filename = ''.join(c for c in filename if c.isalnum() or c in "_ -./")

            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)

            print(f"Song info saved to: {Path(filename).absolute()}")
            return filename
        except Exception as e:
            print(f"Error saving song info: {str(e)}")
            return None
