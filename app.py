from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import json
import threading
import os

from src import convert, sql, train, inference

SOUND_FOLDER = 'sounds'
app = Flask(__name__)
app.secret_key = 'UR_SECRET_KEY'

# 메인 페이지
@app.route('/')
def login_page():
    return render_template('login.html')

# 회원가입 페이지
@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

# 회원가입시 녹음된 wav 파일 blob형태로 받음 
@app.route('/record', methods=['POST'])
def record():
    f = request.files['passwd']
    # print(f.read()) # blob 출력
    # print(f.filename.split('.')[0]) # 아이디
    file_path = 'sounds/' + f.filename
    f.save(file_path)
    
    img_path = convert.run(f.filename, 'sounds')
    ''' 아래 인자 값 변경 해야함 '''
    # sql.insert(f.filename.split('.')[0], file_path + '/2d+fourier.png')
    return ('', 204)

# 회원가입 버튼 클릭시 
@app.route('/register', methods=['POST'])
def register():
    t1 = threading.Thread(target=train.run)
    t1.start()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    f = request.files['passwd']
    file_path = 'login/' + f.filename
    f.save(file_path)

    img_path = convert.run(f.filename, 'login')
    who = inference.run(img_path)
    os.remove(img_path)
    return json.dumps({'redirect':'success', 'who':who })

@app.route('/success', methods=['GET', 'POST'])
def success():
    if not session:
        try:
            session['username'] = request.form['who']
        except:
            return render_template('403.html')
    return render_template('success.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session:
        return render_template('403.html')
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
