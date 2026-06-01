import numpy as np
import matplotlib.pyplot as plt
import librosa      # Carga Universal (WAV / MP3 / FLAC)
from IPython.display import Audio # Reproduce en Jupyter / Colab

# CARGA DE AUDIO 
ruta_wav = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Ejercicio5\\40142__showster1232000__loop36.wav' 

senal, f_s = librosa.load(ruta_wav, sr=None) # sr=None mantiene la frecuencia original

# Informacion basica del archivo 
print(f"Frecuencia de muestreo: {f_s} Hz")
print(f"Numero de muestras: {len(senal)}")
print(f"Duracion del audio: {len(senal)/f_s:.2f} segundos")
print(f"Rango de amplitud: [{senal.min():.3f}, {senal.max():.3f}]")

Audio(senal, rate=f_s) # Reproduce el audio cargado

# VISUALIZACION
t = np.arange(len(senal)) / f_s
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

ax1.plot(t, senal, color='steelblue', lw=0.5)
ax1.set_xlabel('Tiempo [s]')
ax1.set_ylabel('Amplitud')
ax1.set_title(f'Forma de onda completa (fs = {f_s} Hz)')
ax1.grid(True, alpha=0.3)

# Zoom: 50 ms del audio para ver la estructura periodica
inicio = int(1.0 * f_s) # 1 segundo
fin = inicio + int(0.05 * f_s) # 50 ms despues
ax2.plot(t[inicio:fin], senal[inicio:fin], color='darkred', lw=1)
ax2.set_xlabel('Tiempo [s]')
ax2.set_ylabel('Amplitud')
ax2.set_title('Zoom: 50 ms de la señal (se observa periodicidad)')
ax2.grid(True, alpha=0.3)

plt.tight_layout(); plt.show()