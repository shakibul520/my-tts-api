from flask import Flask, request, send_file
from flask_cors import CORS
import edge_tts
import asyncio
import os

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return "TTS Server is Running!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', 'হ্যালো')
    voice = data.get('voice', 'bn-BD-NabanitaNeural') 
    
    output_filename = "output.mp3"

    async def create_audio():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_filename)

    asyncio.run(create_audio())

    return send_file(output_filename, mimetype="audio/mpeg", as_attachment=True, download_name="voice.mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
