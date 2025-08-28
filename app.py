from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=["POST"])
def upload_image():
    try:
        file = request.files['image']
        filename = file.filename

        # Temporarily save the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
            file.save(temp.name)
            image = Image.open(temp.name)

        # OCR
        text = pytesseract.image_to_string(image)

        # Basic logic to detect platform based on keywords
        lower = text.lower()

        if 'followers' in lower and 'following' in lower:
            platform = "instagram"
        elif 'connections' in lower or 'linkedin' in lower:
            platform = "linkedin"
        elif 'friends' in lower or 'likes' in lower:
            platform = "facebook"
        else:
            platform = "unknown"

        response = {
            "platform": platform,
            "raw_text": text  # Optional: return the plain extracted text for debugging
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
