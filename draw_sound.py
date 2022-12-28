import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
from src import convert

audio_folder = 'sample'

for i in range(len(os.listdir(audio_folder))):
    convert.run(str(i+1) + '.wav', audio_folder)