from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import datetime

app = Flask(__name__)
CORS(app)

@app.route("/audit", methods=["GET"])
def audit():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        loader = instaloader.Instaloader()

        # Optional: Add login (must be safe)
        # loader.login("your_instagram_username", "your_password")

        profile = instaloader.Profile.from_username(loader.context, username)

        today = datetime.date.today()
        followers_growth = [
            {
                "date": (today - datetime.timedelta(days=i)).strftime("%d/%m"),
                "followers": profile.followers - i * 12  # example growth
            }
            for i in reversed(range(6))
        ]

        recent_posts = []
        total_likes = 0
        total_comments = 0

        for post in profile.get_posts():
            if len(recent_posts) >= 6:
                break

            recent_posts.append({
                "date": post.date.strftime("%d/%m/%Y"),
                "caption": post.caption[:100] if post.caption else "",
                "likes": post.likes,
                "comments": post.comments,
                "hashtags": post.caption_hashtags
            })
            total_likes += post.likes
            total_comments += post.comments

        avg_likes = total_likes / len(recent_posts) if recent_posts else 0
        avg_comments = total_comments / len(recent_posts) if recent_posts else 0

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
                "average_likes": int(avg_likes),
                "average_comments": int(avg_comments)
            },
            "recent_posts": recent_posts
        })

    except Exception as e:
        print("⚠️ BACKEND ERROR:", str(e))  # Debug in Render logs
        return jsonify({
            "error": "Backend failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
