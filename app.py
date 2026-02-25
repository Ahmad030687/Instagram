from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import json

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"

def get_snapchat_video(url):
    # Session use karne se Snapchat ko dhoka dena asan hota hai
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    try:
        # 🧪 Step 1: Request bhejna
        response = session.get(url, headers=headers, timeout=15)
        
        # Agar Snapchat 404 de raha hai, toh iska matlab IP block hai
        if response.status_code == 404:
            return {"status": False, "error": "Snapchat blocked this IP (404). Render ka server block ho gaya hai."}
        
        if response.status_code != 200:
            return {"status": False, "error": f"Snapchat Error: {response.status_code}"}

        html = response.text
        
        # 🧪 Step 2: Spotlight Video nikalne ka naya tareeka
        # Kabhi kabhi JSON script tag mein data hota hai
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        
        if match:
            data = json.loads(match.group(1))
            # Path: props -> pageProps -> spotlightVideo -> contentUrl
            try:
                # Alag alag patterns check karna
                page_props = data.get('props', {}).get('pageProps', {})
                video_data = page_props.get('spotlightVideo') or page_props.get('story')
                
                video_url = video_data.get('contentUrl') or video_data.get('streamingUrl')
                
                if video_url:
                    return {
                        "status": True,
                        "engine": "RDX Snap-Stealth",
                        "url": video_url.replace('\\u002F', '/')
                    }
            except:
                pass

        # 🧪 Step 3: Agar JSON fail ho jaye toh Meta Tags se nikalna
        meta_match = re.search(r'<meta property="og:video" content="(.*?)"', html)
        if meta_match:
            return {
                "status": True,
                "engine": "RDX Meta-Extractor",
                "url": meta_match.group(1)
            }

        return {"status": False, "error": "Video link nahi mila. Shayad link expired hai."}

    except Exception as e:
        return {"status": False, "error": str(e)}

@app.route('/rdx/snap', methods=['GET'])
def snap_api():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Wrong API Key!"}), 403
    
    if not url:
        return jsonify({"status": False, "msg": "Snapchat URL missing!"}), 400

    result = get_snapchat_video(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
