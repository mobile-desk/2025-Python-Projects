import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os

class AdvancedQRGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
    
    def create_qr(self, data, filename, fill_color="#000000", 
                  back_color="#ffffff", logo_path=None):
        # Add data
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        # Create QR image
        qr_image = self.qr.make_image(fill_color=fill_color, 
                                     back_color=back_color).convert('RGBA')
        
        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path)
            
            # Calculate logo size (max 30% of QR code)
            logo_size = int(qr_image.size[0] * 0.3)
            logo = logo.resize((logo_size, logo_size))
            
            # Calculate position to center logo
            pos = ((qr_image.size[0] - logo_size) // 2,
                  (qr_image.size[1] - logo_size) // 2)
            
            # Create white background for logo
            logo_bg = Image.new('RGBA', qr_image.size, 'white')
            logo_bg.paste(logo, pos)
            
            # Combine QR code and logo
            qr_image = Image.alpha_composite(qr_image, logo_bg)
        
        # Save QR code
        qr_image.save(filename)
        return filename

def generate_styled_qrs():
    generator = AdvancedQRGenerator()
    
    # Basic QR code
    generator.create_qr(
        "https://pycommune.com.ng/snippets/7/",
        "basic_qr.png"
    )
    
    # Colored QR code
    generator.create_qr(
        "https://pycommune.com.ng/snippets/7/",
        "colored_qr.png",
        fill_color="#1f77b4",
        back_color="#ffffff"
    )
    
    # QR with logo
    generator.create_qr(
        "https://pycommune.com.ng/snippets/7/",
        "logo_qr.png",
        logo_path="logo.png"  # Your logo file
    )
    
    # Gradient style QR (requires extra setup)
    generator.create_qr(
        "https://pycommune.com.ng/snippets/7/",
        "gradient_qr.png",
        fill_color="#ff0000",  # Will be modified for gradient
        back_color="#ffffff"
    )

# Additional features you can add:
class QRWithAnimation:
    def create_animated_qr(self, data, filename):
        frames = []
        colors = ['#ff0000', '#00ff00', '#0000ff']
        
        generator = AdvancedQRGenerator()
        for color in colors:
            frame = generator.create_qr(
                data,
                f"frame_{color}.png",
                fill_color=color
            )
            frames.append(Image.open(frame))
        
        # Save as GIF
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=500,
            loop=0
        )

# Usage example
if __name__ == "__main__":
    # Basic usage
    generator = AdvancedQRGenerator()
    generator.create_qr(
        "https://pycommune.com.ng/snippets/7/",
        "custom_qr.png",
        fill_color="#FF5733",
        back_color="#C7CEEA",
        logo_path="company_logo.png"  # Optional
    )
    
    # Create animated QR
    animator = QRWithAnimation()
    animator.create_animated_qr(
        "https://pycommune.com.ng/snippets/7/",
        "animated_qr.gif"
    )
