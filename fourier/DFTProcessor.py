import math
import cmath

class DFTProcessor:
    def __init__(self):
        self.spectrum = []

    def compute_dft(self, signal):
        N = len(signal)
        self.spectrum = [0j] * N
        for k in range(N):
            re_sum = 0.0
            im_sum = 0.0
            for n in range(N):
                angle = (2 * math.pi * k * n) / N
                re_sum += signal[n] * math.cos(angle)
                im_sum -= signal[n] * math.sin(angle)
            
            self.spectrum[k] = complex(re_sum, im_sum)
            
        return self.spectrum

    def compute_idft(self, spectrum=None):
        if spectrum is None:
            spectrum = self.spectrum

        N = len(spectrum)
        restored_signal = [0.0] * N

        for n in range(N):
            re_sum = 0.0
            
            for k in range(N):
                angle = (2 * math.pi * k * n) / N
                
                X_k = spectrum[k]
                re_sum += (X_k.real * math.cos(angle)) - (X_k.imag * math.sin(angle))
            
            restored_signal[n] = re_sum / N
            
        return restored_signal

    def get_amplitude_spectrum(self):
        if not self.spectrum:
            return []
        return [abs(val) for val in self.spectrum]

    def get_phase_spectrum(self):
        if not self.spectrum:
            return []
        return [cmath.phase(val) for val in self.spectrum]