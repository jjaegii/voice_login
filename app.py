from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import librosa
import librosa.display
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = './sounds'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register():
    # print(request.files['passwd'])
    f = request.files['passwd']
    f.save('sounds/' + secure_filename(f.filename + '.wav'))
    y, sr = librosa.load(os.path.join(UPLOAD_FOLDER, f.filename + '.wav'))

    plt.figure()
    librosa.display.waveshow(y, sr=sr)
    
    plt.savefig(os.path.join(UPLOAD_FOLDER, f.filename + '.png'))

    return json.dumps({'redirect':'/'})

@app.route('/login', methods=['POST'])
def login():
    
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
