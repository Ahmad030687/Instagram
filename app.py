from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import json

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"

def get_snapchat_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        # 🧪 Step 1: Page load karna
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"status": False, "error": f"Snapchat blocked access: {response.status_code}"}

        html_content = response.text

        # 🧪 Step 2: JSON data nikalna (Snapchat video details yahan chupa ke rakhta hai)
        # Hum '__NEXT_DATA__' script tag ko target kar rahe hain
        script_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_content)
        
        if script_data:
            json_data = json.loads(script_data.group(1))
            
            # Spotlight video ka direct link nikalne ka logic
            # Snapchat ke naye structure ke mutabiq link yahan hota hai:
            try:
                # Alag alag paths check karte hain taake error na aaye
                props = json_data.get('props', {}).get('pageProps', {})
                spotlight_data = props.get('spotlightVideo', {}) or props.get('story', {})
                
                video_url = spotlight_data.get('contentUrl') or spotlight_data.get('streamingUrl')
                
                if not video_url:
                    # Backup Regex agar JSON fail ho jaye
                    video_url = re.search(r'"contentUrl":"(.*?)"', html_content).group(1)

                return {
                    "status": True,
                    "engine": "RDX Snap Custom",
                    "title": props.get('title', 'Snapchat Spotlight'),
                    "url": video_url.replace('\\u002F', '/'), # URL clean karna
                    "thumbnail": props.get('thumbnailUrl')
                }
            except:
                return {"status": False, "error": "Video link extraction failed within JSON."}
        else:
            return {"status": False, "error": "Metadata not found. Shayad link galat hai?"}

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
