from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import tempfile
import os

# OPTIONAL: use .env for future login support
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔍 Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🟢 Backend is running. Upload screenshot to /upload"})

# 📤 Accepts image + analyzes using OCR
@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400

        uploaded_file = request.files['image']

        if uploaded_file.filename == "":
            return jsonify({"error": "Empty file name"}), 400

        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
            uploaded_file.save(temp.name)
            image = Image.open(temp.name)

        # 🤖 Run OCR using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        # 🧠 Very basic platform detection
        text_lower = extracted_text.lower()

        if "followers" in text_lower and "following" in text_lower:
            platform = "instagram"
        elif "connections" in text_lower or "linkedin" in text_lower:
            platform = "linkedin"
        elif "friends" in text_lower or "likes" in text_lower:
            platform = "facebook"
        else:
            platform = "unknown"

        # You can build smarter field extraction here (followers count, name, etc.)
        response = {
            "platform": platform,
            "raw_text": extracted_text,
            "message": f"{platform.title()} profile detected and analyzed ✅"
        }

        return jsonify(response)

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Failed to analyze image", "details": str(e)}), 500


# ✅ Run locally or via gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
