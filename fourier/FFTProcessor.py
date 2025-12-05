import cmath
import math

class FFTProcessor:
    def __init__(self):
        self.spectrum = []

    def compute_fft(self, signal):
        n = len(signal)
        if (n & (n - 1) == 0) and n > 0:
            padded_signal = signal
        else:
            next_pow2 = 1
            while next_pow2 < n:
                next_pow2 *= 2
            padded_signal = list(signal) + [0] * (next_pow2 - n)
        self.spectrum = self._fft_recursive(padded_signal)
        return self.spectrum

    def _fft_recursive(self, x):
        N = len(x)
        if N <= 1:
            return x
        even = self._fft_recursive(x[0::2])
        odd =  self._fft_recursive(x[1::2])
        combined = [0] * N
        
        for k in range(N // 2):
            angle = -2j * math.pi * k / N
            t = cmath.exp(angle) * odd[k]
            combined[k] = even[k] + t
            combined[k + N // 2] = even[k] - t
        return combined

    def compute_ifft(self, spectrum=None):
        if spectrum is None:
            spectrum = self.spectrum
        
        if not spectrum:
            return []

        N = len(spectrum)
        conjugated_spectrum = [x.conjugate() for x in spectrum]
        transformed = self._fft_recursive(conjugated_spectrum)
        restored_signal = []
        for val in transformed:
            res = val.conjugate().real / N
            restored_signal.append(res)
            
        return restored_signal

    def get_amplitude_spectrum(self):
        if not self.spectrum:
            return []
        return [abs(val) for val in self.spectrum]

    def get_phase_spectrum(self):
        if not self.spectrum:
            return []
        return [cmath.phase(val) for val in self.spectrum]