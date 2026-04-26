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
    return "KinetiVox AI Engine is Live!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        # এখান থেকেই আসল কাজ শুরু - যেকোনো ভয়েস আইডি এটি গ্রহণ করবে
        voice = data.get('voice', 'bn-BD-NabanitaNeural')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # মেমোরি ইফিশিয়েন্ট ওয়েতে অডিও জেনারেট করা
        async def get_audio_data():
            communicate = edge_tts.Communicate(text, voice)
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]
            return audio_bytes

        # রানটাইম হ্যান্ডলিং
        audio_content = asyncio.run(get_audio_data())

        if not audio_content:
            return jsonify({"error": "Failed to generate audio"}), 500

        return send_file(
            io.BytesIO(audio_content),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name=f"kinetivox_{voice}.mp3"
        )

    except Exception as e:
        # এখানে প্রিন্ট দিলে আপনি Render Logs-এ আসল এররটা দেখতে পাবেন
        print(f"Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render-এর জন্য পোর্ট ডাইনামিক রাখা জরুরি
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
