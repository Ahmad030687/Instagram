from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"

# 🍪 Yahan aap 1 ya zyada accounts ki cookies daal sakte hain
# Jitni zyada cookies hongi, blocking ke chances utne kam honge
COOKIES_LIST = [
    "sessionid=47135488335%3ATpyrqNesRoN0Ke%3A17%3AAYit43__sOPvk_-JhGB0l5IDndd4yXlPvFb6KWiE0w; ds_user_id=47135488335; csrftoken=SSkJo4clXfiOkFw5cbGLRZEObyxtIlKr;"
]

def get_insta_custom(url):
    try:
        # Link se ID nikalna
        post_id = re.search(r'/(?:reels|reel|p)/([a-zA-Z0-9_-]+)', url).group(1)
        api_url = f"https://www.instagram.com/api/v1/p/{post_id}/?__a=1&__d=dis"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "X-IG-App-ID": "936619743392459",
            "Cookie": COOKIES_LIST[0] # Pehli cookie use kar raha hai
        }

        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Video URL nikalne ka sahi rasta
            items = data.get('items', [])
            if not items:
                return {"status": False, "error": "Post data not found (Private?)"}
            
            video_url = items[0]['video_versions'][0]['url']
            return {
                "status": True,
                "engine": "RDX Custom Cookie-Engine",
                "url": video_url
            }
        else:
            return {"status": False, "error": f"Instagram Error: {response.status_code}"}

    except Exception as e:
        return {"status": False, "error": str(e)}

@app.route('/rdx/ig', methods=['GET'])
def ig_api():
    url = request.args.get('url')
    if request.args.get('apikey') != API_KEY:
        return jsonify({"status": False, "msg": "Wrong Key"}), 403
    
    if not url:
        return jsonify({"status": False, "msg": "URL missing"}), 400

    result = get_insta_custom(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
