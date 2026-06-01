import numpy as np
import matplotlib.pyplot as plt

# PARAMETROS 
f_senal = 8 #Frecuencia de la senal ORIGINAL 
f_s_values = [15, 16, 20] #Diferentes frecuencias de muestreo
T = 1.0 #Duracion de la senal

# Senal ANALOGICA simulada (ALTA resolucion temporal)
t_cont = np.linspace(0, T, 2000) # Eje Tiempo continuo
x_cont = np.sin(2 * np.pi * f_senal * t_cont) #SENAL ANALOGICA

# VISUALIZACION - 3 subplots para cada frecuencia de muestreo
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

for ax, f_s in zip(axes, f_s_values):
    # Senal MUESTREADA para este valor de f_s
    t_disc = np.arange(0, T, 1/f_s)
    x_disc = np.sin(2 * np.pi * f_senal * t_disc)
    
    # Calcular si cumple el criterio de Nyquist
    f_nyquist = 2 * f_senal
    cumple_nyquist = "✓ CUMPLE" if f_s > f_nyquist else "✗ ALIASING"
    
    # Graficar
    ax.plot(t_cont, x_cont, label=f'Señal Continua ({f_senal} Hz)', color='steelblue', lw=2, alpha=0.7)
    ax.stem(t_disc, x_disc, label=f'Muestras (fs={f_s} Hz)', linefmt='r-', markerfmt='ro', basefmt='k-')
    
    # Configurar el subplot
    ax.set(xlabel='Tiempo (s)', ylabel='Amplitud', title=f'fs = {f_s} Hz vs Nyquist = {f_nyquist} Hz → {cumple_nyquist}') 
    ax.legend(); ax.grid(True, alpha=0.35)
    ax.set_ylim(-1.5, 1.5)  # Ejes consistentes

plt.tight_layout(); plt.show()