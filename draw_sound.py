import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def find_idx(lst, threshold):
    for i, x in enumerate(lst):
        if abs(x) > threshold:
            return i
    return -1

# 2d
def twoD(y, sr, audio_path):
    y_np = np.array(y)

    plt.figure()
    print(np.mean(np.abs(y_np)))
    librosa.display.waveshow(y[find_idx(y_np, np.mean(np.abs(y_np))):-find_idx(reversed(y_np), np.mean(np.abs(y_np)))], sr=sr)
    # plt.show()
    plt.savefig(audio_path.split('.')[0] + '_2d.png')


# mel spectogram
def mel_specto(y, sr, audio_path):
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
    plt.savefig(audio_path.split('.')[0] + '_specto.png', bbox_inches='tight')

# mfcc
def mfcc(y, sr, audio_path):
    y_np = np.array(y)
    
    FIG_SIZE = (15, 10)
    hop_length = 512
    n_fft = 2048

    MFCCs = librosa.feature.mfcc(y[find_idx(y_np, np.mean(np.abs(y_np))):-find_idx(reversed(y_np), np.mean(np.abs(y_np)))], sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)
    plt.figure()
    plt.axis('off')
    librosa.display.specshow(MFCCs, sr=sr, hop_length=hop_length)
    plt.savefig(audio_path.split('.')[0] + '_mfcc.png', bbox_inches='tight')

audio_folder = 'test'
for i in os.listdir(audio_folder):
    audio_path = os.path.join(audio_folder, i)
    y, sr = librosa.load(audio_path)
    twoD(y, sr, audio_path)
    mel_specto(y, sr, audio_path)
    mfcc(y, sr, audio_path)
    