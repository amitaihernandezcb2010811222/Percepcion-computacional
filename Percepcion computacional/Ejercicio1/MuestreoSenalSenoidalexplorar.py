import numpy as np
import matplotlib.pyplot as plt

# PARAMETROS 
f_senal = 8 #Frecuencia de la senal ORIGINAL 
f_s = 12 #Frecuencia de muestreo
T = 1.0 #Duracion de la senal

# Senal ANALOGICA simulada (ALTA resolucion temporal)
t_cont = np.linspace(0, T, 2000) # Eje Tiempo continuo
x_cont = np.sin(2 * np.pi * f_senal * t_cont) #SENAL ANALOGICA

# Senal MUESTREADA (discreta)
t_disc = np.arange(0, T, 1/f_s) # Eje Tiempo discreto
x_disc = np.sin(2 * np.pi * f_senal * t_disc) #SENAL MUESTREADA

# VISUALIZACION
fig, ax = plt.subplots(2, 1, figsize=(10, 4))
ax[0].plot(t_cont, x_cont, label='SENAL CONTINUA (8 Hz)', color='steelblue', lw=1.5)
ax[0].stem(t_disc, x_disc, label=f'MUESTRAS (fs={f_s} Hz)', linefmt='r-', markerfmt='ro', basefmt="k-")
ax[0].set(xlabel='Tiempo (s)', ylabel='Amplitud', title='Muestreo Incorrecto: fs = 12 Hz < 2 x 8 Hz = 16 Hz')
ax[0].legend(); ax[0].grid(True, alpha=0.35)

plt.tight_layout(); plt.show() 