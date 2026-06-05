import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ECG sintetico simple + ruido EMI 60 Hz + AWGN
f_s = 500; T = 5.0
frecuencia_corte = 0.5
t = np.arange(0, T, 1 / f_s)

# QRS aproximado: pulsos cardiacos a ~1.2 Hz (72 bpm)
ecg_limpio = np.zeros_like(t)
for tc in np.arange(0.5, T, 1/1.2):
    pulso = np.exp(-((t- tc) ** 2) / 0.002)
    ecg_limpio += pulso

# Contaminacion: EMI 60 Hz + ruido AWGN suave
emi = 0.3 * np.sin(2 * np.pi * 60 * t)
ecg_sucio = ecg_limpio + emi + np.random.normal(0, 0.05, len(t))

# Filtro Notch en 60 Hz (Q = factor de calidad)
f_notch = 60; Q = 30
b, a = signal.iirnotch(f_notch, Q, f_s)
ecg_filt = signal.filtfilt(b, a, ecg_sucio)

fig, axes = plt.subplots(3, 1, figsize=(13, 7), sharex=True)

axes[0].plot(t, ecg_limpio, color='green', lw=0.8)
axes[0].set(ylabel='Amplitud', title='ECG limpio (referencia)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, ecg_sucio, color='gray', lw=0.6)
axes[1].set(ylabel='Amplitud', title='ECG + EMI 60 Hz + AWGN')
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, ecg_filt, color='darkred', lw=0.8)
axes[2].set(xlabel='Tiempo (s)', ylabel='Amplitud',title='ECG despues del filtro Notch a 60 Hz')
axes[2].grid(True, alpha=0.3)

plt.tight_layout(); plt.show()

# Calcular SNR antes y despues
def snr(limpio, sucio):
    return 10 * np.log10(np.mean(limpio**2) / np.mean((sucio- limpio)**2))

print(f"SNR antes : {snr(ecg_limpio, ecg_sucio):.1f} dB")
print(f"SNR despues: {snr(ecg_limpio, ecg_filt) :.1f} dB")