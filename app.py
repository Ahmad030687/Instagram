from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

def get_instagram_video(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return {
            "status": True,
            "title": info.get("title"),
            "video": info.get("url"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration")
        }

@app.route('/instagram', methods=['GET'])
def instagram():
    url = request.args.get('url')

    if not url:
        return jsonify({"status": False, "msg": "URL missing"}), 400

    try:
        data = get_instagram_video(url)
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/')
def home():
    return jsonify({"message": "Instagram Downloader API Running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
