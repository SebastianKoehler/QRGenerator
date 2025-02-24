import pytest
import tkinter as tk
from src.gui import QRCodeApp

@pytest.fixture
def app():
    """Erstellt die GUI-App für die Tests."""
    root = tk.Tk()
    app = QRCodeApp(root)
    yield app
    root.destroy()

def test_visible_widgets_on_start(app):
    """Tests whether the visible elements exist and are displayed."""
    assert app.app_label.winfo_exists() is not None
    assert app.app_label["text"] == "QR Code Generator"

    assert app.input_entry.winfo_exists() is not None

    assert app.btn_url.winfo_exists() is not None
    assert app.btn_url["text"] == "URL"
    assert app.btn_generate.winfo_exists() is not None
    assert app.btn_generate["text"] == "QR Code erstellen"
    assert app.btn_file.winfo_exists() is not None
    assert app.btn_file["text"] == "Datei"

def test_non_visible_widgets_on_start(app):
    """Tests whether the non-visible elements exist and whether they are displayed."""
    assert app.qr_label.winfo_exists() == 1
    assert app.qr_label.winfo_ismapped() == 0

    assert app.save_button.winfo_exists() == 1
    assert app.save_button.winfo_ismapped() == 0

def test_hidden_widgets_appear_after_button_click(app):
    """Tests whether the hidden element is visible after a button click."""
    assert app.browse_button.winfo_exists() == 1
    assert app.browse_button.winfo_ismapped() == 0

    app.btn_file.invoke()
    app.root.update()

    assert app.browse_button.winfo_ismapped() == 1



