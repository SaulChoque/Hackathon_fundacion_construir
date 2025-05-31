"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
from google.cloud import texttospeech

# Establece la ruta al archivo de credenciales JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "i:/Proyectos/2025/hackathon defensoria pueblo/Hackathon_fundacion_construir/environment/texttospeech-461505-a452c1a3ae9e.json"
)



# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="¡Cochabamba, joya del valle! Tu cielo celeste acaricia cerros vestidos de verdes intensos en verano y dorados en invierno. El imponente Cristo de la Concordia abraza a esta ciudad de eterna primavera, donde el sol brilla con fuerza pero el aire es suave.  Sus calles bulliciosas huelen a salteñas recién horneadas y a mercado vibrante. La Laguna Alalay refleja tu serenidad, mientras las plazas coloniales susurran historias. Los rostros amables de su gente, tu mayor tesoro, hacen sentir a todos en casa.  Eres tierra generosa: de choclos dulces, de huertas fértiles, de risas francas y de un orgullo cochala que se siente en el aire. ¡Cochabamba, no solo eres bella, eres *sentimiento*! Un rincón de Bolivia que cautiva el alma en cada esquina. ¡Así es mi Llajta!")

# Build the voice request, select the language code ("es-ES") and the ssml
# voice gender ("female")
voice = texttospeech.VoiceSelectionParams(
    language_code="es-ES", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# ...código existente...

# The response's audio_content is binary.
# ...código existente...

# ...código existente...

# Ruta absoluta basada en la ubicación de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "../assets/audio/output/output.mp3")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "wb") as out:
    out.write(response.audio_content)
    print(f'Audio content written to file "{output_path}"')
# ...código existente...
# ...código existente...
# ...código existente...