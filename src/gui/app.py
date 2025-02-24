import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, StringVar, LEFT, RIGHT
from tkinter.ttk import Button, Label, Frame, Style
from PIL import Image, ImageTk
from PIL.Image import Resampling
from PIL.ImageTk import PhotoImage

from src.core import QRCodeGenerator

class QRCodeApp:
    def __init__(self, root):

        self.root = root
        self.main_frame = Frame(self.root)
        self.qr_label = Label(self.main_frame)
        self.input_frame = Frame(self.main_frame)
        self.input_var = StringVar()

        base_dir = Path(__file__).resolve().parent.parent
        icon_path = base_dir / "assets" / "icon.png"

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_width = 500
        self.window_height = 400

        x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))

        self.root.title("QR Code Generator")
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")
        self.root.resizable(False, False)

        if icon_path.exists():
            self.root.iconphoto(True, ImageTk.PhotoImage(file=str(icon_path)))
        else:
            print(f"⚠️ Warnung: Icon {icon_path} nicht gefunden!")

        self.qr_generator = QRCodeGenerator()
        self.file_path = None
        self.generated_image = None
        self.input_type = "URL"

        self.style = Style()
        self.style.configure("TButton", font=("Arial", 12))

        self.app_label = Label(self.main_frame, text="QR Code Generator", font=("Arial", 16, "bold"))

        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_var, width=40)

        self.btn_url = Button(self.main_frame, text="URL", command=self.use_url_mode)
        self.btn_generate = Button(self.main_frame, text="QR Code erstellen", command=self.generate_qr_code)
        self.btn_file = Button(self.main_frame, text="Datei", command=self.use_file_mode)

        self.save_button = Button(self.main_frame, text="QR Code speichern", command=self.save_qr_code)
        self.browse_button = Button(self.input_frame, text="Durchsuchen", command=self.open_file_dialog)

        self.create_widgets()

    def create_widgets(self):
        self.main_frame.pack(expand=True)

        self.app_label.pack(pady=10)

        # QR-Code Anzeige
        self.qr_label.pack(pady=10)
        self.qr_label.pack_forget()

        # Speichern-Button
        self.save_button.pack(pady=5)
        self.save_button.pack_forget()

        # Auswahlbuttons
        self.btn_url.pack(pady=5, padx=10, side=LEFT)
        self.btn_file.pack(pady=5, padx=10, side=RIGHT)

        # Eingabebereich
        self.input_frame.pack(pady=10)
        self.input_entry.pack()
        self.btn_generate.pack(pady=10)

    def use_url_mode(self):
        self.input_type = "URL"
        self.input_var.set("")
        self.browse_button.pack_forget()

    def use_file_mode(self):
        self.input_type = "File"
        self.input_var.set("")
        self.browse_button.pack(pady=20)

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("TXT files", "*.txt")])
        if self.file_path:
            self.input_var.set(self.file_path)

    def generate_qr_code(self):
        data = self.input_var.get()
        if not data:
            messagebox.showerror("Fehler", "Bitte eine URL eingeben oder eine Datei auswählen.")
            return

        self.input_var.set("")
        self.generated_image = self.qr_generator.generate_qr_code(data)
        self.display_qr_code(self.generated_image)

    def display_qr_code(self, img: Image):
        img = img.resize((150, 150), Resampling.LANCZOS)
        img_tk = PhotoImage(img)
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk
        self.qr_label.pack()
        self.save_button.pack()

    def save_qr_code(self):
        if self.generated_image:
            save_path = filedialog.asksaveasfilename(
                initialfile="generated_qr_code",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("SVG files", "*.svg")]
            )
            if save_path:
                self.generated_image.save(save_path)
                messagebox.showinfo("Gespeichert", f"QR Code wurde gespeichert: {save_path}")
