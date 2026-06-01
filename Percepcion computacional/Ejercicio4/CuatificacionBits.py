import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 800) # Tiempo continuo
senal = np.sin(2 * np.pi * 3 * t) # Señal analógica (3 Hz)

def cuantificar(senal, bits):
    """Cuantifica la señal analógica a un número específico de bits. En rango [-1,1]"""
    niveles = 2 ** bits
    norm = (senal + 1) / 2 # Normalizar a [0,1]
    idx = np.round(norm * (niveles - 1)).astype(int) # Índice del nivel cuantificado
    idx = np.clip(idx, 0, niveles - 1) # Asegurar que el índice esté dentro de los niveles
    return (idx / (niveles - 1)) * 2 - 1 # Devolver a rango [-1,1]

def snr_real(bits):
    """SNR medido en dB (comparacion directa ORIGINAL vs CUANTIFICADA)"""
    x_q = cuantificar(senal, bits)
    return 10 * np.log10(np.mean(senal**2) / np.mean((senal - x_q)**2))

fig, axes = plt.subplots(4, 1, figsize=(12, 8))

for ax, bits in zip(axes, [2, 4, 8,16]):
    x_q = cuantificar(senal, bits)
    snr_medido = snr_real(bits)
    snr_teo = 6.02 * bits + 1.76 # SNR teórico para cuantificación uniforme

    ax.plot(t, senal, 'b-', alpha=0.4, label='Señal Original', color='steelblue', lw=1.5)
    ax.step(t, x_q, 'r-', where='post', label=f'Señal Cuantificada ({bits} bits) - SNR: {snr_medido:.1f} dB', color='red')
    ax.set_title(f'Cuantificación con {bits} bits (Niveles: {2**bits})', fontsize=10)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

fig.suptitle('Efecto de la Cuantificación por numero de bits', fontsize=12, fontweight='bold')
plt.tight_layout();
plt.show()