from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import datetime

app = Flask(__name__)    # ✅ has to come first
CORS(app)

@app.route("/audit", methods=["GET"])
def audit():
    try:
        loader = instaloader.Instaloader()

        username = request.args.get("username", "cafedebangkok.kochi")
        profile = instaloader.Profile.from_username(loader.context, username)

        return jsonify({
            "username": profile.username,
            "followers": profile.followers
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "error": "Backend failed",
            "details": str(e)
        }), 500

# Needed for local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)    
