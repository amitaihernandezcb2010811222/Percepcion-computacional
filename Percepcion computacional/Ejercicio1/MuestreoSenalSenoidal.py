import numpy as np
import matplotlib.pyplot as plt

# 1. PARAMETROS 
f_senal = 5 #Frecuencia de la senal ORIGINAL (Hz)
            #La ONDA SENOIDAL completa un ciclo 5 veces x segundo
f_s = 50 #Frecuencia de MUESTRAS x segundo (Hz)
T= 1.0 #Duracion de la senal (s)

# 2. Senal ANALOGICA simulada (ALTA resolucion temporal) #cont = continuo
t_cont = np.linspace(0, T, 2000) # Crea 2000 puntos entre 0 y T (1) s para simular el tiempo continuo
x_cont = np.sin(2 * np.pi * f_senal * t_cont) #SENAL ANALOGICA  # 2π×f×t es la fórmula estándar

# 3.  Senal MUESTREADA (discreta) #disc = discreto
t_disc = np.arange(0, T, 1/f_s) # Eje Tiempo discreto. Crea puntos cada 1/50 = 0.02 sg entre 0 y T (1) s
                                # Ejemplo: [0, 0.02, 0.04, 0.06, ..., 0.98]
x_disc = np.sin(2 * np.pi * f_senal * t_disc) #SENAL MUESTREADA.Calcula la onda 


# VISUALIZACION
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(t_cont, x_cont, label='SENAL CONTINUA (5 Hz)', color='steelblue', lw=1.5)
ax.stem(t_disc, x_disc, label=f'MUESTRAS (fs={f_s} Hz)', linefmt='r-', markerfmt='ro', basefmt="k-")
ax.set(xlabel='Tiempo (s)', ylabel='Amplitud', title='Muestreo Correcto: fs = 50 Hz > 2 x 5 Hz = 10 Hz')
ax.legend(); ax.grid(True, alpha=0.35)

plt.tight_layout(); plt.show() 