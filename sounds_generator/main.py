from SignalGenerator import SignalGenerator
from harry_potter import HarryPotterTheme

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import winsound
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Signal Generator")
        self.geometry("1200x680")
        self.resizable(False, False)
        
        self.generator = SignalGenerator()
        self.current_signal_widget_1 = None
        self.current_signal_widget_2 = None
        self.current_signal_widget_3 = None

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.columnconfigure(2, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)

        self.overlay_frame = None
        self.gif_frames = []
        self.anim_id = None
        self.current_frame = 0
        self.HP = None

        self.frame_1 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_1.grid(row=0, column=0, sticky="nsew")
        
        self.frame_2 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_2.grid(row=0, column=1, sticky="nsew")
        
        self.frame_3 = ttk.Frame(self, padding=10, relief="sunken")
        self.frame_3.grid(row=0, column=2, sticky="nsew")

        ttk.Label(self.frame_1, text="Signals Generator", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_2, text="Polyphonic", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_3, text="Modulation", font=("Arial", 12, "bold")).pack(pady=10)

        self.create_column_1_widgets()
        self.create_column_2_widgets()
        self.create_column_3_widgets()
        self.update_comboboxes()

    def create_column_1_widgets(self):
        container = self.frame_1
        ttk.Label(container, text="Signal form:").pack(anchor="w")
        self.var_type = tk.StringVar(value="sine")
        types = ["sine", "square", "triangle", "sawtooth", "noise"]
        self.combo_type = ttk.Combobox(container, textvariable=self.var_type, values=types, state="readonly")
        self.combo_type.pack(fill="x", pady=5)

        ttk.Label(container, text="Frequency (Hz):").pack(anchor="w")
        self.entry_freq = ttk.Entry(container)
        self.entry_freq.insert(0, "440.0")
        self.entry_freq.pack(fill="x", pady=5)

        ttk.Label(container, text="Amplitude (0.0 - 1.0):").pack(anchor="w")
        self.entry_amp = ttk.Entry(container)
        self.entry_amp.insert(0, "1.0")
        self.entry_amp.pack(fill="x", pady=5)
        
        ttk.Label(container, text="Duration (s):").pack(anchor="w")
        self.entry_dur = ttk.Entry(container)
        self.entry_dur.insert(0, "2.0")
        self.entry_dur.pack(fill="x", pady=5)
        
        ttk.Label(container, text="Duty (only for square, 0-1):").pack(anchor="w")
        self.entry_duty = ttk.Entry(container)
        self.entry_duty.insert(0, "0.5")
        self.entry_duty.pack(fill="x", pady=10)

        self.btn_gen = ttk.Button(container, text="GENERATE", command=self.on_generate_click)
        self.btn_gen.pack(fill="x", pady=10)

        self.lbl_image = ttk.Label(container)
        self.lbl_image.pack(pady=5)

        self.btn_play = ttk.Button(container, text="PLAY", command=lambda: self.on_play_b_click(column=1), state="disabled")
        self.btn_play.pack(fill="x", pady=10)
    
    def create_column_2_widgets(self):
        container = self.frame_2
            
        lbl_frame1 = ttk.LabelFrame(container, text="Signal 1", padding=10)
        lbl_frame1.pack(fill="x", pady=10)
            
        self.combo_sig1 = ttk.Combobox(lbl_frame1, state="readonly")
        self.combo_sig1.pack(fill="x", pady=5)
            
        self.btn_play_sig1 = ttk.Button(lbl_frame1, text="PLAY", command=lambda: self.play_selected_from_combo(self.combo_sig1))
        self.btn_play_sig1.pack(fill="x")

        lbl_frame2 = ttk.LabelFrame(container, text="Signal 2", padding=10)
        lbl_frame2.pack(fill="x", pady=25)

        self.combo_sig2 = ttk.Combobox(lbl_frame2, state="readonly")
        self.combo_sig2.pack(fill="x", pady=5)
            
        self.btn_play_sig2 = ttk.Button(lbl_frame2, text="PLAY", command=lambda: self.play_selected_from_combo(self.combo_sig2))
        self.btn_play_sig2.pack(fill="x")

        self.btn_sum = ttk.Button(container, text="SUM", state="normal", command=lambda:self.on_sum_click(self.combo_sig1, self.combo_sig2))
        self.btn_sum.pack(fill="x", pady=10)

        self.lbl_image_col2 = ttk.Label(container, text = '')
        self.lbl_image_col2.pack(pady=5)

        self.btn_play_mix = ttk.Button(container, text="PLAY", state="disabled", command=lambda: self.on_play_b_click(2))
        self.btn_play_mix.pack(fill='x', pady=10)

        ttk.Separator(container, orient='horizontal').pack(fill='x', pady=5)
        self.btn_magic = tk.Button(container, text="Don't touch this button", fg="black", font=("Arial", 10, "bold"), command=lambda: self.play_HP())
        self.btn_magic.pack(fill="x", pady=5)

    def create_column_3_widgets(self):
        container = self.frame_3
            
        lbl_frame1_2 = ttk.LabelFrame(container, text="Carrier", padding=10)
        lbl_frame1_2.pack(fill="x", pady=10)
            
        self.combo_sig1_2 = ttk.Combobox(lbl_frame1_2, state="readonly")
        self.combo_sig1_2.pack(fill="x", pady=5)
            
        self.btn_play_sig1_2 = ttk.Button(lbl_frame1_2, text="PLAY", command=lambda: self.play_selected_from_combo(self.combo_sig1_2))
        self.btn_play_sig1_2.pack(fill="x")

        lbl_frame2_2 = ttk.LabelFrame(container, text="Modulator", padding=10)
        lbl_frame2_2.pack(fill="x", pady=10)

        self.combo_sig2_2 = ttk.Combobox(lbl_frame2_2, state="readonly")
        self.combo_sig2_2.pack(fill="x", pady=5)
            
        self.btn_play_sig2_2 = ttk.Button(lbl_frame2_2, text="PLAY", command=lambda: self.play_selected_from_combo(self.combo_sig2_2))
        self.btn_play_sig2_2.pack(fill="x")

        mod_settings_frame = ttk.LabelFrame(container, text="Settings", padding=5)
        mod_settings_frame.pack(fill="x", pady=5)

        self.var_mod_type = tk.StringVar(value="AM")
        rb_am = ttk.Radiobutton(mod_settings_frame, text="AM (Amplitude)", variable=self.var_mod_type, value="AM")
        rb_am.pack(anchor="w")
        rb_fm = ttk.Radiobutton(mod_settings_frame, text="FM (Frequency)", variable=self.var_mod_type, value="FM")
        rb_fm.pack(anchor="w")

        self.btn_modulate = ttk.Button(container, text="MODULATE", command=lambda: self.on_modulate_click())
        self.btn_modulate.pack(fill="x", pady=10)

        self.lbl_image_col3 = ttk.Label(container, text='')
        self.lbl_image_col3.pack(pady=5)

        self.btn_play_mod = ttk.Button(container, text="PLAY", state="disabled", command=lambda: self.on_play_b_click(3))
        self.btn_play_mod.pack(fill="x", pady=5)

    def update_comboboxes(self):
        signal_names = []
        for index, sig in enumerate(self.generator.generated_signal):
            name = sig.wav_filename;
            signal_names.append(name)
        
        self.combo_sig1['values'] = signal_names
        self.combo_sig2['values'] = signal_names

        self.combo_sig1_2['values'] = signal_names
        self.combo_sig2_2['values'] = signal_names
        
        if len(signal_names) == 1:
             self.combo_sig1.current(0)
             self.combo_sig2.current(0)
             self.combo_sig1_2.current(0)
             self.combo_sig2_2.current(0)            

    def on_generate_click(self):
        try:
            w_type = self.var_type.get()
            freq = float(self.entry_freq.get())
            amp = float(self.entry_amp.get())
            dur = float(self.entry_dur.get())
            duty = float(self.entry_duty.get())

            self.generator.default_duration = dur
            self.current_signal_widget_1 = self.generator.create_signal(w_type, freq, amp, duty)
            self.show_plot(self.lbl_image, self.current_signal_widget_1.plot_filename)
            self.btn_play.config(state="normal")
            self.update_comboboxes() 
        except ValueError as e:
            messagebox.showerror("Input error", "Check that you entered numbers.\nSeparate fractional numbers with a period.")
        except Exception as e:
            messagebox.showerror("Error", f"Aboba:\n{e}")

    def play_selected_from_combo(self, combobox_widget):
        selected_index = combobox_widget.current()
        
        if selected_index != -1:
            signal = self.generator.generated_signal[selected_index]
            self.play_audio(signal.wav_filename)
        else:
            messagebox.showwarning("Error", "Choose the signal to play")

    def play_audio(self, filename):
        if filename and os.path.exists(filename):
            try:
                winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                messagebox.showerror("Audio error", f"Coud not play:\n{e}")
        else:
            messagebox.showwarning("Audio is not found")

    def show_plot(self, label_widget, filename):
        try:
            if not filename or not os.path.exists(filename):
                label_widget.config(test="No plot found")
                return
            img = Image.open(filename)
            img = img.resize((350, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label_widget.config(image=photo, text="")
            label_widget.image = photo
        except Exception as e:
            label_widget.config(test = "Plot Error")
            print(f"Error loading plot: {e}")

    def on_play_b_click(self, column):
        if column == 1:
            self.play_audio(self.current_signal_widget_1.wav_filename)
        elif column == 2:
            self.play_audio(self.current_signal_widget_2.wav_filename)
        elif column == 3:
            self.play_audio(self.current_signal_widget_3.wav_filename)
        else:
            messagebox.showerror("No sounds for column 2+")

    def on_sum_click(self, box1, box2):
        idx1 = box1.current()
        idx2 = box2.current()

        if idx1 == -1 or idx2 == -1:
            messagebox.showwarning("Error", "Choose signals to sum")
            return
        self.btn_play_mix.config(state = "normal")
        signal1 = self.generator.generated_signal[idx1]
        signal2 = self.generator.generated_signal[idx2]
        res_signal = self.generator.sum_signals(signal1, signal2)
        self.current_signal_widget_2 = res_signal
        self.show_plot(self.lbl_image_col2, res_signal.plot_filename)
        self.update_comboboxes() 

    def on_modulate_click(self):
        idx_carrier = self.combo_sig1_2.current()
        idx_modulator = self.combo_sig2_2.current()

        if idx_carrier == -1 or idx_modulator == -1:
            messagebox.showwarning("Error", "Select both Carrier and Modulator signals")
            return
        try:
            carrier = self.generator.generated_signal[idx_carrier]
            modulator = self.generator.generated_signal[idx_modulator]
            mod_type = self.var_mod_type.get()
            res_signal = self.generator.modulate_signal(carrier, modulator, mod_type)            
            self.current_signal_widget_3 = res_signal            
            self.show_plot(self.lbl_image_col3, res_signal.plot_filename)
            self.btn_play_mod.config(state="normal")
            self.update_comboboxes()
            
        except ValueError:
            messagebox.showerror("Input Error", "Modulation Index must be a number")
        except Exception as e:
            messagebox.showerror("Modulation Error", f"An error occurred:\n{e}")

    def play_HP(self):
        self.HP = HarryPotterTheme()
        self.HP.play()
        gif_path = "harry_potter/pusheen-harry-potter.gif"
        if not os.path.exists(gif_path):
            messagebox.showerror("Error", "File 'hp.gif' not found!")
            return
        self.overlay_frame = tk.Frame(self, bg="black")
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        img = Image.open(gif_path)
        self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((1250, 700), Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(img)]    
        self.lbl_gif_anim = tk.Label(self.overlay_frame)
        self.lbl_gif_anim.pack(expand=True, fill="both")
        btn_close = tk.Button(self.overlay_frame, text="STOP", bg="yellow", font=("Arial", 14, "bold"), command=self.stop_magic)
        btn_close.place(relx=0.5, rely=0.9, anchor="center")
        self.current_frame = 0
        self.animate_gif()
    
    def stop_magic(self):
        self.HP.stop()
        if self.anim_id:
            self.after_cancel(self.anim_id)
            self.anim_id = None
        if self.overlay_frame:
            self.overlay_frame.destroy()
            self.overlay_frame = None

    def animate_gif(self):
        if self.overlay_frame is None: 
            return
        frame = self.gif_frames[self.current_frame]
        self.lbl_gif_anim.configure(image=frame)
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.anim_id = self.after(100, self.animate_gif)

if __name__ == "__main__":
    app = App()
    app.mainloop()

