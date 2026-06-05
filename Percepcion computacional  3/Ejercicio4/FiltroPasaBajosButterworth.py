import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

 # Senal: 50 Hz (interes) + 300 Hz (ruido alta frecuencia)
f_s = 1000; T = 1.0
t = np.arange(0, T, 1 / f_s)
util = np.sin(2 * np.pi * 50 * t)
basura = 0.6 * np.sin(2 * np.pi * 300 * t)
senal = util + basura + np.random.normal(0, 0.1, len(t))

# Diseno del filtro pasa-bajos Butterworth orden 4, fc=100 Hz
f_corte = 100 # Hz
orden = 4
b, a = signal.butter(orden, f_corte, btype='low', fs=f_s)

# Aplicar con filtfilt (fase cero)
senal_filtrada = signal.filtfilt(b, a, senal)

 # Respuesta en frecuencia del filtro
w, h = signal.freqz(b, a, fs=f_s)

fig, axes = plt.subplots(3, 1, figsize=(12, 7))

# (a) Senal original vs filtrada
axes[0].plot(t[:200], senal[:200], color='gray', alpha=0.6, label='Original')
axes[0].plot(t[:200], senal_filtrada[:200], color='darkred', lw=1.5, label='Filtrada')
axes[0].plot(t[:200], util[:200], color='green', ls='--', label='Util (50 Hz)')
axes[0].set(xlabel='Tiempo (s)', ylabel='Amplitud',
title='Senal cruda vs filtrada (primeros 200 ms)')
axes[0].legend(); axes[0].grid(True, alpha=0.3)

# (b) Respuesta en magnitud del filtro
axes[1].semilogx(w, 20 * np.log10(np.abs(h)), color='steelblue')
axes[1].axvline(f_corte, color='r', ls='--', label=f'fc = {f_corte} Hz')
axes[1].axhline(-3, color='gray', ls=':')
axes[1].set(xlabel='Frecuencia (Hz)', ylabel='Magnitud (dB)',title=f'Respuesta del Butterworth (orden {orden})')
axes[1].legend(); axes[1].grid(True, which='both', alpha=0.3)

# (c) Espectros comparados
from scipy.fft import rfft, rfftfreq
N = len(senal); f = rfftfreq(N, 1/f_s)
axes[2].plot(f, np.abs(rfft(senal))/N*2, color='gray', label='Antes')
axes[2].plot(f, np.abs(rfft(senal_filtrada))/N*2, color='darkred', label='Despues')
axes[2].set(xlim=(0, 500), xlabel='Frecuencia (Hz)', ylabel='Magnitud',title='Espectros antes y despues del filtrado')
axes[2].legend(); axes[2].grid(True, alpha=0.3)

plt.tight_layout(); plt.show()