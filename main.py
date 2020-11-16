from flask import Flask, render_template, request
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
        #c.execute(f'INSERT INTO articles VALUES ({id},"{title}","a","a","a","a","a","a")')
        round_up = [(title, body, body_c, pants, pants_c, shoes, shoes_c, date)]
        c.executemany('''INSERT INTO articles(title, body, body_c, pants, pants_c, shoes, shoes_c, date) VALUES (?,?,?,?,?,?,?,?)''' , round_up)

        conn.commit()

    date = dt_now
    table_insert(title=title,body=body,body_c=body_c,date=date)

    for row in c.execute(f'SELECT * FROM articles WHERE title = "{title}" and date = "{date}"'):
        url = row[0]
        print(url)
    

    # コネクションをクローズ
    conn.close()

    return render_template('create_result.html',
                            id = url,
                            title = title,
                            body = body,
                            body_c = body_c)

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
    for row in c.execute('SELECT * FROM articles WHERE id = (?)',tuple(tp_id)):
        result = row
    # コネクションをクローズ
    
    #TODO faviconのせいで二回呼び出されている気がする
    print('result:',list(result))
    conn.close()
    return render_template('coordinate_page.html',
                            title = result,
                            result = result)

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
