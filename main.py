import numpy as np
from scipy import signal
from scipy.io import wavfile
import os

def ensure_sounds_directory():
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
        print("Создана папка 'sounds'")

def generate_sine_wave(freq, duration, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def generate_pulse_wave(freq, duration, duty_cycle, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.square(2 * np.pi * freq * t, duty=duty_cycle)
    return wave

def generate_triangle_wave(freq, duration, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.sawtooth(2 * np.pi * freq * t, width=0.5)
    return wave

def generate_sawtooth_wave(freq, duration, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.sawtooth(2 * np.pi * freq * t, width=1)
    return wave

def generate_noise(duration, amplitude=0.5, sample_rate=44100):
    samples = int(sample_rate * duration)
    wave = amplitude * np.random.uniform(-1, 1, samples)
    return wave

def save_waveform(wave, filename):
    if not filename.startswith("sounds/"):
        filename = os.path.join("sounds", filename)
    
    if not filename.lower().endswith('.wav'):
        filename += '.wav'
    
    wavfile.write(filename, 44100, (wave * 32767).astype(np.int16))
    print(f"Файл сохранен как: {filename}")

def get_amplitude_input(prompt, default=0.5):
    while True:
        try:
            amplitude = float(input(prompt) or default)
            if 0.1 <= amplitude <= 1.0:
                return amplitude
            else:
                print("Амплитуда должна быть в диапазоне от 0.1 до 1.0")
        except ValueError:
            print("Пожалуйста, введите число")

def generate_polyphonic_signal():
    print("\n--- Генерация полифонического сигнала ---")
    
    duration = float(input("Длительность сигнала (сек) [2]: ") or "2")
    num_signals = int(input("Количество монофонических сигналов для суммирования [2]: ") or "2")
    filename = input("Имя файла [polyphonic.wav]: ") or "polyphonic.wav"

    sample_rate = 44100
    total_samples = int(sample_rate * duration)
    poly_signal = np.zeros(total_samples)
    
    for i in range(num_signals):
        print(f"\n--- Сигнал {i+1} из {num_signals} ---")
        print("Выберите тип сигнала:")
        print("1. Синусоида")
        print("2. Импульс (прямоугольный)")
        print("3. Треугольный")
        print("4. Пилообразный")
        print("5. Шум")
        
        choice = input("Ваш выбор (1-5): ").strip()
        amplitude = get_amplitude_input(f"Амплитуда сигнала {i+1} (0.1-1.0) [0.3]: ", 0.3)
        
        if choice == "1":
            freq = float(input("Частота (Гц) [440]: ") or "440")
            signal_wave = generate_sine_wave(freq, duration, amplitude)
        elif choice == "2":
            freq = float(input("Частота (Гц) [440]: ") or "440")
            duty_cycle = float(input("Скважность (0.1-0.9) [0.5]: ") or "0.5")
            signal_wave = generate_pulse_wave(freq, duration, duty_cycle, amplitude)
        elif choice == "3":
            freq = float(input("Частота (Гц) [440]: ") or "440")
            signal_wave = generate_triangle_wave(freq, duration, amplitude)
        elif choice == "4":
            freq = float(input("Частота (Гц) [440]: ") or "440")
            signal_wave = generate_sawtooth_wave(freq, duration, amplitude)
        elif choice == "5":
            signal_wave = generate_noise(duration, amplitude)
        else:
            print("Неверный выбор! Используется синусоида по умолчанию")
            freq = 440
            signal_wave = generate_sine_wave(freq, duration, amplitude)
        
        poly_signal += signal_wave
    
    max_amplitude = np.max(np.abs(poly_signal))
    if max_amplitude > 1.0:
        poly_signal = poly_signal / max_amplitude
        print(f"Выполнена нормализация амплитуды (максимум был {max_amplitude:.2f})")
    
    return poly_signal, filename

def main():
    ensure_sounds_directory()
    
    while True:
        print("\n" + "="*50)
        print("        ГЕНЕРАТОР ЗВУКОВЫХ СИГНАЛОВ")
        print("="*50)
        print("1. Синусоида")
        print("2. Импульс (прямоугольный)")
        print("3. Треугольный")
        print("4. Пилообразный")
        print("5. Шум")
        print("6. Полифонический сигнал (сумма нескольких сигналов)")
        print("0. Выход")
        print("-"*50)
        
        choice = input("Выберите тип сигнала (0-6): ").strip()
        
        if choice == "0":
            print("Выход из программы.")
            break
            
        elif choice == "1":
            print("\n--- Синусоидальный сигнал ---")
            freq = float(input("Частота (Гц) [440]: ") or "440")
            duration = float(input("Длительность (сек) [2]: ") or "2")
            amplitude = get_amplitude_input("Амплитуда (0.1-1.0) [0.5]: ", 0.5)
            filename = input("Имя файла [sine.wav]: ") or "sine.wav"
            
            wave = generate_sine_wave(freq, duration, amplitude)
            save_waveform(wave, filename)
            
        elif choice == "2":
            print("\n--- Импульсный сигнал ---")
            freq = float(input("Частота (Гц) [440]: ") or "440")
            duration = float(input("Длительность (сек) [2]: ") or "2")
            duty_cycle = float(input("Скважность (0.1-0.9) [0.5]: ") or "0.5")
            amplitude = get_amplitude_input("Амплитуда (0.1-1.0) [0.5]: ", 0.5)
            filename = input("Имя файла [pulse.wav]: ") or "pulse.wav"
            
            wave = generate_pulse_wave(freq, duration, duty_cycle, amplitude)
            save_waveform(wave, filename)
            
        elif choice == "3":
            print("\n--- Треугольный сигнал ---")
            freq = float(input("Частота (Гц) [440]: ") or "440")
            duration = float(input("Длительность (сек) [2]: ") or "2")
            amplitude = get_amplitude_input("Амплитуда (0.1-1.0) [0.5]: ", 0.5)
            filename = input("Имя файла [triangle.wav]: ") or "triangle.wav"
            
            wave = generate_triangle_wave(freq, duration, amplitude)
            save_waveform(wave, filename)
            
        elif choice == "4":
            print("\n--- Пилообразный сигнал ---")
            freq = float(input("Частота (Гц) [440]: ") or "440")
            duration = float(input("Длительность (сек) [2]: ") or "2")
            amplitude = get_amplitude_input("Амплитуда (0.1-1.0) [0.5]: ", 0.5)
            filename = input("Имя файла [sawtooth.wav]: ") or "sawtooth.wav"
            
            wave = generate_sawtooth_wave(freq, duration, amplitude)
            save_waveform(wave, filename)
            
        elif choice == "5":
            print("\n--- Шум ---")
            duration = float(input("Длительность (сек) [2]: ") or "2")
            amplitude = get_amplitude_input("Амплитуда (0.1-1.0) [0.5]: ", 0.5)
            filename = input("Имя файла [noise.wav]: ") or "noise.wav"
            
            wave = generate_noise(duration, amplitude)
            save_waveform(wave, filename)
            
        elif choice == "6":
            wave, filename = generate_polyphonic_signal()
            save_waveform(wave, filename)
            
        else:
            print("Неверный выбор! Попробуйте снова.")

        continue_choice = input("\nСгенерировать еще один сигнал? (y/n): ").lower()
        if continue_choice != 'y':
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main()