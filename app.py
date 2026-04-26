import asyncio
import edge_tts
import os
import uuid
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "TTS Server is Running!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'bn-BD-NabanitaNeural')

        if not text:
            return {"error": "No text provided"}, 400

        # অডিও ফাইলের নাম তৈরি
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        async def amain() -> None:
            communicate = edge_tts.Communicate(text, voice)
            # এখানে 'save' হবে (আগের 'saver' ভুল ছিল)
            await communicate.save(filename)

        asyncio.run(amain())

        return send_file(filename, mimetype="audio/mpeg", as_attachment=True, download_name="voice.mp3")
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
