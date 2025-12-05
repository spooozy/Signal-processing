import math

class FilterProcessor:
    def __init__(self):
        pass

    def _calculate_alpha_lp(self, cutoff, sample_rate):
        if cutoff <= 0: return 0
        dt = 1.0 / sample_rate
        rc = 1.0 / (2.0 * math.pi * cutoff)
        return dt / (rc + dt)

    def _calculate_alpha_hp(self, cutoff, sample_rate):
        if cutoff <= 0: return 1
        dt = 1.0 / sample_rate
        rc = 1.0 / (2.0 * math.pi * cutoff)
        return rc / (rc + dt)

    def apply_low_pass(self, signal, cutoff, sample_rate):
        alpha = self._calculate_alpha_lp(cutoff, sample_rate)
        
        result = [0.0] * len(signal)
        prev_y = signal[0]
        
        for i in range(len(signal)):
            x = signal[i]
            y = prev_y + alpha * (x - prev_y)
            result[i] = y
            prev_y = y
            
        return result

    def apply_high_pass(self, signal, cutoff, sample_rate):
        alpha = self._calculate_alpha_hp(cutoff, sample_rate)
        
        result = [0.0] * len(signal)
        prev_y = 0.0
        prev_x = signal[0]
        
        for i in range(len(signal)):
            x = signal[i]
            y = alpha * (prev_y + x - prev_x)
            result[i] = y
            prev_y = y
            prev_x = x
            
        return result

    def apply_band_pass(self, signal, low_cut, high_cut, sample_rate):
        step1 = self.apply_high_pass(signal, low_cut, sample_rate)
        step2 = self.apply_low_pass(step1, high_cut, sample_rate)
        return step2