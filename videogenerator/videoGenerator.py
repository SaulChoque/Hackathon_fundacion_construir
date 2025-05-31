import os
import random
from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

# Rutas de los assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "../assets/audio/output/output.mp3")
PERSONAJE_PATH = os.path.join(BASE_DIR, "../assets/images/characters/bob.jpeg")
CLIPS_DIR = os.path.join(BASE_DIR, "../assets/video/clips")

# Selecciona un video aleatorio de la carpeta clips
clips = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
if not clips:
    raise FileNotFoundError("No se encontraron videos en la carpeta clips.")
video_fondo_path = os.path.join(CLIPS_DIR, random.choice(clips))

# Carga el video de fondo
fondo = VideoFileClip(video_fondo_path)

# Carga el audio generado por texto a voz
audio = AudioFileClip(AUDIO_PATH)

# Carga el personaje y lo sincroniza con el audio
personaje = (ImageClip(PERSONAJE_PATH)
             .with_duration(audio.duration)
             .with_position(("center", "bottom"))
             .resized(height=300))

# Ejemplo de imágenes contextuales (puedes agregar más o parametrizar)
# Aquí se omiten para centrarse en los cambios solicitados

# Composición final
video_final = CompositeVideoClip([fondo, personaje])
video_final = video_final.with_audio(audio)
video_final.write_videofile("video_final.mp4", fps=24)