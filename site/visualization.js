document.addEventListener("DOMContentLoaded", function () {
  // Afficher les informations de base
  document.getElementById("name").textContent =
    audioData.title || "Titre inconnu";
  document.getElementById("artist").textContent =
    audioData.artist || "Artiste inconnu";

  if (audioData.tempo == NaN) {
    document.getElementById("tempo").textContent = "Tempo non trouvé";
  } else {
    document.getElementById("tempo").textContent =
      `${Math.round(audioData.tempo)} BPM`;
  }

  createFrequencyViz();
  displaySpectrogram();
  createPulseAnimation();

  function createFrequencyViz() {
    const container = document.getElementById("frequency-viz");
    const barValues = audioData.barValues;
    const tempo = audioData.tempo;
    container.innerHTML = "";

    container.style.display = "flex";
    container.style.alignItems = "flex-end";
    container.style.height = "200px";
    container.style.width = "100%";

    const tempoDescription =
      tempo < 70
        ? "Very slow"
        : tempo < 90
          ? "Slow"
          : tempo < 120
            ? "Moderate"
            : tempo < 150
              ? "Fast"
              : "Very fast";

    // small tempo label to container
    const tempoLabel = document.createElement("div");
    tempoLabel.textContent = `${tempoDescription}: ${tempo.toFixed(1)} BPM`;
    tempoLabel.style.position = "absolute";
    tempoLabel.style.top = "5px";
    tempoLabel.style.left = "10px";
    tempoLabel.style.color = "rgba(255, 255, 255, 0.7)";
    tempoLabel.style.fontSize = "12px";
    container.appendChild(tempoLabel);

    let colorStart, colorEnd;

    if (tempoDescription === "Very slow") {
      // Blue-based colors
      colorStart = { h: 220, s: 75, l: 40 }; // Dark blue
      colorEnd = { h: 195, s: 80, l: 75 }; // Light blue/cyan
    } else if (tempoDescription === "Slow") {
      // Blue-green colors
      colorStart = { h: 220, s: 75, l: 40 }; // Dark blue
      colorEnd = { h: 170, s: 75, l: 65 }; // Light green
    } else if (tempoDescription === "Moderate") {
      // Green-yellow colors
      colorStart = { h: 200, s: 60, l: 55 }; // Blue
      colorEnd = { h: 65, s: 75, l: 60 }; // Yellow
    } else if (tempoDescription === "Fast") {
      // Orange-based colors
      colorStart = { h: 120, s: 60, l: 55 }; // Green
      colorEnd = { h: 20, s: 90, l: 55 }; // Red-orange
    } else {
      // Red-based colors
      colorStart = { h: 30, s: 80, l: 50 }; // Orange
      colorEnd = { h: 0, s: 95, l: 40 }; // Dark red
    }

    // Calculate bar width based on container width and number of bars
    const barWidth = 100 / barValues.length;

    // Create visualization bars
    barValues.forEach((value, index) => {
      // Scale bar height (values should already be normalized between 0-1)
      // Minimum height of 5% so bars are always visible
      const barHeight = Math.max(5, value * 100);

      // Interpolate color based on value
      const hue = colorStart.h - (colorStart.h - colorEnd.h) * value;
      const saturation = colorStart.s + (colorEnd.s - colorStart.s) * value;
      const lightness = colorStart.l + (colorEnd.l - colorStart.l) * value;

      // Create and style each bar
      const bar = document.createElement("div");
      bar.style.width = `${barWidth}%`;
      bar.style.height = `${barHeight}%`;
      bar.style.backgroundColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
      bar.style.margin = "0 1px";

      // Add the bar to the container
      container.appendChild(bar);
    });
  }

  function displaySpectrogram() {
    if (!audioData || !audioData.spectrogramUri) {
      console.error("No spectrogram data available");
      return;
    }

    const spectrogramContainer = document.querySelector(".spectrogram-wrapper");

    if (spectrogramContainer) {
      spectrogramContainer.innerHTML = "";

      const spectrogramImg = document.createElement("img");
      spectrogramImg.src = audioData.spectrogramUri;
      spectrogramImg.id = "spectrogram-img";
      spectrogramImg.style.width = "100%";
      spectrogramImg.style.height = "auto";

      spectrogramImg.onload = () => {
        console.log("Spectrogram loaded successfully.");
      };

      spectrogramImg.onerror = (e) => {
        console.error("Error loading the spectrogram:", e);
        spectrogramContainer.innerHTML =
          "<p>Erreur de chargement du spectrogramme</p>";
      };

      spectrogramContainer.appendChild(spectrogramImg);
    } else {
      console.error("Spectrogram container not found");
    }
  }

  function setDynamicHeadingColors(colors) {
    // Select all h1 and h2 elements
    const headings = document.querySelectorAll('h1, h2');
    
    // Create a linear gradient with the provided colors
    const gradient = `linear-gradient(to right, ${colors[0]}, ${colors[1]}, ${colors[2]}, ${colors[3]})`;
    
    // Create a style tag to apply the gradient text color
    const styleTag = document.createElement('style');
    styleTag.textContent = `
      h1, h2 {
        background: ${gradient};
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    text-align: center;
      }
    `;
    document.head.appendChild(styleTag);
  }

  function createPulseAnimation() {
    // Get container and clear any existing pulse circles
    const container = document.getElementById("pulse-container");
    container.innerHTML = "";

    // Get volume slider and display elements
    const volumeSlider = document.getElementById("volume-slider");
    const volumeValue = document.getElementById("volume-value");

    const audioElement = new Audio(audioData.audio_uri);
    audioElement.volume = parseFloat(volumeSlider.value) / 100;
    audioElement.controls = false;
    audioElement.autoplay = true;
	
	  // Volume slider event listener
    volumeSlider.addEventListener("input", function() {
      const volume = parseFloat(this.value) / 100;
      audioElement.volume = volume;
      volumeValue.textContent = `${this.value}%`;
    });


    // Get tempo from audioData
    const tempo = audioData.tempo || 120; // Default to 120 if not available

    // Calculate how many milliseconds between pulses (60000 ms / tempo = ms per beat)
    const msBetweenPulses = 60000 / tempo;

    // Define color palettes based on tempo
    let colors;
    if (tempo < 70) {
      // Blue-based color scheme
      colors = [
        "rgb(8, 48, 107)", // Dark blue
        "rgb(31, 119, 180)", // Medium blue
        "rgb(68, 170, 222)", // Light blue
        "rgb(145, 215, 240)", // Very light blue/cyan
      ];
    } else if (tempo < 90) {
      // Blue-green color scheme
      colors = [
        "rgb(8, 48, 107)", // Dark blue
        "rgb(44, 117, 172)", // Medium blue
        "rgb(57, 163, 180)", // Teal
        "rgb(52, 203, 170)", // Light green
      ];
    } else if (tempo < 120) {
      // Green-yellow color scheme
      colors = [
        "rgb(44, 117, 172)", // Blue
        "rgb(57, 163, 180)", // Teal
        "rgb(76, 200, 144)", // Green
        "rgb(220, 230, 62)", // Yellow
      ];
    } else if (tempo < 150) {
      // Orange-based color scheme
      colors = [
        "rgb(76, 200, 144)", // Green
        "rgb(196, 215, 68)", // Yellow-green
        "rgb(253, 173, 39)", // Orange
        "rgb(244, 109, 67)", // Red-orange
      ];
    } else {
      // Red-based color scheme
      colors = [
        "rgb(220, 120, 47)", // Orange
        "rgb(244, 109, 67)", // Red-orange
        "rgb(227, 26, 28)", // Red
        "rgb(178, 4, 4)", // Dark red
      ];
    }

    setDynamicHeadingColors(colors);

    // Dynamically set volume slider gradient
    volumeSlider.style.background = `linear-gradient(to right, ${colors[0]}, ${colors[1]}, ${colors[2]}, ${colors[3]})`;
    volumeSlider.style.backgroundImage = `linear-gradient(to right, ${colors[0]}, ${colors[1]}, ${colors[2]}, ${colors[3]})`;

    // Set slider thumb color to be the middle color
    volumeSlider.style.setProperty('--thumb-color', colors[1]);

    // Inject a style to handle the thumb color
    const styleTag = document.createElement('style');
    styleTag.textContent = `
      #volume-slider::-webkit-slider-thumb {
        background: ${colors[1]} !important;
      }
      #volume-slider::-moz-range-thumb {
        background: ${colors[1]} !important;
      }
    `;
    document.head.appendChild(styleTag);

    // Function to create a pulse circle
    function createPulseCircle() {
      const circle = document.createElement("div");
      circle.className = "pulse-circle";

      // Position aléatoire
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      circle.style.left = `${x}%`;
      circle.style.top = `${y}%`;

      // Random size (variety)
      const size = 50 + Math.random() * 50; // 50-100px
      circle.style.width = `${size}px`;
      circle.style.height = `${size}px`;

      // Assign a random color from the palette
      const colorIndex = Math.floor(Math.random() * colors.length);
      circle.style.backgroundColor = colors[colorIndex];

      // For the pulse effect, use a different color for the box-shadow
      const glowColor = colors[(colorIndex + 1) % colors.length];
      circle.style.boxShadow = `0 0 20px 10px ${glowColor}`;

      // Add to container
      container.appendChild(circle);

      // Remove the circle after animation completes (default 2s)
      setTimeout(() => {
        circle.remove();
      }, 2000);
    }

    // Start creating pulse circles at the tempo rate
    const pulseInterval = setInterval(createPulseCircle, msBetweenPulses);

    // Stop the animation when the audio ends
    audioElement.onended = () => {
      clearInterval(pulseInterval);
    };

    // Add some initial circles to start
    for (let i = 0; i < 5; i++) {
      setTimeout(createPulseCircle, i * 200);
    }

    // Append audio to document (can be hidden with CSS)
    document.body.appendChild(audioElement);

    return {
      stop: () => {
        clearInterval(pulseInterval);
        audioElement.pause();
        audioElement.remove();
      },
    };
  }
});
