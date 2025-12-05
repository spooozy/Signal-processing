import numpy as np
import scipy.io.wavfile as wav
import winsound
import os

class HarryPotterTheme:
    def __init__(self, sample_rate=44100, filename="harry_potter/theme.wav"):
        self.sample_rate = sample_rate
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        self.notes_freq = {
            'B3': 246.94,
            'E4': 329.63,
            'G4': 392.00,
            'F#4': 369.99,
            'F4': 349.23,
            'B4': 493.88,
            'A4': 440.00,
            'D#4': 311.13,
        }

        self.melody = [
            ('B3', 0.5),
            ('E4', 0.75),
            ('G4', 0.25),
            ('F#4', 0.5),
            ('E4', 1.0),
            ('B4', 0.5),
            ('A4', 1.5),
            ('F#4', 1.5),
            ('E4', 0.75),
            ('G4', 0.25),
            ('F#4', 0.5),
            ('D#4', 1.0),
            ('F4', 0.5),
            ('B3', 1.5)
        ]

    def _generate_note_wave(self, freq, duration):
        freq = freq * 8

        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        
        wave = np.sin(2 * np.pi * freq * t)
        wave += 0.5 * np.sin(2 * np.pi * (freq * 2) * t) 
        
        total_samples = len(t)
        attack_len = int(0.05 * self.sample_rate)
        release_len = int(0.3 * self.sample_rate)
        
        envelope = np.ones(total_samples)
        
        if total_samples > attack_len:
            envelope[:attack_len] = np.linspace(0, 1, attack_len)
        
        if total_samples > release_len:
            envelope[-release_len:] = np.linspace(1, 0, release_len)
        else:
            envelope = np.linspace(1, 0, total_samples)

        return wave * envelope * 0.5

    def generate(self):
        full_song = []

        for note, duration in self.melody:
            if note in self.notes_freq:
                wave = self._generate_note_wave(self.notes_freq[note], duration)
                full_song.append(wave)
            else:
                full_song.append(np.zeros(int(duration * self.sample_rate)))
            full_song.append(np.zeros(int(0.05 * self.sample_rate)))

        combined_signal = np.concatenate(full_song)

        max_val = np.max(np.abs(combined_signal))
        if max_val > 0:
            combined_signal = combined_signal / max_val
        
        audio_data = (combined_signal * 32767).astype(np.int16)
        wav.write(self.filename, self.sample_rate, audio_data)
        
        return self.filename

    def play(self):
        try:
            self.stop()
            file_path = self.generate()
            winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def stop(self):
        winsound.PlaySound(None, winsound.SND_PURGE)