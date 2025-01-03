import instaloader
import os
import speech_recognition as sr
from pydub import AudioSegment

# Initialiser Instaloader
L = instaloader.Instaloader()

# Télécharger un Reels à partir de son shortcode
shortcode = "DAEBElSCIWa"  # Remplace par le shortcode réel du Reels
post = instaloader.Post.from_shortcode(L.context, shortcode)

# Télécharger la vidéo du Reels
L.download_post(post, target='reels')

# Chemin vers la vidéo téléchargée
video_file = 'reels/2024-08-29_16-04-39_UTC.mp4'

# Chemin de sortie pour le fichier audio
audio_file = 'reels/filename_audio.mp3'

# Utiliser FFmpeg pour extraire l'audio (s'assurer que le fichier n'existe pas déjà)
if not os.path.exists(audio_file):
    os.system(f'ffmpeg -i "{video_file}" -q:a 0 -map a "{audio_file}"')

# Charger le fichier audio avec Pydub
audio = AudioSegment.from_mp3(audio_file)

# Exporter l'audio en WAV pour le traitement par SpeechRecognition
wav_file = 'reels/audio_output.wav'
audio.export(wav_file, format="wav")

# Initialiser le recognizer de SpeechRecognition
recognizer = sr.Recognizer()

# Charger l'audio dans recognizer
with sr.AudioFile(wav_file) as source:
    audio_data = recognizer.record(source)

# Transcrire l'audio en texte et enregistrer dans un fichier
output_file = 'reels/transcription.txt'

try:
    text = recognizer.recognize_google(audio_data, language="fr-FR")
    print("Texte transcrit :", text)

    # Enregistrer la transcription dans un fichier texte
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Transcription enregistrée dans {output_file}")

except sr.UnknownValueError:
    print("Google Speech Recognition n'a pas compris l'audio.")
except sr.RequestError as e:
    print(f"Erreur avec le service de Google Speech Recognition : {e}")
except Exception as e:
    print(f"Une autre erreur s'est produite : {e}")
