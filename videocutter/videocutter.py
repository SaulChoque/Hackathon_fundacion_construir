import os
from moviepy import VideoFileClip

# ...resto del código...

# Carpeta de videos de entrada y salida
input_folder = "assets/video/raw"
output_folder = "assets/video/clips"
os.makedirs(output_folder, exist_ok=True)

# Nombre del video a cortar (puedes cambiarlo por el que quieras)
video_name = "lpz.2.mp4"
video_path = os.path.join(input_folder, video_name)

# Cargar el video
video = VideoFileClip(video_path)
duration = int(video.duration)
clip_length = 30  # segundos

# Cortar en clips de 30s
for i in range(0, duration, clip_length):
    start = i
    end = min(i + clip_length, duration)
    clip = video.subclipped(start, end)
    output_path = os.path.join(output_folder, f"{os.path.splitext(video_name)[0]}_clip_{start}-{end}.mp4")
    clip.write_videofile(
        output_path,
        codec="h264_nvenc",      # Usa la GPU NVIDIA para codificar
        audio_codec="aac",
        ffmpeg_params=[
            "-hwaccel", "cuda",  # Intenta usar la GPU para decodificar
            "-preset", "fast"
        ]
    )
video.close()