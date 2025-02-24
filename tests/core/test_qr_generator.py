
import pytest
from qrcode.image.pil import PilImage


from src.core import QRCodeGenerator
import os


@pytest.fixture
def qr_generator():
    """Creates a QR Code Generator object for the tests."""
    return QRCodeGenerator()


def test_generate_valid_qr_code_from_url(qr_generator):
    """Tests whether a QR code is generated from a valid URL."""

    # Arrange - Preparations
    test_url = "https://www.example.com"

    # Act - Execute action
    qr_code = qr_generator.generate_qr_code(test_url)

    # Assert - Check expectations
    assert qr_code is None, "The generated QR code should not be None."
    assert isinstance(qr_code, PilImage), "The generated QR code should be of type 'PilImage'."

def test_generate_valid_qr_code_from_file(qr_generator):
    """Tests whether a QR code is generated from a file."""

    # Arrange - Preparations
    test_file = "../data/demo_data.txt"

    # Act - Execute action
    qr_code = qr_generator.generate_qr_code(test_file)

    # Assert - Check expectations
    assert os.path.exists(test_file), f"Test file {test_file} does not exist."
    assert qr_code is not None, "The generated QR code should not be None."
    assert isinstance(qr_code, PilImage), "The generated QR code should be of type 'PilImage'."
