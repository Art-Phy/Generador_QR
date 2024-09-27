### Generador de QR ###

# descargamos los paquetes necesarios
# pip install qrcode
# pip install pillow (esto es para editar colores)

import qrcode
from PIL import Image, ImageDraw, ImageFont

# introducimos lo que queremos que se encuentre en el QR
data = "https://discord.com/channels/1288084026883706912/1288084028611629148"

# definimos las características del QR
qr = qrcode.QRCode(version=8, box_size=7, border=3)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color = 'black', back_color = 'white').convert('RGB')

# le indicamos nuestro logo y sus dimensiones
logo = Image.open("/Users/arturosanma/Desktop/Informática/Logo.png")

logo_size = 120
logo = logo.resize((logo_size, logo_size))

# comprobar si el logo tiene canal alfa (transparencia)
if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
    mask = logo.split()[3] # canal alfa en posición 3
else:
    mask = None # no hay transparencia no necesitamos máscara

# centrar el logo en el QR
qr_width, qr_height = img.size
logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

img.paste(logo, logo_position, mask)

# guardamos nuestro QR en la ubicación que queramos
img.save("/Users/arturosanma/Desktop/qr_image.png")
