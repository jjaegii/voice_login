import librosa
import librosa.display
import matplotlib.pyplot as plt

audio_path = 'file_example_WAV_10MG.wav'

# y = 파형의 amplitude 값
# sr = sampling rate
y, sr = librosa.load(audio_path)

plt.figure()
librosa.display.waveshow(y, sr=sr)
# plt.show()

plt.savefig('sample4.png')