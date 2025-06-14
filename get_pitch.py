from collections import deque

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
DURATION = 0.1  # in seconds
MOVING_AVG_WINDOW = 1  # Number of samples for moving average

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def freq_to_note(freq):
    if freq == 0:
        return None, None
    A4 = 440.0
    n = int(round(12 * np.log2(freq / A4)))
    note_number = n + 69
    octave = note_number // 12 - 1
    note_index = note_number % 12
    return NOTE_NAMES[note_index], octave


def detect_pitch(audio):
    audio = audio * np.hanning(len(audio))  # smooth edges
    fft = np.fft.rfft(audio)
    freq_bins = np.fft.rfftfreq(len(audio), 1 / SAMPLE_RATE)
    magnitude = np.abs(fft)
    peak_idx = np.argmax(magnitude)
    return freq_bins[peak_idx], magnitude[peak_idx]


print("Listening... Press Ctrl+C to stop.")

with open("pitch.txt", "w") as f:
    pass

freq_history = deque(maxlen=MOVING_AVG_WINDOW)

try:
    while True:
        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        audio = audio.flatten()
        freq, magnitude = detect_pitch(audio)
        freq_history.append(freq)
        avg_freq = np.mean(freq_history)
        note, octave = freq_to_note(avg_freq)

        with open("pitch.txt", "a") as f:
            f.write(f"{avg_freq},{magnitude},{note},{octave}\n")
except KeyboardInterrupt:
    print("Stopped.")
