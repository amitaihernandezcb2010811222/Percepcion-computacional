import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Cargar audio (puede ser un MP3, WAV, FLAC, OGG...)
ruta_audio = librosa.example('trumpet') # muestra incluida en librosa

# Alternativa: ruta_audio = 'mi_audio.wav'

senal, f_s = librosa.load(ruta_audio, sr=None)
print(f"Audio cargado: {len(senal)} muestras a {f_s} Hz "f"({len(senal)/f_s:.2f} s)")

# Calcular STFT (Short-Time Fourier Transform)
n_fft = 2048 # tamano de ventana FFT
hop_length = 512 # paso entre ventanas

stft = librosa.stft(senal, n_fft=n_fft, hop_length=hop_length)
mag_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

fig, axes = plt.subplots(2, 1, figsize=(13, 7))

# (a) Forma de onda en el tiempo
t = np.arange(len(senal)) / f_s
axes[0].plot(t, senal, color='steelblue', lw=0.4)
axes[0].set(xlabel='Tiempo (s)', ylabel='Amplitud',title='Forma de onda')
axes[0].grid(True, alpha=0.3)

# (b) Spectrogram (mapa de calor)
img = librosa.display.specshow(mag_db, sr=f_s, hop_length=hop_length,
x_axis='time', y_axis='log', ax=axes[1],
cmap='magma')
axes[1].set(title='Spectrogram (escala log de frecuencia)')
fig.colorbar(img, ax=axes[1], format='%+2.0f dB')

plt.tight_layout(); plt.show()