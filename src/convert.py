''' 오디오 파일을 이미지화 시키는 모듈 '''
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
    plt.axis('off')
    librosa.display.waveshow(y, sr=sr)
    img_path = os.path.join(SOUND_FOLDER, wavfile.split('.')[0] + '_2d.png')
    plt.savefig(img_path, bbox_inches='tight')
    return img_path

# 푸리에 변환
def convertFourier(wavfile, y):
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    plt.figure()
    plt.plot(D)
    img_path = os.path.join(SOUND_FOLDER, wavfile.split('.')[0] + '_fourier.png')
    plt.savefig(img_path, bbox_inches='tight')
    return img_path

# 2D, 푸리에 합친 후 삭제
def merge(wavfile, path_2d, path_fourier):
    img_2d = cv2.imread(path_2d)
    img_fourier = cv2.imread(path_fourier)
    merged_img = cv2.addWeighted(img_2d, 0.5, img_fourier, 0.5, 0)
    
    img_folder = os.path.join(SOUND_FOLDER, wavfile.split('.')[0])
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    img_path = os.path.join(img_folder, '2d+fourier.png')
    cv2.imwrite(img_path, merged_img)
    
    os.remove(path_2d)
    os.remove(path_fourier)
    os.remove(os.path.join(SOUND_FOLDER, wavfile))
    return img_path

# MFCCs 변환 후 삭제
def mfcc(wavfile, y, sr):
    FIG_SIZE = (15, 10)
    hop_length = 512
    n_fft = 2048

    MFCCs = librosa.feature.mfcc(y, sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)
    plt.figure()
    plt.axis('off')
    librosa.display.specshow(MFCCs, sr=sr, hop_length=hop_length)
    img_folder = os.path.join(SOUND_FOLDER, wavfile.split('.')[0])
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    img_path = os.path.join(img_folder, 'mfcc.png')
    plt.savefig(img_path, bbox_inches='tight')
    os.remove(os.path.join(SOUND_FOLDER, wavfile))
    return img_path
    

def run(wavfile, path):
    # 소리가 없는 부분 자르는 기능이 필요함
    global SOUND_FOLDER
    SOUND_FOLDER = path
    y, sr = librosa.load(os.path.join(SOUND_FOLDER, wavfile))
    # path_2d = convert2D(wavfile, y, sr)
    # path_fourier = convertFourier(wavfile, y)
    # img_path = merge(wavfile, path_2d, path_fourier)
    img_path = mfcc(wavfile, y, sr)
    return img_path