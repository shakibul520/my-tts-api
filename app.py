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
    return "KinetiVox AI Engine (Pro v4.1) is Live!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'bn-BD-NabanitaNeural')

        # ডাটাগুলো নাম্বার হিসেবে রিসিভ করা হচ্ছে
        rate_val = int(data.get('rate', 0))
        pitch_val = int(data.get('pitch', 0))
        volume_val = int(data.get('volume', 0))

        if not text:
            return jsonify({"error": "No text provided"}), 400

        voice_params = {}
        
        # 🎯 স্পিড এবং ভলিউম যাবে % এ
        if rate_val != 0:
            voice_params['rate'] = f"+{rate_val}%" if rate_val > 0 else f"{rate_val}%"
        if volume_val != 0:
            voice_params['volume'] = f"+{volume_val}%" if volume_val > 0 else f"{volume_val}%"
            
        # 🎯 ম্যাজিক ফিক্স: পিচ অবশ্যই Hz এ যেতে হবে!
        if pitch_val != 0:
            voice_params['pitch'] = f"+{pitch_val}Hz" if pitch_val > 0 else f"{pitch_val}Hz"

        async def get_audio_data():
            communicate = edge_tts.Communicate(text, voice, **voice_params)
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]
            return audio_bytes

        audio_content = asyncio.run(get_audio_data())

        return send_file(
            io.BytesIO(audio_content),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name=f"kinetivox_master.mp3"
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
