from PIL import ImageFont, Image, ImageDraw
import qrcode

base_path = 'background_img.png'
qr_path = 'qr_img.png'
font_path = "meiryo.ttc"
icon_path = 'resize-icon.png'
url_path = 'https://google.co.jp/'

def generate_qrcode():
    icon = Image.open(icon_path)

    qr_big = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=1
    )
    qr_big.add_data(url_path)
    qr_big.make()
    img_qr_big = qr_big.make_image(fill_color = '#7fd6ff').convert('RGB')

    pos = ((img_qr_big.size[0] - icon.size[0]) // 2, (img_qr_big.size[1] - icon.size[1]) // 2)

    img_qr_big.paste(icon, pos)
    img_qr_big.save('qr_img.png')


#読み込み
base_img = Image.open(base_path).copy()
qr_img = Image.open(qr_path).copy()

#貼り付け
base_img.paste(qr_img,(140,160))

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)

    return img

text = "This is Title"
font_size = 60
font_color = (255, 255, 255)
height = 200
width = 615
img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width)

text = """This space is some 
comments"""
font_size = 50
font_color = (255, 255, 255)
height = 330
width = 580
img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width)



img.save('unique_card.png')