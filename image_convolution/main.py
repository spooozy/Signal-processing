import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

from ImageFilterProcessor import ImageFilterProcessor

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Image Processing Tool")
        self.geometry("1000x600")
        self.resizable(False, False)
        
        self.processor = ImageFilterProcessor()
        
        self.original_image_np = None
        self.processed_image_np = None
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
    
        self.frame_orig = ttk.LabelFrame(self, text="Original Image")
        self.frame_orig.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.lbl_orig = ttk.Label(self.frame_orig, text="Load an image...")
        self.lbl_orig.pack(expand=True)

        self.frame_res = ttk.LabelFrame(self, text="Result")
        self.frame_res.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.lbl_res = ttk.Label(self.frame_res, text="Result will appear here")
        self.lbl_res.pack(expand=True)
        
        self.control_panel = ttk.Frame(self, padding=10)
        self.control_panel.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        ttk.Button(self.control_panel, text="Load Image", command=self.load_image).pack(side="left", padx=10)
        
        ttk.Label(self.control_panel, text="Filter:").pack(side="left", padx=(20, 5))
        self.combo_filter = ttk.Combobox(self.control_panel, 
                                         values=["Box Blur", "Gaussian Blur", "Median Filter", "Sobel Operator", "Color Sobel"],
                                         state="readonly")
        self.combo_filter.current(0)
        self.combo_filter.pack(side="left", padx=5)
        self.combo_filter.bind("<<ComboboxSelected>>", self.on_filter_changed)
        
        self.lbl_kernel = ttk.Label(self.control_panel, text="Kernel Size:")
        self.lbl_kernel.pack(side="left", padx=(20, 5))
        self.spin_kernel = ttk.Spinbox(self.control_panel, from_=3, to=15, increment=2, width=5)
        self.spin_kernel.set(3)
        self.spin_kernel.pack(side="left", padx=5)
        
        self.btn_process = ttk.Button(self.control_panel, text="APPLY FILTER", state="disabled", command=self.process_image)
        self.btn_process.pack(side="right", padx=10)

    def on_filter_changed(self, event):
        filter_name = self.combo_filter.get()
        if filter_name == "Sobel Operator" or filter_name == "Color Sobel":
            self.spin_kernel.config(state="disabled")
        else:
            self.spin_kernel.config(state="normal")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return
            
        try:
            pil_img = Image.open(file_path).convert('RGB')
            
            pil_img.thumbnail((600, 600)) 
            
            self.original_image_np = np.array(pil_img)
            
            self.show_image(pil_img, self.lbl_orig)
            
            self.btn_process.config(state="normal")
            self.lbl_res.config(image='', text="Press Apply...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    def show_image(self, pil_image, label_widget):
        display_img = pil_image.copy()
        display_img.thumbnail((480, 400))
        
        tk_img = ImageTk.PhotoImage(display_img)
        label_widget.config(image=tk_img, text="")
        label_widget.image = tk_img

    def process_image(self):
        if self.original_image_np is None:
            return
            
        filter_name = self.combo_filter.get()
        k_size = int(self.spin_kernel.get())
        
        if k_size % 2 == 0:
            k_size += 1
        
        self.config(cursor="watch")
        self.update()
        
        try:
            result_np = None
            
            if filter_name == "Box Blur":
                result_np = self.processor.apply_box_blur(self.original_image_np, kernel_size=k_size)
                
            elif filter_name == "Gaussian Blur":
                sigma = k_size / 3.0 
                result_np = self.processor.apply_gaussian_blur(self.original_image_np, kernel_size=k_size, sigma=sigma)
                
            elif filter_name == "Median Filter":
                result_np = self.processor.apply_median_filter(self.original_image_np, kernel_size=k_size)
                
            elif filter_name == "Sobel Operator":
                result_np = self.processor.apply_sobel(self.original_image_np)
            elif filter_name == "Color Sobel":
                result_np = self.processor.apply_color_sobel(self.original_image_np)
            
            messagebox.showinfo("Message", f"{filter_name} is done")
            self.processed_image_np = result_np
            
            if len(result_np.shape) == 2:
                res_pil = Image.fromarray(result_np, mode='L')
            else:
                res_pil = Image.fromarray(result_np, mode='RGB')
                
            self.show_image(res_pil, self.lbl_res)
            
        except Exception as e:
            messagebox.showerror("Error during processing", str(e))
        finally:
            self.config(cursor="")

if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()