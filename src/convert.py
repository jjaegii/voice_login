''' wav 파일을 이미지화 시키는 모듈 '''
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cv2

SOUND_FOLDER = None

# 2D 음파 그래프
def convert2D(wavfile, y, sr):
    plt.figure()
    librosa.display.waveshow(y, sr=sr)
    img_path = os.path.join(SOUND_FOLDER, wavfile.split('.')[0] + '_2d.png')
    plt.savefig(img_path)
    return img_path

# 푸리에 변환
def convertFourier(wavfile, y):
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    plt.figure()
    plt.plot(D)
    img_path = os.path.join(SOUND_FOLDER, wavfile.split('.')[0] + '_fourier.png')
    plt.savefig(img_path)
    return img_path

# 2D, 푸리에 합친 후 삭제
def merge(wavfile, path_2d, path_fourier):
    img_2d = cv2.imread(path_2d)
    img_fourier = cv2.imread(path_fourier)
    merged_img = cv2.addWeighted(img_2d, 0.5, img_fourier, 0.5, 0)
    img_path = os.path.join(SOUND_FOLDER, wavfile.split('.')[0] + '.png')
    cv2.imwrite(img_path, merged_img)
    os.remove(path_2d)
    os.remove(path_fourier)
    os.remove(os.path.join(SOUND_FOLDER, wavfile))

def run(wavfile, path):
    global SOUND_FOLDER
    SOUND_FOLDER = path
    y, sr = librosa.load(os.path.join(SOUND_FOLDER, wavfile))
    path_2d = convert2D(wavfile, y, sr)
    path_fourier = convertFourier(wavfile, y)
    merge(wavfile, path_2d, path_fourier)