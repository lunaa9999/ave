document.addEventListener('DOMContentLoaded', function() {
    // Afficher les informations de base
    document.getElementById('filename').textContent = audioData.filename;
    document.getElementById('duration').textContent = `${audioData.duration.toFixed(2)} secondes`;
    document.getElementById('tempo').textContent = `${Math.round(audioData.tempo)} BPM`;
    
    // Créer visualisation de fréquence
    createFrequencyViz();
    
    // Créer spectrogramme
    createSpectrogram();
    
    // Créer animation réactive
    createPulseAnimation();
    
    function createFrequencyViz() {
        const container = document.getElementById('frequency-viz');
        const numBars = 32;
        
        // Utiliser les données du chromagramme pour les barres de fréquence
        const chromaData = audioData.chromagram;
        
        // Moyenne des données pour chaque barre
        const barValues = [];
        
        for (let i = 0; i < numBars; i++) {
            // Calculer une valeur moyenne pour chaque barre
            let sum = 0;
            let count = 0;
            
            // Prendre des échantillons du chromagramme 
            for (let j = 0; j < chromaData.length; j++) {
                const idx = Math.floor((i / numBars) * chromaData[j].length);
                if (idx < chromaData[j].length) {
                    sum += chromaData[j][idx];
                    count++;
                }
            }
            
            barValues.push(sum / (count || 1));
        }
        
        // Normaliser les valeurs
        const maxVal = Math.max(...barValues);
        const normValues = barValues.map(val => val / maxVal);
        
        // Créer les barres
        for (let i = 0; i < numBars; i++) {
            const bar = document.createElement('div');
            bar.className = 'freq-bar';
            bar.style.height = `${normValues[i] * 200}px`;
            container.appendChild(bar);
        }
    }
    
    function createSpectrogram() {
        const canvas = document.getElementById('spectrogram');
        const ctx = canvas.getContext('2d');
        
        const spectrogramData = audioData.spectrogram.data;
        const timeFrames = audioData.spectrogram.time_bins;
        const freqBins = audioData.spectrogram.freq_bins;
        
        // Ajuster la taille du canvas
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        
        // Dessiner le spectrogramme
        const blockWidth = canvas.width / timeFrames;
        const blockHeight = canvas.height / freqBins;
        
        for (let t = 0; t < timeFrames; t++) {
            for (let f = 0; f < freqBins; f++) {
                // Normaliser les valeurs entre 0 et 1
                let value = spectrogramData[f][t];
                
                // Convertir en valeur entre 0 et 1
                const minDb = -80;
                const maxDb = 0;
                value = (value - minDb) / (maxDb - minDb);
                value = Math.max(0, Math.min(1, value));
                
                // Créer une couleur basée sur la valeur
                const hue = 240 - value * 240; // Bleu (240) à rouge (0)
                ctx.fillStyle = `hsl(350, 100%, ${20 + value * 50}%)`;
                
                ctx.fillRect(
                    t * blockWidth, 
                    canvas.height - (f + 1) * blockHeight, // Inverser pour que les basses fréquences soient en bas
                    blockWidth, 
                    blockHeight
                );
            }
        }
    }
    
    function createPulseAnimation() {
        const container = document.getElementById('pulse-container');
        const beats = audioData.beats;
        
        // Créer plusieurs cercles pulsants basés sur les temps forts
        const numBeats = Math.min(10, beats.length);
        for (let i = 0; i < numBeats; i++) {
            const beatTime = beats[i];
            const delay = i * 0.4; // Délai pour l'animation
            
            const circle = document.createElement('div');
            circle.className = 'pulse-circle';
            
            // Position aléatoire
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            
            circle.style.left = `${x}%`;
            circle.style.top = `${y}%`;
            circle.style.animationDelay = `${delay}s`;
            
            container.appendChild(circle);
        }
    }
});
