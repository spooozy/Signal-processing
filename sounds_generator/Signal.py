import numpy as np
import scipy.signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, signal_form, ampl, freq, duration, sample_rate):
        self.signal_form = signal_form
        self.ampl = ampl
        self.freq = freq
        self.duration = duration
        self.sample_rate = sample_rate

        self.time = None
        self.signal_data = None
        
        self.plot_name = f"Signal: {self.signal_form.capitalize()}, {self.ampl}, {self.freq}"
        self.base_name = f"{self.signal_form}_{self.ampl}_{self.freq}"
        self.wav_filename = f"sounds/{self.base_name}.wav"
        self.plot_filename = f"plots/{self.base_name}.png"
    
    def generate(self, duty=0.5):
        self.time = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        arg = 2 * np.pi * self.freq * self.time
        if self.signal_form == 'sine':
            signal = np.sin(arg)
        elif self.signal_form == 'square':
            signal = self.square_wave(arg, duty)
        elif self.signal_form == 'triangle':
            signal = self.triangle_wave(arg)
        elif self.signal_form == 'sawtooth':
            signal = self.sawtooth_wave(arg)
        elif self.signal_form == 'noise':
            signal = np.random.uniform(-1, 1, len(self.time))
        else:
            raise ValueError("Unknown form")
        
        self.signal_data = signal * self.ampl
        return self.signal_data
    
    def square_wave(self, arg, duty=0.5):
        normalized_arg = arg % (2 * np.pi)
        threshold = duty * 2 * np.pi
        signal = np.where(normalized_arg < threshold, 1.0, -1.0)
        return signal
    
    def triangle_wave(self, arg):
        phase = (self.time * self.freq) % 1.0
        signal = 1 - 2 * np.abs(1 - 2 * phase)
        return signal

    def sawtooth_wave(self, arg):
        normalized_arg = arg % (2 * np.pi)
        phase = normalized_arg / (2 * np.pi)
        signal = 2 * phase - 1
        return signal
    
    def normalize(self):
        if self.signal_data is None:
            return
        max_val = np.max(np.abs(self.signal_data))
        if max_val > 0:
            self.signal_data = self.signal_data / max_val
            print("Signal is normalized")
    
    def save(self):
        self.save_sound()
        self.save_plot()
    
    def save_sound(self):
        if self.signal_data is None:
            print("Signal is not generated yet")
            return
        clipped_data = np.clip(self.signal_data, -1.0, 1.0)
        audio_data = (clipped_data * 32767).astype(np.int16)
        wav.write(self.wav_filename, self.sample_rate, audio_data)
        print(f"File {self.wav_filename} saved")

    def save_plot(self):
        if self.signal_data is None:
            print("Signal is not generated yet")
            return
        limit = int(self.sample_rate * 0.1)
        plt.figure(figsize=(6, 3))
        plt.plot(self.time[:limit], self.signal_data[:limit])
        plt.title(self.plot_name)
        plt.xlabel("Time (s)")
        plt.ylabel("A")
        plt.grid(True)
        plt.savefig(self.plot_filename)
        plt.close()
        print(f"File {self.plot_filename} saved")