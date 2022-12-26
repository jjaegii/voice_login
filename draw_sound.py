import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

audio_folder = 'sounds/'

for i in range(len(os.listdir(audio_folder))):
    # y = 파형의 amplitude 값
    # sr = sampling rate
    y, sr = librosa.load(audio_folder + str(i+1) + '.wav')

    plt.figure()
    librosa.display.waveshow(y, sr=sr)
    # plt.show()

    plt.savefig(audio_folder + str(i+1) + '.png')