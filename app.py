import asyncio
import edge_tts
import io
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

        # অডিও ডাটা মেমোরিতে জমা করার জন্য
        async def get_audio():
            communicate = edge_tts.Communicate(text, voice)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data

        audio_bytes = asyncio.run(get_audio())
        
        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="voice.mp3"
        )

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
