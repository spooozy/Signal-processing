import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import winsound
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt

from DFTProcessor import DFTProcessor
from FFTProcessor import FFTProcessor
from FilterProcessor import FilterProcessor

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Signal Analysis Tool")
        self.geometry("1400x750")
        self.resizable(False, False)
        
        self.base_signal_data = [] 
        self.sample_rate = 44100
        self.dft_result = None
        
        self.base_name = ""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.join(self.base_dir, "src", "sounds")
        self.plots_dir = os.path.join(self.base_dir, "src", "plots")

        self.DFTProcessor = DFTProcessor()
        self.FFTProcessor = FFTProcessor()
        self.FilterProcessor = FilterProcessor()

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.columnconfigure(2, weight=1, uniform="group1")
        self.columnconfigure(3, weight=1, uniform="group1")
        
        self.rowconfigure(0, weight=1)
        
        self.frame_1 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_1.grid(row=0, column=0, sticky="nsew")
        
        self.frame_2 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_2.grid(row=0, column=1, sticky="nsew")
        
        self.frame_3 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_3.grid(row=0, column=2, sticky="nsew")

        self.frame_4 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_4.grid(row=0, column=3, sticky="nsew")

        ttk.Label(self.frame_1, text="BASE", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_2, text="DFT", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_3, text="FFT", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_4, text="FILTER", font=("Arial", 12, "bold")).pack(pady=10)

        self.create_source_widgets()
        self.create_dft_widgets()
        self.create_fft_widgets()
        self.create_filter_widgets()

    def create_source_widgets(self):
        files = self.get_sound_files()
        lbl_select = ttk.Label(self.frame_1, text="Choose sound:")
        lbl_select.pack(anchor="w", pady=(0, 5))
        
        self.combo_sounds = ttk.Combobox(self.frame_1, values=files, state="readonly")
        self.combo_sounds.pack(fill='x', pady=5)
        self.combo_sounds.bind("<<ComboboxSelected>>", self.on_sound_selected)
        
        if files:
            self.combo_sounds.current(0)
            
        self.btn_play = ttk.Button(self.frame_1, text="PLAY", state="disabled", 
                                   command=lambda: self.play_sound(os.path.join(self.sounds_dir, self.combo_sounds.get())))
        self.btn_play.pack(pady=10, fill='x')
        
        self.base_plot_container = ttk.LabelFrame(self.frame_1, text="Base Plot (Full)", padding=5)
        self.base_plot_container.pack(pady=5, fill='x')
        self.base_plot_label = ttk.Label(self.base_plot_container, text="No plot")
        self.base_plot_label.pack(pady=5)

        self.used_plot_container = ttk.LabelFrame(self.frame_1, text="Used Slice (Zoom)", padding=5)
        self.used_plot_container.pack(pady=5, fill='x')
        
        self.used_plot_label = ttk.Label(self.used_plot_container, text="Slice plot")
        self.used_plot_label.pack(pady=5)

    def create_dft_widgets(self):
        self.transform_container = ttk.LabelFrame(self.frame_2, text="DF transform", padding=5)
        self.transform_container.pack(pady=5, fill='both')

        self.transform_btn = ttk.Button(self.transform_container, state="disabled", text="TRANSFORM", command=self.on_dft_pressed)
        self.transform_btn.pack(pady=5, fill='x')

        self.ampl_spectrum_lbl = ttk.Label(self.transform_container, text="Amplitude spectrum")
        self.ampl_spectrum_lbl.pack(pady=5)

        self.phase_spectrum_lbl = ttk.Label(self.transform_container, text="Phase spectrum")
        self.phase_spectrum_lbl.pack(pady=2)

        self.restore_container = ttk.LabelFrame(self.frame_2, text="DF restore", padding=5)
        self.restore_container.pack(pady=5, fill='both')

        self.restore_plot_lbl = ttk.Label(self.restore_container, text="Restored plot")
        self.restore_plot_lbl.pack(pady=5)      

    def create_fft_widgets(self):
        self.fft_container = ttk.LabelFrame(self.frame_3, text="FF transform", padding=5)
        self.fft_container.pack(pady=5, fill='both')

        self.fft_btn = ttk.Button(self.fft_container, state="disabled", text="TRANSFORM", command=self.on_fft_pressed)
        self.fft_btn.pack(pady=5, fill='x')
        self.fft_amp_lbl = ttk.Label(self.fft_container, text="Amp Spectrum")
        self.fft_amp_lbl.pack(pady=2)

        self.fft_phase_lbl = ttk.Label(self.fft_container, text="Phase Spectrum")
        self.fft_phase_lbl.pack(pady=2)

        self.fft_restore_frame = ttk.LabelFrame(self.frame_3, text="FF restore", padding=5)
        self.fft_restore_frame.pack(pady=5, fill='both')

        self.fft_restored_lbl = ttk.Label(self.fft_restore_frame, text="Restored")
        self.fft_restored_lbl.pack(pady=5)

    def create_filter_widgets(self):
        self.filter_container = ttk.LabelFrame(self.frame_4, text="Filter Settings", padding=5)
        self.filter_container.pack(pady=5, fill='both')

        # 1. Выбор типа фильтра
        lbl_type = ttk.Label(self.filter_container, text="Type:")
        lbl_type.pack(anchor="w")
        self.combo_filter = ttk.Combobox(self.filter_container, values=["Low Pass", "High Pass", "Band Pass"], state="readonly")
        self.combo_filter.current(0)
        self.combo_filter.pack(fill='x', pady=2)

        input_frame = ttk.Frame(self.filter_container)
        input_frame.pack(fill='x', pady=5)

        lbl_f1 = ttk.Label(input_frame, text="Freq 1 (Hz):")
        lbl_f1.pack(anchor="w")
        self.entry_cutoff1 = ttk.Entry(input_frame)
        self.entry_cutoff1.insert(0, "1000") 
        self.entry_cutoff1.pack(fill='x', pady=(0, 5))

        lbl_f2 = ttk.Label(input_frame, text="Freq 2 (Hz) [BandPass only]:")
        lbl_f2.pack(anchor="w")
        self.entry_cutoff2 = ttk.Entry(input_frame)
        self.entry_cutoff2.insert(0, "5000")
        self.entry_cutoff2.pack(fill='x')

        self.btn_filter = ttk.Button(self.filter_container, text="APPLY FILTER", state="disabled", command=self.on_filter_pressed)
        self.btn_filter.pack(pady=10, fill='x')

        self.filter_res_frame = ttk.LabelFrame(self.frame_4, text="Result", padding=5)
        self.filter_res_frame.pack(pady=5, fill='both')

        self.filter_time_lbl = ttk.Label(self.filter_res_frame, text="Time Domain")
        self.filter_time_lbl.pack(pady=2)

        self.filter_freq_lbl = ttk.Label(self.filter_res_frame, text="Freq Domain")
        self.filter_freq_lbl.pack(pady=2)

    def get_sound_files(self):
        if not os.path.exists(self.sounds_dir):
            try:
                os.makedirs(self.sounds_dir)
                os.makedirs(self.plots_dir)
            except:
                pass
            return []
        return [f for f in os.listdir(self.sounds_dir) if f.lower().endswith('.wav')]
    
    def on_sound_selected(self, event):
        selected_file = self.combo_sounds.get()
        if not selected_file:
            return
            
        self.base_name = os.path.splitext(selected_file)[0]
        sound_path = os.path.join(self.sounds_dir, selected_file)
        
        try:
            sample_rate, data = wavfile.read(sound_path)
            self.sample_rate = sample_rate
            
            if len(data.shape) > 1:
                data = data[:, 0]
                
            self.base_signal_data = data.tolist()
            
            image_path = os.path.join(self.plots_dir, self.base_name + ".png")
            
            self.btn_play.config(state="normal")
            self.transform_btn.config(state="normal")
            self.fft_btn.config(state="normal")
            self.btn_filter.config(state="normal")
            
            if os.path.exists(image_path):
                self.display_plot(self.base_plot_label, image_path)
            else:
                self.base_plot_label.config(text="No preview image")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sound: {e}")

    def play_sound(self, filename):
        if filename and os.path.exists(filename):
            try:
                winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                messagebox.showerror("Audio error", f"Could not play:\n{e}")
        else:
            messagebox.showwarning("Error", "Audio file not found")
    
    def display_plot(self, loc, filename):
        try:
            if not filename or not os.path.exists(filename):
                loc.config(text="Plot not found", image="")
                return
            
            img = Image.open(filename)
            target_width = 300
            w_percent = (target_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            
            img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            loc.config(image=photo, text="")
            loc.image = photo
        except Exception as e:
            loc.config(text="Plot Error", image="")
            print(f"Error loading plot: {e}")

    def on_dft_pressed(self):
        self.run_transform(
            processor=self.DFTProcessor,
            N=1024,
            suffix="dft",
            lbl_amp=self.ampl_spectrum_lbl,
            lbl_phase=self.phase_spectrum_lbl,
            lbl_restore=self.restore_plot_lbl,
            show_slice=True
        )

    def on_fft_pressed(self):
        self.run_transform(
            processor=self.FFTProcessor,
            N=1024, 
            suffix="fft",
            lbl_amp=self.fft_amp_lbl,
            lbl_phase=self.fft_phase_lbl,
            lbl_restore=self.fft_restored_lbl,
            show_slice=False
        )

    def on_filter_pressed(self):
        if len(self.base_signal_data) == 0:
            return
        filter_type = self.combo_filter.get()
        try:
            f1 = float(self.entry_cutoff1.get())
            f2 = float(self.entry_cutoff2.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid frequencies (numbers)")
            return
        
        fs = self.sample_rate
        signal = self.base_signal_data
        try:
            if filter_type == "Low Pass":
                filtered_signal = self.FilterProcessor.apply_low_pass(signal, f1, fs)
                title_suffix = f"LP {f1}Hz"
                
            elif filter_type == "High Pass":
                filtered_signal = self.FilterProcessor.apply_high_pass(signal, f1, fs)
                title_suffix = f"HP {f1}Hz"
                
            elif filter_type == "Band Pass":
                if f1 >= f2:
                    messagebox.showwarning("Warning", "Freq 1 must be < Freq 2 for Band Pass")
                    return
                filtered_signal = self.FilterProcessor.apply_band_pass(signal, f1, f2, fs)
                title_suffix = f"BP {f1}-{f2}Hz"
        
        except Exception as e:
            messagebox.showerror("Filter Error", str(e))
            return
        N_view = 1000 
        if len(signal) > N_view:
            t_data = filtered_signal[:N_view]
            t_orig = signal[:N_view]
        else:
            t_data = filtered_signal
            t_orig = signal
        
        times = [i/fs for i in range(len(t_data))]
        path_time = os.path.join(self.plots_dir, f"{self.base_name}_filt_time.png")
        self.save_plot(
            f"Signal: {title_suffix}", "Time (s)", "Amp", 
            path_time, times, t_data, kind='comparison', y_data_2=t_orig
        )
        self.display_plot(self.filter_time_lbl, path_time)
        N_fft = 4096
        if len(filtered_signal) > N_fft:
            seg_filt = filtered_signal[:N_fft]
        else:
            seg_filt = filtered_signal
            N_fft = len(seg_filt)

        self.FFTProcessor.compute_fft(seg_filt)
        amps = self.FFTProcessor.get_amplitude_spectrum()
        real_N = len(amps)
        freqs = [(k * fs / real_N) for k in range(real_N)]
        path_freq = os.path.join(self.plots_dir, f"{self.base_name}_filt_spec.png")
        half_N = real_N // 2
        
        self.save_plot(
            f"Spectrum: {title_suffix}", "Freq (Hz)", "Mag", 
            path_freq, freqs[:half_N], amps[:half_N], kind='stem'
        )
        self.display_plot(self.filter_freq_lbl, path_freq)

    def run_transform(self, processor, N, suffix, lbl_amp, lbl_phase, lbl_restore, show_slice=False):
        if len(self.base_signal_data) == 0: return
        
        fs = self.sample_rate
        
        if len(self.base_signal_data) > N:
            start_pos = 0
            source_segment = self.base_signal_data[start_pos : start_pos + N]
        else:
            source_segment = self.base_signal_data
            N = len(source_segment)

        try:
            if hasattr(processor, 'compute_fft'):
                processor.compute_fft(source_segment)
            else:
                processor.compute_dft(source_segment)
                
            ampl = processor.get_amplitude_spectrum()
            phase = processor.get_phase_spectrum()
            restored = processor.compute_ifft() if hasattr(processor, 'compute_ifft') else processor.compute_idft()
        except Exception as e:
            messagebox.showerror("Math Error", str(e))
            return

        freqs = [(k * fs / N) for k in range(N)]
        times = [(i / fs) for i in range(N)]

        path_amp = os.path.join(self.plots_dir, f"{self.base_name}_{suffix}_amp.png")
        self.save_plot("Amplitude", "Hz", "Amp", path_amp, freqs, ampl, 'stem')
        self.display_plot(lbl_amp, path_amp)

        path_phase = os.path.join(self.plots_dir, f"{self.base_name}_{suffix}_phase.png")
        self.save_plot("Phase", "Hz", "Rad", path_phase, freqs, phase, 'stem')
        self.display_plot(lbl_phase, path_phase)

        path_rest = os.path.join(self.plots_dir, f"{self.base_name}_{suffix}_rest.png")
        self.save_plot("Original vs Restored", "Sec", "Val", path_rest, times, restored, 'comparison', source_segment)
        self.display_plot(lbl_restore, path_rest)
        if show_slice:
            path_slice = os.path.join(self.plots_dir, f"{self.base_name}_slice.png")
            self.save_plot(f"Slice (N={N})", "Sec", "Val", path_slice, times, source_segment, 'line')
            self.display_plot(self.used_plot_label, path_slice)

    def save_plot(self, title, xlabel, ylabel, filepath, x_data, y_data, kind='line', y_data_2=None):
        plt.figure(figsize=(3.5, 2.2))

        if kind == 'stem':

            # if len(x_data) > 200:
            #     plt.plot(x_data, y_data, linewidth=0.8)
            # else:
            #     plt.stem(x_data, y_data)

            plt.plot(x_data, y_data)
        elif kind == 'comparison' and y_data_2 is not None:
            plt.plot(x_data, y_data_2, label='Orig', color='blue', alpha=0.5, linewidth=1.5)
            plt.plot(x_data, y_data, label='Rest', color='red', linestyle='--', linewidth=1)
            plt.legend(fontsize=6)
        else:
            plt.plot(x_data, y_data)

        plt.title(title, fontsize=9)
        plt.xlabel(xlabel, fontsize=7)
        plt.ylabel(ylabel, fontsize=7)
        plt.grid(True, alpha=0.3)
        plt.tick_params(labelsize=6)
        plt.tight_layout()
        try: plt.savefig(filepath, dpi=90); plt.close()
        except: pass

if __name__ == "__main__":
    app = App()
    app.mainloop()