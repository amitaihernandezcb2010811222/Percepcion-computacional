import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, signal

# Parámetros de la señal
ts = 10000  # frecuencia de muestreo en Hz
mu_real = 0.0
sigma_real = 1.0
N = 10000

# Función para generar ruido rosa (1/f)
def generar_ruido_rosa(N):
    """Genera ruido rosa mediante filtrado en el dominio de frecuencia"""
    ruido_blanco = np.random.normal(0, 1, N)
    fft = np.fft.fft(ruido_blanco)
    S = np.sqrt(np.arange(1, N//2 + 1))  
    S[0] = 1  
    fft[:N//2] /= S
    fft[-(N//2-1):] = np.conj(fft[1:N//2])
    return np.real(np.fft.ifft(fft))

# Función para generar ruido marrón (1/f²)
def generar_ruido_marron(N):
    """Genera ruido marrón mediante integración de ruido rosa"""
    ruido_p = generar_ruido_rosa(N)
    return np.cumsum(ruido_p) / np.std(np.cumsum(ruido_p))

# Generar los tres tipos de ruido
ruido_blanco = np.random.normal(mu_real, sigma_real, N)
ruido_rosa = generar_ruido_rosa(N)
ruido_marron = generar_ruido_marron(N)

# Estadísticas empíricas - Ruido Blanco
mu_emp = np.mean(ruido_blanco)
sigma_emp = np.std(ruido_blanco)
sesgo = stats.skew(ruido_blanco)
curtosis = stats.kurtosis(ruido_blanco)

print("RUIDO BLANCO")
print(f"Media : real={mu_real:.3f} emp={mu_emp:.3f}")
print(f"Sigma : real={sigma_real:.3f} emp={sigma_emp:.3f}")
print(f"Sesgo : {sesgo:.3f} (ideal=0)")
print(f"Curtosis : {curtosis:.3f} (ideal=0)")

# Calcular espectros para RUIDO BLANCO
f_wb, Pxx_wb = signal.welch(ruido_blanco, fs=ts, nperseg=1024)

# Calcular espectros para RUIDO ROSA
f_wr, Pxx_wr = signal.welch(ruido_rosa, fs=ts, nperseg=1024)

# Calcular espectros para RUIDO MARRÓN
f_wm, Pxx_wm = signal.welch(ruido_marron, fs=ts, nperseg=1024)

# Mostrar serie temporal y histograma de los tres tipos de ruido
fig, axes = plt.subplots(3, 2, figsize=(14, 10))

# Ruido Blanco
axes[0, 0].plot(np.arange(1000), ruido_blanco[:1000], color='steelblue', lw=0.6)
axes[0, 0].set(xlabel='Muestras', ylabel='Amplitud', title='Serie Temporal - Ruido Blanco')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(ruido_blanco, bins=60, density=True, alpha=0.6, color='steelblue', label='Histograma')
x = np.linspace(-5, 5, 300)
pdf_teo = stats.norm.pdf(x, mu_real, sigma_real)
axes[0, 1].plot(x, pdf_teo, color='red', lw=2, label='PDF teórica N(0,1)')
axes[0, 1].set(xlabel='Valor', ylabel='Densidad', title='Histograma - Ruido Blanco')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Ruido Rosa
axes[1, 0].plot(np.arange(1000), ruido_rosa[:1000], color='darkorange', lw=0.6)
axes[1, 0].set(xlabel='Muestras', ylabel='Amplitud', title='Serie Temporal - Ruido Rosa')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].hist(ruido_rosa, bins=60, density=True, alpha=0.6, color='darkorange', label='Histograma')
axes[1, 1].plot(x, pdf_teo, color='red', lw=2, label='PDF teórica N(0,1)')
axes[1, 1].set(xlabel='Valor', ylabel='Densidad', title='Histograma - Ruido Rosa')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Ruido Marrón
axes[2, 0].plot(np.arange(1000), ruido_marron[:1000], color='brown', lw=0.6)
axes[2, 0].set(xlabel='Muestras', ylabel='Amplitud', title='Serie Temporal - Ruido Marrón')
axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].hist(ruido_marron, bins=60, density=True, alpha=0.6, color='brown', label='Histograma')
axes[2, 1].plot(x, pdf_teo, color='red', lw=2, label='PDF teórica N(0,1)')
axes[2, 1].set(xlabel='Valor', ylabel='Densidad', title='Histograma - Ruido Marrón')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Graficar 4 espectros en escala log-log: Blanco, Rosa, Marrón y comparación
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))

axes2[0, 0].loglog(f_wb[1:], Pxx_wb[1:], color='steelblue', lw=2, label='Ruido Blanco')
axes2[0, 0].set(title='PSD - Ruido Blanco (1/f⁰)', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[0, 0].grid(True, which='both', alpha=0.3)
axes2[0, 0].legend()

axes2[0, 1].loglog(f_wr[1:], Pxx_wr[1:], color='darkorange', lw=2, label='Ruido Rosa')
axes2[0, 1].set(title='PSD - Ruido Rosa (1/f)', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[0, 1].grid(True, which='both', alpha=0.3)
axes2[0, 1].legend()

axes2[1, 0].loglog(f_wm[1:], Pxx_wm[1:], color='brown', lw=2, label='Ruido Marrón')
axes2[1, 0].set(title='PSD - Ruido Marrón (1/f²)', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[1, 0].grid(True, which='both', alpha=0.3)
axes2[1, 0].legend()

# Comparación de los tres en una sola gráfica
axes2[1, 1].loglog(f_wb[1:], Pxx_wb[1:], color='steelblue', lw=2, label='Blanco (1/f⁰)')
axes2[1, 1].loglog(f_wr[1:], Pxx_wr[1:], color='darkorange', lw=2, label='Rosa (1/f)')
axes2[1, 1].loglog(f_wm[1:], Pxx_wm[1:], color='brown', lw=2, label='Marrón (1/f²)')
axes2[1, 1].set(title='Comparación de PSD - Todos los tipos', xlabel='Frecuencia (Hz)', ylabel='PSD (V²/Hz)')
axes2[1, 1].grid(True, which='both', alpha=0.3)
axes2[1, 1].legend()

plt.tight_layout()
plt.show()