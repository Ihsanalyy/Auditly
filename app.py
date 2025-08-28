from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/audit", methods=["GET"])
def audit():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        loader = instaloader.Instaloader()

        # 🔐 Use read-only login with your dummy account
        ig_username = os.getenv("IG_USERNAME")
        ig_password = os.getenv("IG_PASSWORD")
        loader.login(ig_username, ig_password)

        profile = instaloader.Profile.from_username(loader.context, username)

        # Basic info
        today = datetime.date.today()
        followers_growth = [
            {
                "date": (today - datetime.timedelta(days=i)).strftime("%d/%m"),
                "followers": profile.followers - i * 12  # Simulated
            }
            for i in reversed(range(7))
        ]

        # Recent posts
        recent_posts = []
        total_likes = 0
        total_comments = 0
        for post in profile.get_posts():
            if len(recent_posts) >= 6:
                break
            recent_posts.append({
                "date": post.date.strftime("%d/%m/%Y"),
                "caption": post.caption[:150] if post.caption else "",
                "likes": post.likes,
                "comments": post.comments,
                "hashtags": post.caption_hashtags or []
            })
            total_likes += post.likes
            total_comments += post.comments

        avg_likes = int(total_likes / len(recent_posts)) if recent_posts else 0
        avg_comments = int(total_comments / len(recent_posts)) if recent_posts else 0

        return jsonify({
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "followees": profile.followees,
            "is_private": profile.is_private,
            "posts": profile.mediacount,
            "followers_growth": followers_growth,
            "engagement_trend": {
                "average_likes": avg_likes,
                "average_comments": avg_comments
            },
            "recent_posts": recent_posts
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "error": "Unable to fetch profile",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
