from flask import Flask, request
import yt_dlp
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json

app = Flask(__name__)

SetLogLevel(-1)
model = Model("model")

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': 'audio.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,  # 50 MB
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'audio.mp3'

def transcribe_audio(audio_file):
    # Convert mp3 to wav for Vosk
    wav_file = 'temp.wav'
    os.system(f"ffmpeg -i {audio_file} -acodec pcm_s16le -ar 16000 {wav_file}")
    
    wf = wave.open(wav_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    transcription = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription.append(result['text'])

    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result['text'])

    os.remove(wav_file)  # Clean up temporary wav file
    return ' '.join(transcription)

@app.route('/transcribe', methods=['GET'])
def transcribe():
    url = request.args.get('url')
    if not url:
        return "Please provide a YouTube URL", 400

    try:
        audio_file = download_audio(url)
        transcript = transcribe_audio(audio_file)
        os.remove(audio_file)
        return transcript, 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
