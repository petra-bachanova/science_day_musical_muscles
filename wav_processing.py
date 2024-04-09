import pandas as pd
import seaborn as sns
import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram
import sounddevice as sd


def extract_dominant_frequency(wav_file, window_size=1):
    # Read the wav file
    sample_rate, data = wavfile.read(wav_file)

    # Calculate the number of samples in each 2-second window
    samples_per_window = int(window_size * sample_rate)

    # Calculate the number of windows
    num_windows = len(data) // samples_per_window

    dominant_freqs = []

    # Iterate through each 2-second window
    for i in range(num_windows):
        # Extract the segment of data for the current window
        window_data = data[i * samples_per_window: (i + 1) * samples_per_window]

        # Calculate the spectrogram of the windowed data
        f, t, Sxx = spectrogram(window_data, fs=sample_rate, nperseg=samples_per_window)

        # Find the index of the maximum amplitude frequency
        dominant_freq_index = np.argmax(Sxx, axis=0)

        # Get the dominant frequency for the current window
        dominant_freq = float(f[dominant_freq_index])

        # Append the dominant frequency to the list
        dominant_freqs.append(dominant_freq)

    return dominant_freqs


# Example usage:
file = 'wav files/Grace.wav'
dominant_frequencies = extract_dominant_frequency(file)
print(dominant_frequencies)

# Function to play a single frequency
def play_frequency(frequency, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    sd.play(waveform, samplerate=sample_rate)
    sd.wait()


# Play each dominant frequency for 1 second
for freq in dominant_frequencies:
    play_frequency(freq, duration=1)


