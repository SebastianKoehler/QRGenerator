import qrcode
import qrcode.main as qrcm


class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(data: str) -> qrcm.GenericImage:
        qr = qrcm.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1
        )
        qr.add_data(data)
        qr.make(fit=True)

        return qr.make_image(fill='black', back_color='white')
