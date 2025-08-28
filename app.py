from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import tempfile
import re

app = Flask(__name__)
CORS(app)

def extract_stats(text):
    """ Extracts common stats like followers, following, posts, connections """
    def extract(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).replace(',', '')
            try:
                if "k" in value.lower():
                    return int(float(value.lower().replace('k', '')) * 1000)
                elif "m" in value.lower():
                    return int(float(value.lower().replace('m', '')) * 1000000)
                return int(value)
            except:
                return None
        return None

    return {
        "followers": extract(r'([\d.,]+)\s*followers?'),
        "following": extract(r'([\d.,]+)\s*following'),
        "posts": extract(r'([\d.,]+)\s*posts?'),
        "connections": extract(r'([\d.,]+)\s*connections'),
        "friends": extract(r'([\d.,]+)\s*friends')
    }

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🟢 Backend is live. Upload to /upload"})

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    uploaded_file = request.files['image']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        uploaded_file.save(temp.name)
        image = Image.open(temp.name)

    extracted_text = pytesseract.image_to_string(image)
    lower = extracted_text.lower()

    # Platform detection
    if 'followers' in lower and 'following' in lower:
        platform = "instagram"
    elif 'connections' in lower or 'linkedin' in lower:
        platform = "linkedin"
    elif 'friends' in lower or 'likes' in lower:
        platform = "facebook"
    else:
        platform = "unknown"

    # Stat extraction
    stats = extract_stats(lower)

    return jsonify({
        "platform": platform,
        "raw_text": extracted_text,
        "extracted": stats,
        "message": f"{platform.title()} profile analyzed ✅"
    })
