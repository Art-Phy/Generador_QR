### Generador de QR ###

# descargamos los paquetes necesarios
# pip install qrcode
# pip install pillow (esto es para editar colores)

import qrcode

# introducimos lo que queremos que se encuentre en el QR
data = "Hola, soy Art_Phy"

# definimos las características del QR
qr = qrcode.QRCode(version=1, box_size=10, border=5)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color = 'black', back_color = 'green')

# guardamos nuestro QR en la ubicación que queramos
img.save("/Users/arturosanma/Desktop/Principiantes/qr_image.png")
