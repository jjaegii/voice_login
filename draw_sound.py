import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
from src import convert

audio_folder = 'test'

convert.run(str('새해복') + '.m4a', audio_folder)