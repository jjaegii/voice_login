from flask import Flask, render_template, request, session, escape
from werkzeug.utils import secure_filename
import json
import threading

from src import convert, sql, train, inference

SOUND_FOLDER = 'sounds'
app = Flask(__name__)
app.secret_key = 'UR_SECRET_KEY'

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register():
    f = request.files['passwd']
    # print(f.read()) # blob 출력
    # print(f.filename.split('.')[0]) # 아이디
    file_path = 'sounds/' + f.filename
    f.save(file_path)
    
    convert.run(f.filename, 'sounds')
    # sql.insert(f.filename.split('.')[0], file_path + '/2d+fourier.png')
    t1 = threading.Thread(target=train.run)
    t1.start()
    return json.dumps({'redirect':'/'})

# https://blogair.tistory.com/165 로그인 성공 시 세션 사용
@app.route('/login', methods=['POST'])
def login():
    f = request.files['passwd']
    file_path = 'login/' + f.filename
    f.save(file_path)

    img_path = convert.run(f.filename, 'login')
    print(img_path)
    inference.run(img_path)
    return json.dumps({'redirect':'success'})

@app.route('/success')
def success():

    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
