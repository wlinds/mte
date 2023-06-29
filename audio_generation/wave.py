import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# sampling rate and the duratio
fs = 44100 # Hz
duration = 5 # seconds

# time array from 0 to duration
t = np.linspace(0, duration, int(duration * fs), endpoint=False)

# Sawtooth wave @ 440 Hz
f = 440
x = np.mod(f * t, 1) - 0.5

# Normalize
x = x / np.max(np.abs(x))

if __name__ == "__main__":
    sd.play(x, fs)
    sd.wait()