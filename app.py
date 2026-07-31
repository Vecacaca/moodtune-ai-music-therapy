from flask import Flask, request, jsonify
import yt_dlp  # 使用 yt-dlp 而不是 youtube_dl

app = Flask(__name__)

def get_audio_url(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_url = info_dict.get('url', None)
            if audio_url:
                return audio_url
            else:
                return None
    except Exception as e:
        return None

@app.route('/get_audio', methods=['POST'])
def get_audio():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    
    audio_url = get_audio_url(video_url)
    if audio_url:
        return jsonify({"audio_url": audio_url}), 200
    else:
        return jsonify({"error": "Failed to extract audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

