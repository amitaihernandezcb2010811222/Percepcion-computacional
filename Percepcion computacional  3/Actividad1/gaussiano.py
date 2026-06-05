import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, signal

# Parámetros de la señal
ts = 10000  # frecuencia de muestreo en Hz
mu_real = 0.0
sigma_real = 1.0
N = 10000

# Generar ruido AWGN (gaussiano) con media 0 y desviación estándar 1
ruido = np.random.normal(mu_real, sigma_real, N)

# Estadísticas empíricas
mu_emp = np.mean(ruido)
sigma_emp = np.std(ruido)
sesgo = stats.skew(ruido)
curtosis = stats.kurtosis(ruido)

print(f"Media : real={mu_real:.3f} emp={mu_emp:.3f}")
print(f"Sigma : real={sigma_real:.3f} emp={sigma_emp:.3f}")
print(f"Sesgo : {sesgo:.3f} (ideal=0)")
print(f"Curtosis : {curtosis:.3f} (ideal=0)")

# Calcular espectros en distintos métodos
f_periodo, Pxx_periodo = signal.periodogram(ruido, fs=ts)
f_welch_256, Pxx_welch_256 = signal.welch(ruido, fs=ts, nperseg=256)
f_welch_512, Pxx_welch_512 = signal.welch(ruido, fs=ts, nperseg=512)
f_welch_1024, Pxx_welch_1024 = signal.welch(ruido, fs=ts, nperseg=1024)

# Mostrar serie temporal
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].plot(np.arange(1000), ruido[:1000], color='steelblue', lw=0.8)
axes[0].set(xlabel='Muestras', ylabel='Amplitud', title='Ruido gaussiano (1000 muestras)')
axes[0].grid(True, alpha=0.3)

# Mostrar histograma y PDF teórica
axes[1].hist(ruido, bins=60, density=True, alpha=0.6, color='steelblue', label='Histograma')
x = np.linspace(-5, 5, 300)
pdf_teo = stats.norm.pdf(x, mu_real, sigma_real)
axes[1].plot(x, pdf_teo, color='red', lw=2, label='PDF teórica N(0,1)')
axes[1].set(xlabel='Valor', ylabel='Densidad', title='Histograma vs PDF teórica')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Mostrar espectro en escala log-log 
axes[2].loglog(f_welch_1024[1:], Pxx_welch_1024[1:], color='red', lw=0.8)
axes[2].set(xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)', title='PSD en escala log-log')
axes[2].grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.show()

# Graficar 4 espectros en escala log-log
fig2, axes2 = plt.subplots(2, 2, figsize=(18, 10))

axes2[0, 0].loglog(f_periodo[1:], Pxx_periodo[1:], color='tab:pink')
axes2[0, 0].set(title='Periodograma', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[0, 0].grid(True, which='both', alpha=0.3)

axes2[0, 1].loglog(f_welch_256[1:], Pxx_welch_256[1:], color='tab:whiteblue')
axes2[0, 1].set(title='Welch nperseg=256', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[0, 1].grid(True, which='both', alpha=0.3)

axes2[1, 0].loglog(f_welch_512[1:], Pxx_welch_512[1:], color='tab:yellow')
axes2[1, 0].set(title='Welch nperseg=512', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[1, 0].grid(True, which='both', alpha=0.3)

axes2[1, 1].loglog(f_welch_1024[1:], Pxx_welch_1024[1:], color='tab:red')
axes2[1, 1].set(title='Welch nperseg=1024', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[1, 1].grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.show()