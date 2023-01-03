''' 오디오 파일을 이미지화 시키는 모듈 '''
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cv2

SOUND_FOLDER = None

# 시작점, 끝점 찾기
def find_idx(lst, threshold):
    for i, x in enumerate(lst):
        if abs(x) > threshold:
            return i
    return -1

# 2D 음파 그래프
def convert2D(wavfile, y, sr):
    y_np = np.array(y)
    plt.figure()
    plt.axis('off')
    librosa.display.waveshow(y[find_idx(y_np, np.mean(np.abs(y_np))):-find_idx(reversed(y_np), np.mean(np.abs(y_np)))], sr=sr)
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
    
# mel spectogram
def mel_specto(wavfile, y, sr):
    y_np = np.array(y)

    n_fft = 2048
    win_length = 2048
    hop_length = 1024
    n_mels = 128

    D = np.abs(librosa.stft(y[find_idx(y_np, np.mean(np.abs(y_np))):-find_idx(reversed(y_np), np.mean(np.abs(y_np)))], n_fft=n_fft, win_length = win_length, hop_length=hop_length))
    plt.figure()
    plt.axis('off')
    mel_spec = librosa.feature.melspectrogram(S=D, sr=sr, n_mels=n_mels, hop_length=hop_length, win_length=win_length)
    librosa.display.specshow(librosa.amplitude_to_db(mel_spec, ref=0.00002), sr=sr, hop_length = hop_length, y_axis='mel', x_axis='time')
    # plt.colorbar(format='%2.0f dB')
    img_folder = os.path.join(SOUND_FOLDER, wavfile.split('.')[0])
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    f_list = os.listdir(img_folder)
    f_name = str(len(f_list) + 1) + '.png'
    img_path = os.path.join(img_folder, f_name)
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
    # img_path = mfcc(wavfile, y, sr)
    return mel_specto(wavfile, y, sr)
