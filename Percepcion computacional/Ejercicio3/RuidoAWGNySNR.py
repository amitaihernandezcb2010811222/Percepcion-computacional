import numpy as np
import matplotlib.pyplot as plt

# Parametros 
f_s = 500
T = 1.0
t = np.arange(0, T, 1/f_s)
senal = np.sin(2 * np.pi * 10 * t) 

def agregar_ruido(senal, snr_db):
    """Agrega ruido AWGN  con el SNR objetivo en dB."""
    # Calcular la potencia de la señal
    potencia_senal = np.mean(senal**2)
    
    # Calcular la potencia del ruido necesario para alcanzar el SNR deseado
    potencia_n = potencia_senal / (10**(snr_db/10))
    
    # Generar ruido AWGN
    ruido = np.random.normal(0, np.sqrt(potencia_n), senal.shape)
    return senal + ruido

def calcular_snr(original, contaminada):
    """Calcula el SNR en dB entre la señal original y la contaminada."""
    ruido = contaminada - original
    return 10 * np.log10(np.mean(original**2) / np.mean(ruido**2))

fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

for ax, snr_obj in zip(axes, [30,10,0]):
    x_ruidosa = agregar_ruido(senal, snr_obj)
    snr_real = calcular_snr(senal, x_ruidosa)
    ax.plot(t, x_ruidosa, label=f'Señal Original + Ruido (SNR: {snr_obj} dB | medido: {snr_real:.1f} dB)', color='steelblue', lw=0.8)
    ax.plot(t, senal, 'r--', label='Señal Original', lw=1.5, alpha=0.7)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('Amplitud')

axes[-1].set_xlabel('Tiempo (s)')
fig.suptitle('Efecto del Ruido AWGN en distintos niveles de SNR', fontsize=12, fontweight='bold')
plt.tight_layout();
plt.show()
