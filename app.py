from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import json

app = Flask(__name__)
CORS(app)

# 🦅 RDX MASTER CONFIG
API_KEY = "AhmadRDX"

# 🍪 YOUR PRIVATE COOKIES INTEGRATED
RDX_COOKIES = [
    {"domain": ".instagram.com", "name": "datr", "value": "uSKAadyUYea0BpWZdtL4f9Kx"},
    {"domain": ".instagram.com", "name": "ig_did", "value": "731C0210-4E78-4A23-B215-71BA1C49BF92"},
    {"domain": ".instagram.com", "name": "mid", "value": "aYAiuQABAAFPO0HzHIr7I-YaiHNX"},
    {"domain": ".instagram.com", "name": "dpr", "value": "3.2983407974243164"},
    {"domain": ".instagram.com", "name": "ig_nrcb", "value": "1"},
    {"domain": ".instagram.com", "name": "wd", "value": "891x1753"},
    {"domain": ".instagram.com", "name": "csrftoken", "value": "SSkJo4clXfiOkFw5cbGLRZEObyxtIlKr"},
    {"domain": ".instagram.com", "name": "ds_user_id", "value": "47135488335"},
    {"domain": ".instagram.com", "name": "sessionid", "value": "47135488335%3ATpyrqNesRoN0Ke%3A17%3AAYit43__sOPvk_-JhGB0l5IDndd4yXlPvFb6KWiE0w"},
    {"domain": ".instagram.com", "name": "rur", "value": "RVA\05447135488335\0541803491081:01feebd66480a9239da4bc584c5173e8d2a0bad3e675eba5c7d3a063e4e15ea297ccf260"}
]

def create_cookie_file():
    """Converts JSON cookies to Netscape format for yt-dlp"""
    cookie_file = 'rdx_cookies.txt'
    with open(cookie_file, 'w') as f:
        f.write('# Netscape HTTP Cookie File\n')
        for c in RDX_COOKIES:
            # Netscape format: domain, flag, path, secure, expiration, name, value
            domain = c.get('domain')
            name = c.get('name')
            value = c.get('value')
            f.write(f"{domain}\tTRUE\t/\tTRUE\t0\t{name}\t{value}\n")
    return cookie_file

def get_insta_video(url):
    cookie_path = create_cookie_file()
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_path,
        'format': 'best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": True,
                "title": info.get('title', 'RDX Instagram Video'),
                "url": info.get('url'),
                "thumbnail": info.get('thumbnail')
            }
    except Exception as e:
        return {"status": False, "error": str(e)}

@app.route('/rdx/ig', methods=['GET'])
def ig_api():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Invalid API Key!"}), 403
    
    if not url:
        return jsonify({"status": False, "msg": "URL missing!"}), 400

    result = get_insta_video(url)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
