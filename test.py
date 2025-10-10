import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

frequency = 440
duration = 3
sample_rate = 44100

sine_wave = generate_sine_wave(frequency, duration, sample_rate)

sd.play(sine_wave, sample_rate)
sd.wait()