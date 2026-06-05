import numpy as np
import matplotlib.pyplot as plt

# Serie temporal sintetica: temperatura horaria con outliers

np.random.seed(0)
horas = np.arange(0, 168) # 1 semana
temp_base = 22 + 3 * np.sin(2 * np.pi * horas / 24) # ciclo diario
ruido = np.random.normal(0, 0.5, len(horas))
temp = temp_base + ruido

# Inyectar 4 anomalias (fallos del sensor)
indices_falla = [30, 75, 120, 145]
temp[indices_falla] += [12,-8, 15,-10]

# Z-score robusto (basado en mediana y MAD)
mediana = np.median(temp)
mad = np.median(np.abs(temp- mediana))
z_rob = 0.6745 * (temp- mediana) / mad

umbral = 3.5
anomalias = np.where(np.abs(z_rob) > umbral)[0]

print(f"Anomalias detectadas en: {anomalias}")
print(f"Esperadas (inyectadas): {indices_falla}")

fig, axes = plt.subplots(2, 1, figsize=(13, 6), sharex=True)

# (a) Serie temporal con anomalias destacadas
axes[0].plot(horas, temp, color='steelblue', lw=1, label='Temperatura')
axes[0].scatter(horas[anomalias], temp[anomalias], color='red',s=80, zorder=5, label='Anomalia detectada')
axes[0].set(ylabel='Temperatura (C)',title='Serie temporal con anomalias detectadas')
axes[0].legend(); axes[0].grid(True, alpha=0.3)


# (b) Z-score robusto con umbral
axes[1].plot(horas, z_rob, color='darkgreen', lw=1)
axes[1].axhline( umbral, color='r', ls='--', label=f'+/-{umbral} sigma')
axes[1].axhline(-umbral, color='r', ls='--')
axes[1].fill_between(horas,-umbral, umbral, color='green', alpha=0.05)
axes[1].set(xlabel='Hora', ylabel='Z-score robusto',title='Z-score con umbral de deteccion')
axes[1].legend(); axes[1].grid(True, alpha=0.3)
plt.tight_layout(); plt.show()