import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import sqlite3

from src import convert, sql

SOUND_FOLDER = 'sounds'
app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register():
    f = request.files['passwd']
    # print(f.filename) # 아이디
    file_path = 'sounds/' + f.filename
    f.save(file_path + '.wav')
    convert.run(f.filename + '.wav', 'sounds')
    sql.insert(f.filename, file_path + '.png')
    return json.dumps({'redirect':'/'})

@app.route('/login', methods=['POST'])
def login():
    
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
