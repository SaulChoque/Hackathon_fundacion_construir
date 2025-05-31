import os
import math
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(BASE_DIR, "../assets/video/raw")
output_folder = os.path.join(BASE_DIR, "../assets/video/clips")
clip_length = 30  # segundos

os.makedirs(output_folder, exist_ok=True)

def get_duration(filename):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", filename
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    output = result.stdout.decode().strip()
    try:
        return float(output)
    except ValueError:
        print(f"Error obteniendo duración con ffprobe: {output}")
        raise

# Listar todos los archivos de video en la carpeta raw
video_files = [
    f for f in os.listdir(input_folder)
    if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
]

for video_name in video_files:
    input_path = os.path.join(input_folder, video_name)
    duration = int(get_duration(input_path))
    num_clips = math.ceil(duration / clip_length)

    for i in range(num_clips):
        start = i * clip_length
        end = min((i + 1) * clip_length, duration)
        output_path = os.path.join(
            output_folder,
            f"{os.path.splitext(video_name)[0]}_clip_{start}-{end}.mp4"
        )
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-ss", str(start),
            "-t", str(end - start),
            "-i", input_path,
            "-vf", "crop=ih*9/16:ih",  # Recorte a 9:16 centrado
            "-c:v", "h264_nvenc",
            "-preset", "fast",
            "-c:a", "aac",
            "-y",
            output_path
        ]
        print(f"Procesando {video_name} clip {start}-{end} (recorte 9:16)...")
        subprocess.run(cmd, check=True)

print("¡Listo! Todos los clips verticales han sido generados usando la GPU.")