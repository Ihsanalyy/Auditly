from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # 🔐 Load .env credentials

app = Flask(__name__)
CORS(app)

@app.route("/audit", methods=["GET"])
def audit():
    try:
        loader = instaloader.Instaloader()
        
        # 🔐 Login using .env credentials
        ig_username = os.getenv("IG_USERNAME")
        ig_password = os.getenv("IG_PASSWORD")
        loader.login(ig_username, ig_password)

        username = request.args.get("username", "concept.com_store")
        profile = instaloader.Profile.from_username(loader.context, username)

        return jsonify({
            "username": profile.username,
            "followers": profile.followers,
            "bio": profile.biography
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "error": "Backend failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
