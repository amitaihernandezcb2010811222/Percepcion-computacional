import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.ensemble import IsolationForest

# ECG 
f_s = 500; T = 3.0
t = np.arange(0, T, 1 / f_s)

# QRS 
ecg_limpio = np.zeros_like(t)
for tc in np.arange(0.5, T, 1/1.2):
    pulso = np.exp(-((t- tc) ** 2) / 0.002)
    ecg_limpio += pulso

# Contaminacion: EMI 60 Hz + ruido AWGN suave
emi = 0.2 * np.sin(2 * np.pi * 0.3 * t)
ecg_sucio = ecg_limpio + emi + np.random.normal(0, 0.1, len(t))

#Generar 5 indices (posiciones) completamente al azr dela longitud de la señal
artefactos_puntuales = np.random.choice (len(t), size=5, replace=False)

# Innsertar picos de amplitud 3 en esas posiciones
ecg_sucio[artefactos_puntuales] += 3

# Z-score robusto
mediana = np.median(ecg_sucio)
mad = np.median(np.abs(ecg_sucio - mediana))
z_rob = 0.6745 * (ecg_sucio - mediana) / mad

umbral = 3.5
anomalias = np.where(np.abs(z_rob) > umbral)[0]

print(f"Anomalias detectadas en: {anomalias}")
print(f"Esperadas (inyectadas): {artefactos_puntuales}")

#Filtro pasa-altos Butterworth de 0.5 Hz
f_alto = 0.5
orden = 4
b, a = signal.butter(orden, f_alto, btype='high', fs=f_s)
ecg_filtrado = signal.filtfilt(b, a, ecg_sucio)

# Filtro Notch en 60 Hz 
f_notch = 60; Q = 30
b, a = signal.iirnotch(f_notch, Q, f_s)
ecg_filtrado = signal.filtfilt(b, a, ecg_sucio)

# Diseno del filtro pasa-bajos Butterworth orden 4, fc=100 Hz
f_baja = 40 # Hz
orden = 4
b, a = signal.butter(orden, f_baja, btype='low', fs=f_s)
ecg_filtrado = signal.filtfilt(b, a, ecg_sucio)
# Isolation Forest para deteccion de anomalías (picos)
datos_ml = ecg_sucio.reshape(-1, 1)
iso_forest = IsolationForest(contamination=0.01, random_state=42)

predicciones = iso_forest.fit_predict(datos_ml)
indices_anomalias_if = np.where(predicciones == -1)[0]

print(f"El Isolation Forest encontro anomalias en las posiciones: {indices_anomalias_if}")

senal_limpia_ml = ecg_sucio.copy()
for i in indices_anomalias_if:
    if i > 0:
        senal_limpia_ml[i] = senal_limpia_ml[i-1]
    else:
        senal_limpia_ml[i] = 0

fig, axes = plt.subplots(6, 1, figsize=(13, 7), sharex=True)


#Visualizar la señal limpia, sucia, z-score, y comparacion entre limpio y filtrado
axes[0].plot(t, ecg_limpio, color='pink', lw=0.8)
axes[0].set(ylabel='Amplitud', title='ECG limpio ')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, ecg_sucio, color='purple', lw=0.6)
axes[1].set(ylabel='Amplitud', title='ECG + EMI 60 Hz + AWGN')
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, z_rob, color='purple', lw=0.8)
axes[2].axhline( umbral, color='r', ls='--', label=f'+/-{umbral} sigma')
axes[2].axhline(-umbral, color='r', ls='--')
axes[2].fill_between(t,-umbral, umbral, color='purple', alpha=0.05)
axes[2].set(xlabel='Tiempo (s)', ylabel='Z-score robusto',title='Z-score con umbral de deteccion')
axes[2].legend(); axes[2].grid(True, alpha=0.3)

#Visualizar filtros pasa-altos, notch y pasa-bajos
axes[3].plot(t, ecg_filtrado, color='steelblue', lw=0.8, label='ECG filtrado')
axes[3].set(xlabel='Tiempo (s)', ylabel='Amplitud', title='Filtros de frecuencia')
axes[3].legend()
axes[3].grid(True, alpha=0.3)

axes[4].plot(t, ecg_limpio, color='pink', lw=0.8, label='ECG limpio')
axes[4].plot(t, ecg_filtrado, color='darkred', lw=0.8, label='ECG filtrado')
axes[4].set(xlabel='Tiempo (s)', ylabel='Amplitud', title='Comparacion ECG limpio vs filtrado')
axes[4].legend()
axes[4].grid(True, alpha=0.3)

axes[5].plot(t, ecg_sucio, label='Señal con Artefactos', color='gray', alpha=0.5)
axes[5].plot(t, senal_limpia_ml, label='Señal Limpiada (Isolation Forest)', color='blue', alpha=0.8)
axes[5].scatter(t[indices_anomalias_if], ecg_sucio[indices_anomalias_if], color='red', label='Anomalías Detectadas (ML)', zorder=5)
axes[5].set(xlabel='Muestras', ylabel='Amplitud', title='Deteccion y eliminacion de anomalias usando Isolation Forest')
axes[5].legend()
axes[5].grid(True, alpha=0.3)


plt.tight_layout()
plt.show()

# Calcular SNR antes y despues
def snr(limpio, sucio):
    return 10 * np.log10(np.mean(limpio**2) / np.mean((sucio- limpio)**2))

print(f"SNR antes : {snr(ecg_limpio, ecg_sucio):.1f} dB")
print(f"SNR despues: {snr(ecg_limpio, ecg_filtrado) :.1f} dB")

error_RMS= np.sqrt(np.mean((ecg_limpio - ecg_filtrado) ** 2))
print(f"Error RMS despues del filtrado: {error_RMS:.4f}")
