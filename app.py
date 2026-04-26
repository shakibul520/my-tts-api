import asyncio
import edge_tts
import io
import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "KinetiVox AI Engine (Pro v4) is Live!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'bn-BD-NabanitaNeural')
        
        # Speed, Pitch এবং Volume রিসিভ করা
        rate_val = data.get('rate', 0)
        pitch_val = data.get('pitch', 0)
        volume_val = data.get('volume', 0)

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Edge-TTS এর ফরমেট সেট করা
        rate_str = f"+{rate_val}%" if int(rate_val) >= 0 else f"{rate_val}%"
        pitch_str = f"+{pitch_val}%" if int(pitch_val) >= 0 else f"{pitch_val}%"
        volume_str = f"+{volume_val}%" if int(volume_val) >= 0 else f"{volume_val}%"

        async def get_audio_data():
            # ভলিউম প্যারামিটার যোগ করা হলো
            communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str, volume=volume_str)
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]
            return audio_bytes

        audio_content = asyncio.run(get_audio_data())

        if not audio_content:
            return jsonify({"error": "Failed to generate audio"}), 500

        return send_file(
            io.BytesIO(audio_content),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name=f"kinetivox_master.mp3"
        )

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
