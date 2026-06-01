import numpy as np
import matplotlib.pyplot as plt
import librosa
import os 

# Misma musica pero en formato WAV y MP3
wav_path = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Ejercicio6\\316830__lalks__ferambie.wav'
mp3_path = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Ejercicio6\\316830__lalks__ferambie.mp3'


x_wav, f_s_wav = librosa.load(wav_path, sr=None)
x_mp3, f_s_mp3 = librosa.load(mp3_path, sr=None)

#Tamanos en disco 
tamano_wav = os.path.getsize(wav_path) / 1024 # KB
tamano_mp3 = os.path.getsize(mp3_path) / 1024 # KB

print(f"WAV: {tamano_wav:.1f} KB | fs = {f_s_wav} Hz")
print(f"MP3: {tamano_mp3:.1f} KB | fs = {f_s_mp3} Hz")
print(f"Ratio de compresion MP3: {tamano_wav / tamano_mp3:.2f}x")

def espectro(x, fs):
    """ Retorna frecuencias (Hz) y magnitud en dB"""
    N = len(x)
    X = np.abs(np.fft.rfft(x))
    f = np.fft.rfftfreq(N, 1 / fs)
    return f, 20 * np.log10(X + 1e-12) # Evitar log(0)

#Tomar el mismo tramo de 5 s en cada archivo
dur = 5
x_wav_seg = x_wav[: int(dur * f_s_wav)]
x_mp3_seg = x_mp3[: int(dur * f_s_mp3)]

f_w, X_w = espectro(x_wav_seg, f_s_wav)
f_m, X_m = espectro(x_mp3_seg, f_s_mp3)

fig, ax = plt.subplots(figsize = (12, 5))
ax.semilogx(f_w, X_w, color='steelblue', alpha=0.7, label='WAV (sin COMPRESION)')
ax.semilogx(f_m, X_m, color='darkred', alpha=0.7, label='MP3 (con COMPRESION)')
ax.set(xlabel = 'Frecuencia (Hz)', ylabel = 'Magnitud (dB)', xlim=(20, f_s_wav / 2), title='Comparacion espectral: WAV vs MP3')
ax.legend(); ax.grid(True, which='both', alpha=0.3)
plt.tight_layout(); plt.show()