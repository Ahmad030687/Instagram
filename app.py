from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import json

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"

def get_insta_direct(url):
    # Link ko clean karna (Reel link se direct query banana)
    if "/reels/" in url:
        url = url.replace("/reels/", "/reel/")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-IG-App-ID": "936619743392459", # Instagram Public App ID
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # 🧪 Step 1: Get Post ID from URL
        post_id = re.search(r'/(?:reels|reel|p)/([a-zA-Z0-9_-]+)', url).group(1)
        
        # 🧪 Step 2: Hit Instagram's internal GraphQL/AJAX endpoint
        # Ye wahi endpoint hai jo Instagram web use karta hai video load karne ke liye
        api_url = f"https://www.instagram.com/api/v1/p/{post_id}/?__a=1&__d=dis"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Video link nikalne ka logic
            video_url = data['items'][0]['video_versions'][0]['url']
            title = data['items'][0].get('caption', {}).get('text', 'RDX Reel')
            
            return {
                "status": True,
                "engine": "RDX Lite Custom",
                "title": title,
                "url": video_url
            }
        else:
            return {"status": False, "error": f"Insta block: {response.status_code}"}

    except Exception as e:
        return {"status": False, "error": str(e)}

@app.route('/rdx/ig', methods=['GET'])
def ig_api():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Wrong Key"}), 403
    
    if not url:
        return jsonify({"status": False, "msg": "URL missing"}), 400

    result = get_insta_direct(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
