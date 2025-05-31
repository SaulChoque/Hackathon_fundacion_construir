# Ejemplo básico con moviepy
from moviepy import *

# Cargar video de fondo y audio
background = VideoFileClip("fondo.mp4")
audio = AudioFileClip("voz.mp3")

# Cargar personaje (imagen con fondo transparente)
personaje = ImageClip("personaje.png").set_duration(background.duration).set_position(("center", "bottom"))

# Cargar imagen contextual y definir aparición
img_contextual = ImageClip("contexto.png").set_start(10).set_duration(5).set_position(("right", "top"))

# Componer el video
final = CompositeVideoClip([background, personaje, img_contextual])
final = final.set_audio(audio)
final.write_videofile("video_final.mp4", fps=24)