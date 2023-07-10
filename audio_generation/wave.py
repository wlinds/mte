import numpy as np
import sounddevice as sd

def generate_waveform(frequency, waveform_type, duration=1, sampling_rate=44100) -> np.ndarray:
    """
    Generates a waveform of a specified frequency and type. Supports sine and square.
    #TODO: Add sawtooth?
    """

    # time array from 0 to duration
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)

    if waveform_type == 'sine':
        x = np.sin(2 * np.pi * frequency * t)
    elif waveform_type == 'square':
        x = np.sign(np.sin(2 * np.pi * frequency * t))
    else:
        raise ValueError('Choose either "sine" or "square".')

    # Normalize
    x = x / np.max(np.abs(x))

    return x

if __name__ == "__main__":
    # Sine wave @ 440 Hz
    f = 440
    x = generate_waveform(f, 'sine')
    sd.play(x)
    
    sd.wait()

    # Square wave @ 880 Hz
    f = 880
    x = generate_waveform(f, 'square')
    sd.play(x)

    sd.wait()