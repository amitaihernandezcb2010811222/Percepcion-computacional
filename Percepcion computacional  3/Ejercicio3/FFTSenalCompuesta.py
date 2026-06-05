import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq

# Senal: suma de 3 senoidales (50, 120, 300 Hz)
f_s = 1000 # Hz-frecuencia de muestreo
T = 2.0 # s-duracion
t = np.arange(0, T, 1 / f_s)

frecuencias = [50, 120, 300]
amplitudes = [1.0, 0.5, 0.3]

senal = np.zeros_like(t)
for f, A in zip(frecuencias, amplitudes):
    senal += A * np.sin(2 * np.pi * f * t)

# Agregar ruido AWGN moderado
senal_ruidosa = senal + np.random.normal(0, 0.2, len(t))

# Calcular FFT
N = len(senal_ruidosa)
X = rfft(senal_ruidosa)
frec_eje = rfftfreq(N, 1 / f_s)
mag = np.abs(X) / N * 2

fig, axes = plt.subplots(2, 1, figsize=(12, 6))

# (a) Senal en tiempo
axes[0].plot(t[:500], senal_ruidosa[:500], color='steelblue', lw=0.8)
axes[0].set(xlabel='Tiempo (s)', ylabel='Amplitud',
title='Senal compuesta + ruido (primeros 500 ms)')
axes[0].grid(True, alpha=0.3)

# (b) Espectro de magnitud
axes[1].plot(frec_eje, mag, color='darkred', lw=1)
for f, A in zip(frecuencias, amplitudes):
    axes[1].axvline(f, color='gray', ls=':', alpha=0.6)
    axes[1].annotate(f'{f} Hz', xy=(f, A), xytext=(f+10, A+0.05),fontsize=9, color='black')

axes[1].set(xlabel='Frecuencia (Hz)', ylabel='Magnitud',xlim=(0, 500),title='Espectro: 3 picos donde se inyectaron las senoidales')
axes[1].grid(True, alpha=0.3)

plt.tight_layout(); plt.show()