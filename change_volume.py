import librosa
import soundfile as sf

data, sr = librosa.load("voices/nate_shouting.wav")
factor = 0.3
data *= factor
sf.write("output1.wav", data, sr)