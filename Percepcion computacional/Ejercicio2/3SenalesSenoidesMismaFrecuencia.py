import numpy as np
import matplotlib.pyplot as plt

# PARAMETROS 
f_s = 20 #Hz - Frecuencia de muestreo fija
T = 1.0 #s - Duracion de la senal 
freqs = [3, 10, 17, 25] #Hz 3:OK 10:Limite Nyquist 17:ALIASING

# Senal ANALOGICA simulada (ALTA resolucion temporal)
t_cont = np.linspace(0, T, 2000) # Eje Tiempo continuo
t_disc = np.arange(0, T, 1/f_s) # Eje Tiempo discreto

fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, f in zip(axes, freqs):
    x_cont = np.sin(2 * np.pi * f * t_cont) #SENAL ANALOGICA
    x_disc = np.sin(2 * np.pi * f * t_disc) #SENAL MUESTREADA

    # Frecuencia de alias resultante 
    f_alias = abs(f - round(f / f_s) * f_s)

    ax.plot(t_cont, x_cont, 'steelblue', alpha=0.5, lw=1.2, label=f'SENAL CONTINUA ORIGINAL ({f} Hz)')
    ax.stem(t_disc, x_disc, linefmt='r-', markerfmt='ro', basefmt="k-", label=f'MUESTRAS (fs={f_s} Hz)')
    if f > f_s / 2:
        titulo = f'f = {f} Hz \ n [!] ALIASING = {f_alias} Hz'
    else:
        titulo = f'f = {f} Hz \ n [OK] Sin Aliasing'
    ax.set_title(titulo, fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.35)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')

fig.suptitle(f'Efecto Aliasing  (f_s={f_s} Hz, Nyquist={f_s/2} Hz)', fontsize=12, fontweight='bold')
plt.tight_layout();
plt.show()