import librosa
import librosa.display
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import base64
from io import BytesIO
from pathlib import Path

class MusicProcessor:
    def __init__(self, audio_path):
        self.audio_path = audio_path

        # y - audio time series, sr - sampling rate
        self.y, self.sr = librosa.load(audio_path)


    def calculate_duration(self):
        duration = librosa.get_duration(y=self.y, sr=self.sr)
        print(f"Duration: {duration:.2f} seconds")
        return duration

    def calculate_tempo(self):
        duration = librosa.get_duration(y=self.y, sr=self.sr)

        avg_amplitude = np.mean(np.abs(self.y))

        tempo, beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)

        tempo = int(tempo)

        print(f"Estimated tempo: {tempo} BPM")
        return tempo

    def create_frequency_bars(self, num_bars=32):
        """
        Process an audio file using librosa and extract frequency data.
        Save the bar values to a JSON file.

        Args:
            num_bars (int): Number of frequency bars to generate

        Returns:
            bar values (list): List of bar values
        """

        chromagram = librosa.feature.chroma_stft(y=self.y, sr=self.sr)

        # Calculate bar values (similar to the JavaScript code)
        bar_values = []
        for i in range(num_bars):
            total_sum = 0
            count = 0

            # Sample from the chromagram
            for j in range(chromagram.shape[0]):  # For each pitch class
                idx = int((i / num_bars) * chromagram.shape[1])
                if idx < chromagram.shape[1]:
                    total_sum += chromagram[j, idx]
                    count += 1

            # Calculate average and append to bar values
            bar_values.append(float(total_sum / (count if count > 0 else 1)))

        # Normalize the bar values to ensure they're between 0 and 1
        # Find min and max values
        min_val = min(bar_values)
        max_val = max(bar_values)

        # Apply normalization only if there's a range to normalize
        if max_val > min_val:
            bar_values = [(val - min_val) / (max_val - min_val) for val in bar_values]

        return bar_values

    def create_spectrogram(self, tempo, n_fft=2048, hop_length=512):
        """
        Generate a spectrogram image with a color palette based on the tempo.
        - Very slow (< 70 BPM): Blue-based colors
        - Slow (70-90 BPM): Blue-green colors
        - Moderate (90-120 BPM): Green-yellow colors
        - Fast (120-150 BPM): Orange-based colors
        - Very fast (> 150 BPM): Red-based colors

        Args:
            n_fft (int): FFT window size
            hop_length (int): Number of samples between frames
            tempo (float): Tempo in BPM
        Returns:
            str: Path to the generated spectrogram image
        """

        # Define color maps based on tempo
        if tempo < 70:
            # Blue-based color scheme
            colors = [(0.031, 0.188, 0.419),    # Dark blue
                        (0.122, 0.467, 0.706),    # Medium blue
                        (0.267, 0.667, 0.871),    # Light blue
                        (0.569, 0.843, 0.941)]    # Very light blue/cyan
        elif tempo < 90:
            # Blue-green color scheme
            colors = [(0.031, 0.188, 0.419),    # Dark blue
                        (0.173, 0.459, 0.675),    # Medium blue
                        (0.224, 0.639, 0.706),    # Teal
                        (0.204, 0.796, 0.667)]    # Light green
        elif tempo < 120:
            # Green-yellow color scheme
            colors = [(0.173, 0.459, 0.675),    # Blue
                        (0.224, 0.639, 0.706),    # Teal
                        (0.298, 0.784, 0.565),    # Green
                        (0.863, 0.902, 0.243)]    # Yellow
        elif tempo < 150:
            # Orange-based color scheme
            colors = [(0.298, 0.784, 0.565),    # Green
                        (0.769, 0.843, 0.267),    # Yellow-green
                        (0.992, 0.678, 0.153),    # Orange
                        (0.957, 0.427, 0.263)]    # Red-orange
        else:  # Very fast
            # Red-based color scheme
            colors = [(0.863, 0.471, 0.184),    # Orange
                        (0.957, 0.427, 0.263),    # Red-orange
                        (0.890, 0.102, 0.110),    # Red
                        (0.698, 0.016, 0.016)]    # Dark red

        # Create custom colormap for the tempo
        custom_cmap = LinearSegmentedColormap.from_list("tempo", colors)

        # Compute spectrogram (STFT)
        D = librosa.stft(self.y, n_fft=n_fft, hop_length=hop_length)

        # Convert to power spectrogram in dB
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

        # Define min and max dB values for normalization
        min_db = -80
        max_db = 0

        # Background color: #121212
        bg_color = (0.07, 0.07, 0.07)

        # Create figure with dark background
        plt.figure(figsize=(10, 5), facecolor=bg_color)
        ax = plt.axes()
        ax.set_facecolor(bg_color)
        plt.axis('off')

        # Calculate percentile values for better color distribution
        vmin = np.percentile(S_db, 5)  # 5th percentile
        vmax = np.percentile(S_db, 95)  # 95th percentile

        # Plot spectrogram with the tempo-based colormap
        librosa.display.specshow(
            S_db,
            sr=self.sr,
            hop_length=hop_length,
            x_axis='time',
            y_axis='log',
            cmap=custom_cmap,
            vmin=vmin,
            vmax=vmax
        )

        # Remove margins and padding
        plt.tight_layout(pad=0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Save the spectrogram image
        audio_path = Path(self.audio_path)
        img_filename = audio_path.parent.parent / "site" / f"spectrogram.png"
        plt.savefig(img_filename, bbox_inches='tight', pad_inches=0, dpi=150, facecolor=bg_color)
        plt.close()

        print(f"Tempo-based spectrogram saved to {img_filename}")
        return img_filename.absolute().as_uri()
