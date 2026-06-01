import os
import sys

# Rutas de audio
wav_path = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Actividad2\\100269__uknow-dude__loop-addon-4-122-bpm.wav'
mp3_path = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Actividad2\\100269__uknow-dude__loop-addon-4-122-bpm_1.mp3'
flac_path = 'C:\\Users\\Usuario\\Downloads\\Percepcion computacional\\Actividad2\\100269__uknow-dude__loop-addon-4-122-bpm.flac'

def is_running_in_notebook():
	try:
		from IPython import get_ipython
		ip = get_ipython()
		return ip is not None
	except Exception:
		return False

if is_running_in_notebook():
	# En notebook Jupyter/Colab: usar el reproductor embebido
	from IPython.display import Audio, display
	print("Reproduciendo archivo WAV:")
	display(Audio(filename=wav_path))
	print("Reproduciendo archivo MP3:")
	display(Audio(filename=mp3_path))
	print("Reproduciendo archivo FLAC:")
	display(Audio(filename=flac_path))
else:
	# En un script normal: usar playsound (instalar con `pip install playsound`)
	try:
		from playsound import playsound
	except Exception as e:
		print('No se puede importar playsound. Instala con: pip install playsound')
		print('Error:', e)
		sys.exit(1)

	def play_if_exists(path):
		if os.path.exists(path):
			print(f'Reproduciendo: {path}')
			try:
				playsound(path)
			except Exception as e:
				print(f'Error al reproducir {path}:', e)
		else:
			print(f'Archivo no encontrado: {path}')

	play_if_exists(wav_path)
	play_if_exists(mp3_path)
	play_if_exists(flac_path)