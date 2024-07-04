import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Radiobutton, Entry, Button, Label, Frame
from PIL import Image, ImageTk

from tools import QRCodeGenerator


class MainWindow:
    def __init__(self, root):
        super().__init__()

        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")

        # Configure row and column weights
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(3, weight=1)

        # Main frame
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure row and column weights for main_frame
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.columnconfigure(3, weight=1)

        self.qr_generator = QRCodeGenerator()
        self.radio_value = tk.IntVar(value=1)
        self.url_var = tk.StringVar()

        self.radio_url = None
        self.radio_file = None

        self.url_entry = None
        self.file_button = None

        self.submit_button_url = None
        self.submit_button_file = None
        self.save_button = None

        self.file_label = None
        self.qr_label = None

        self.file_path = None
        self.generated_image = None

        self.create_widgets()
        self.create_url_widgets()

    def create_widgets(self):
        self.radio_url = Radiobutton(self.main_frame,
                                     text="URL",
                                     variable=self.radio_value,
                                     value=1,
                                     command=self.update_input_mode)
        self.radio_url.grid(row=0, column=1, pady=5)

        self.radio_file = Radiobutton(self.main_frame,
                                      text="File",
                                      variable=self.radio_value,
                                      value=2,
                                      command=self.update_input_mode)
        self.radio_file.grid(row=0, column=2, pady=5)

    def create_url_widgets(self):
        if hasattr(self, 'file_label') and self.file_label:
            self.file_label.grid_forget()

        if hasattr(self, 'file_button') and self.file_button:
            self.file_button.grid_forget()

        if hasattr(self, 'submit_button_file') and self.submit_button_file:
            self.submit_button_file.grid_forget()

        if hasattr(self, 'url_entry') and self.url_entry:
            self.url_entry.grid_forget()

        self.url_entry = Entry(self.main_frame,
                               textvariable=self.url_var,
                               width=50)
        self.url_entry.grid(row=1, column=1, pady=5)

        if hasattr(self, 'submit_button_url') and self.submit_button_url:
            self.submit_button_url.grid_forget()

        self.submit_button_url = Button(self.main_frame,
                                        text="Generate QR Code",
                                        command=self.generate_qr_code)
        self.submit_button_url.grid(row=2, column=1, pady=5)

    def create_file_widgets(self):
        if hasattr(self, 'url_entry') and self.url_entry:
            self.url_entry.grid_forget()

        if hasattr(self, 'submit_button_url') and self.submit_button_url:
            self.submit_button_url.grid_forget()

        if hasattr(self, 'file_label') and self.file_label:
            self.file_label.grid_forget()

        self.file_label = Label(self.main_frame)
        self.file_label.grid(row=1, column=1, pady=10)

        if hasattr(self, 'file_button') and self.file_button:
            self.file_button.grid_forget()

        self.file_button = Button(self.main_frame,
                                  text="Select File",
                                  command=self.open_file_dialog)
        self.file_button.grid(row=2, column=1, pady=10)

        if hasattr(self, 'submit_button_file') and self.submit_button_file:
            self.submit_button_file.grid_forget()

        self.submit_button_file = Button(self.main_frame,
                                         text="Generate QR Code",
                                         command=self.generate_qr_code)
        self.submit_button_file.grid(row=3, column=1, pady=10)

    def create_qr_code_widgets(self):
        if hasattr(self, 'qr_label') and self.qr_label:
            self.qr_label.grid_forget()

        self.qr_label = Label(self.main_frame)
        self.qr_label.grid(row=4, column=1, pady=10)

        if hasattr(self, 'save_button') and self.save_button:
            self.save_button.grid_forget()

        self.save_button = Button(self.main_frame,
                                  text="Save QR Code",
                                  command=self.save_qr_code)
        self.save_button.grid(row=6, column=1, pady=10)

    def update_input_mode(self):
        if self.radio_value.get() == 1:  # URL
            self.create_url_widgets()
        else:  # File
            self.create_file_widgets()

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            self.file_label = Label()
            self.file_label.config(text=file_name)
            self.file_label.grid(row=1, column=1, pady=10)

    def generate_qr_code(self):
        data = self.url_var.get() if self.radio_value.get() == 1 else self.file_path
        if not data:
            messagebox.showerror("Input Error", "Please provide a URL or select a file.")
            return

        self.generated_image = self.qr_generator.generate_qr_code(data)
        self.display_qr_code(self.generated_image)

    def display_qr_code(self, img: Image):

        self.create_qr_code_widgets()

        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk
        self.qr_label.grid(row=4, column=1, pady=10)
        self.save_button.grid(row=6, column=1, pady=10)

    def save_qr_code(self):
        if self.generated_image:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("SVG files", "*.svg")])
            if save_path:
                self.generated_image.save(save_path)
                messagebox.showinfo("Saved", f"QR Code saved to {save_path}")
