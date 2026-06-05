import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Generar ruido AWGN con parametros conocidos
np.random.seed(42) #Reproducibilidad
mu_real = 0.0 #Media teorica del ruido 
sigma_real = 1.0 #Desviacion estandar teorica del ruido
N = 10000 #Numero de muestras de ruido a generar

ruido = np.random.normal(mu_real, sigma_real, N)

#Estadisticas empriricos 
mu_emp = np.mean(ruido)
sigma_emp = np.std(ruido)
sesgo = stats.skew(ruido)
curtosis = stats.kurtosis(ruido)

print(f"Media : real={mu_real:.3f} emp={mu_emp:.3f}")
print(f"Sigma : real={sigma_real:.3f} emp={sigma_emp:.3f}")
print(f"Sesgo : {sesgo:.3f} (ideal=0)")
print(f"Curtosis : {curtosis:.3f} (ideal=0)")

#Histograma del ruido vs PDF teorica
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

#(a) Serie temporal del ruido
axes[0].plot(ruido[:500], color='steelblue', lw = 0.6)
axes[0].set(xlabel='Muestras', ylabel='Amplitud', title='Primeras 500 muestras del ruido')
axes[0].grid(True, alpha=0.3)

#(b) Histograma del ruido y PDF teorica
axes[1].hist(ruido, bins=60, density=True, alpha=0.6, color='steelblue', label='Histograma empirico')
x = np.linspace(-5, 5, 200)
pdf_teo = stats.norm.pdf(x, mu_real, sigma_real)
axes[1].plot(x, pdf_teo, 'r-', lw=2, label='PDF teorica N(0,1)')
axes[1].set(xlabel='Valor', ylabel='Densidad de probabilidad', title='Distribucion empirica vs teorica del ruido')

axes[1].legend(); axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()