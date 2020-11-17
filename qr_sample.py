import qrcode
from PIL import Image

# icon = Image.open('Logo-icon.png')

# qr = qrcode.QRCode(
#     error_correction=qrcode.constants.ERROR_CORRECT_H,
#     border = 10
# )

# qr.add_data('https://google.co.jp/')
# qr.make()
# img = qr.make_image(fill_color = '#7fd6ff').convert('RGB')

# pos = ((img[0] - icon.size[0]) // 2, (img.size[1] - icon.size[1]) // 2)

# img.paste(icon, pos)
# img.save('./sample_qr.png')

icon = Image.open('resize-icon.png')

qr_big = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    border=1
)
qr_big.add_data('https://google.co.jp/')
qr_big.make()
img_qr_big = qr_big.make_image(fill_color = '#7fd6ff').convert('RGB')

pos = ((img_qr_big.size[0] - icon.size[0]) // 2, (img_qr_big.size[1] - icon.size[1]) // 2)

img_qr_big.paste(icon, pos)
img_qr_big.save('sample.png')