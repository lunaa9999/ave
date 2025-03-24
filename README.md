# Audio Visualization for Entertainment (AVE)
### Made for `Les Trophées NSI 2025`

## Description

The project is intended for amusement purposes.

This project is a simple audio visualization tool that uses the Fast Fourier Transform (FFT) to analyze the frequency spectrum of an audio signal.
The color of the visualization is predifened and is based on the BPM of the song. e.g. slow songs -> blue color, fast songs -> red color
BPM is fetched with the song's metadata. If the song does not have any metadata, the BPM is calculated by the script.

The main part of the project is written in Python. It allows the user to search for a song, it processes it and extracts all the necessary information, as well as creating a spectrogram.
Then, this information is passed to JavaScript which does the actual visualization and audio playback.


## Installation

- Clone the repository with `git clone https://github.com/lunaa9999/ave.git`
- Install the required libraries with `pip install -r requirements.txt`
- Run the script with `python main.py`

### or... just use this one-liner
```bash
git clone https://github.com/lunaa9999/ave.git && cd ave && pip install -r requirements.txt && python main.py
```


## How the project was created?

In the beginning, our team started to explore the possibilities for turning an audio signal into a visual representation. We found out that the Fast Fourier Transform (FFT) is the best way to analyze the frequency spectrum of an audio signal. We also found out that the BPM of a song can be calculated by analyzing the audio signal. We decided to use the BPM to determine the color of the visualization.
At first, we were looking for creating a static image. We thought about mapping frequencies and their amplitudes, splitting sampples into bins and assigning to pixels of an image with a fixed size.
That way, we thought, changing the initial pixel and the way we iterate through the pixels, we could create something beautiful.
But, after the initial implementation, we were not satisfied with the result.

Then, we looked at our options and settled with three types of visualizations:

- Frequency bars (just splitting the frequency spectrum into bins and drawing them)
- Spectrogram
- Pulse animation

as these were the most visually appealing and easy to implement.
One of our goals was also to make the visualization same for the same song, so we didn't use any randomization.
Also, we wanted for the colors of the visualizaiton to match the song's mood, so we decided to use the BPM for that.

In the beginning of prototyping, the whole visualization was done by the JavaScript side and Python was only used
to retrieve the data from the audio file which was stored locally.
Unfortunately, we experienced some huge performance issues. The site was being rendered for ~10 seconds or even more.

Thus, we decided to move all the audio processing to python, as well as creating the spectrogram.
In this way, we maximized the performance and minimized the data transfer between the two sides.

While one part of the team was working on the audio processing and visualization, the other part was working
on the pretty CLI and possibility to search for a song and fetch it, as well as the metadata necessary.
Locally stored files were no longer supported if they were not downloaded by the script, as the information
stored in a json file would be missing.

In the end, we combined the two parts parts, polished it a bit, wrote the docs, added some simple CI workflows
to make the code prettier and organized the GitHub repo page correctly.


## Future plans

- [ ] Add more visualizations
- [ ] Add more color schemes
- [ ] Add a more visually appealing UI and make the site more interactive (such as possibility to search for the song)


## Bugs

If you encounter any problems with the script, please, create an Issue on the GitHub page and assign it to [innerviewer](https://github.com/innerviewer).
Add such information as:

- Your platform
- Python version
- Song you were trying to visualize
- Additional steps you think are necessary to reproduce the bug


## Used Libraries
- [x] [Librosa](https://librosa.org/doc/main/index.html)
- [x] [matplotlib](https://matplotlib.org/)
- [x] [numpy](https://numpy.org/)
