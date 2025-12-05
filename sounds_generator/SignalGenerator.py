import numpy as np
import scipy.signal
from Signal import Signal

class SignalGenerator:
    def __init__(self, sample_rate = 44100, default_duration=2.0):
        self.sample_rate = sample_rate
        self.default_duration = default_duration
        self.generated_signal = list()

    def create_signal(self, signal_form, frequency, amplitude=1.0, duty=0.5):
        signal = Signal(signal_form, amplitude, frequency, self.default_duration, self.sample_rate)
        signal.generate(duty=duty)
        signal.save()
        self.generated_signal.append(signal)
        return signal
        
    def sum_signals(self, signal1, signal2):
        if not isinstance(signal1, Signal) or not isinstance(signal2, Signal):
            raise TypeError("Both objects must be signals")
        if signal1.sample_rate != signal2.sample_rate:
            raise ValueError("Samples rate of both signals must be equal")
        res_len = min(len(signal1.signal_data), len(signal2.signal_data))
        data1 = signal1.signal_data[:res_len]
        data2 = signal2.signal_data[:res_len]
        mixed_data = data1 + data2
        res_signal = Signal (
            signal_form = "mixed",
            ampl = 1.0,
            freq=0,
            duration=self.default_duration,
            sample_rate=self.sample_rate
        )
        res_signal.signal_data = mixed_data
        res_signal.time = signal1.time[:res_len]
        res_signal.base_name = f"Polyphonic_{signal1.base_name}_{signal2.base_name}"
        res_signal.normalize()
        res_signal.save()
        self.generated_signal.append(res_signal);
        return res_signal
    
    def modulate_signal(self, carrier, modulator, mod_type="AM", modulation_index=50.0):
        if not isinstance(carrier, Signal) or not isinstance(modulator, Signal):
            raise TypeError("Both objects must be signals")
        if carrier.sample_rate != modulator.sample_rate:
            raise ValueError("Samples rate of both signals must be equal")
            
        min_len = min(len(carrier.signal_data), len(modulator.signal_data))
        
        c_data = carrier.signal_data[:min_len]
        m_raw = modulator.signal_data[:min_len]
        max_mod = np.max(np.abs(m_raw))
        if max_mod > 0:
            m_data = m_raw / max_mod 
        else:
            m_data = m_raw
            
        time = carrier.time[:min_len]
        result_data = None

        if mod_type.upper() == "AM":
            result_data = c_data * (1.0 + 0.5 * m_data)

        elif mod_type.upper() == "FM":
            deviation = modulation_index
            instantaneous_freq = carrier.freq + (deviation * m_data)
            phase_arg = 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
            
            if carrier.signal_form == 'sine':
                result_data = np.sin(phase_arg)
            elif carrier.signal_form == 'square':
                result_data = scipy.signal.square(phase_arg, duty=0.5)
            elif carrier.signal_form == 'triangle':
                result_data = scipy.signal.sawtooth(phase_arg, width=0.5)
            elif carrier.signal_form == 'sawtooth':
                result_data = scipy.signal.sawtooth(phase_arg, width=1)
            else:
                result_data = np.sin(phase_arg)
            result_data = result_data * carrier.ampl

        else:
            raise ValueError("Modulation type must be 'AM' or 'FM'")    
        
        res_signal = Signal(
            signal_form=f"mod_{mod_type}",
            ampl=carrier.ampl,
            freq=carrier.freq,
            duration=self.default_duration,
            sample_rate=self.sample_rate
        )

        res_signal.signal_data = result_data
        res_signal.time = time
        res_signal.base_name = f"Mod_{mod_type}_{carrier.base_name}_by_{modulator.base_name}"
        
        param_str = f"Depth={modulation_index}" if mod_type.upper() == "AM" else f"Dev={modulation_index}Hz"
        res_signal.plot_name = f"{mod_type} Mod: {carrier.freq}Hz by {modulator.freq}Hz ({param_str})"
        
        res_signal.normalize()
        res_signal.save()
        self.generated_signal.append(res_signal)
        
        return res_signal
        