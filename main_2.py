from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import datetime
import os

db_path = './coordinate.db'

dt_now = datetime.datetime.now()

app = Flask(__name__)


@app.route('/')
def top_page():
    # 接続。なければDBを作成する。
    conn = sqlite3.connect(db_path)

    # カーソルを取得
    c = conn.cursor()

    c.execute("SELECT * FROM articles")
    length = len(c.fetchall())
    new_list = list(range(length-5,length))

    def partial_acquisition(id,selector):#1:title,3:body_c
        #idで検索
        for row in c.execute(f'SELECT * FROM articles WHERE id = {id}'):
            result = row[selector]

        return result
    
    title_list = []
    body_c_list = []
    id_list = []
    for i in new_list:
        id_list.append(i)
        title_list.append(partial_acquisition(i,1))
        body_c_list.append(partial_acquisition(i,3))

    conn.close()

    return render_template('top_page.html',
                            url = id_list,
                            title=title_list,
                            comment=body_c_list)

@app.route('/create')
def create():
    return render_template('create_form.html')

@app.route('/create_result', methods=["POST"])
def create_result():
    # 接続。なければDBを作成する。
    conn = sqlite3.connect(db_path)

    # カーソルを取得
    c = conn.cursor()

    title = request.form.get("title",None)
    body = request.form.get("body",None)
    body_c = request.form.get("body_c",None)

    # Insert実行
    def table_insert(title = "",body = "",body_c = "",pants = "",pants_c = "",shoes = "",shoes_c = "",date=dt_now):

        #id = c.lastrowid + 1
        round_up = [(title, body, body_c, pants, pants_c, shoes, shoes_c, date)]
        c.executemany('''INSERT INTO articles(title, body, body_c, pants, pants_c, shoes, shoes_c, date) VALUES (?,?,?,?,?,?,?,?)''' , round_up)

        conn.commit()

    # 現在時刻を変数に格納
    date = dt_now
    table_insert(title=title,body=body,body_c=body_c,date=date)

    for row in c.execute(f'SELECT * FROM articles WHERE title = "{title}" and date = "{date}"'):
        url = row[0]
    
    # コネクションをクローズ
    conn.close()

    return redirect(f'/{url}')

@app.route('/<id>')
def coordinate_page(id):
    # DBに接続する。なければDBを作成する。
    conn = sqlite3.connect(db_path)

    # カーソルを取得する
    c = conn.cursor()

    #idで検索
    tp_id = []
    tp_id.append(id)
    result = []
    try:
        for row in c.execute('SELECT * FROM articles WHERE id = (?)',tuple(tp_id)):
            result = row
    except:
        abort(404,{ 'id':id })
    # コネクションをクローズ
    
    # faviconのせいで二回呼び出されている気がする
    # print('result:',list(result))
    conn.close()
    return render_template('coordinate_page.html',
                            title = result,
                            result = result)

@app.route('/<id>/qr')
def id_qr(id):
    def generate_qr(id):
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
        img_qr_big.save("{{url_for('static', 'qr_img.png')}}")

    def insert_text():
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
            
            
            
            img.save("{{ url_for('static', 'unique_card.png')}}")
    
    
@app.errorhandler(404)
def error_handler(error):
    return render_template('error.html',
                            id = id)

if __name__ == '__main__':
    try:
        if os.path.exists(db_path):
            # 接続。なければDBを作成する。
            conn = sqlite3.connect(db_path)
            # カーソルを取得
            c = conn.cursor()
            # テーブルを作成
            c.execute('''CREATE TABLE articles  (
                        id INTEGER PRIMARY KEY,
                        title text, 
                        body text, 
                        body_c text,
                        pants text,
                        pants_c text,
                        shoes text,
                        shoes_c text,
                        date text)''')
            # コネクションをクローズ
            conn.close()
    except:
        pass

    app.run(debug=True)
