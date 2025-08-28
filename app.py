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
        profile = instaloader.Profile.from_username(loader.context, username)

        recent_posts = []
        total_likes = 0
        total_comments = 0

        posts_to_check = 6  # Number of recent posts to analyze

        for post in profile.get_posts():
            if posts_to_check == 0:
                break

            caption = post.caption or ""
            hashtags = post.caption_hashtags or []
            likes = post.likes
            comments = post.comments
            date = post.date.strftime("%d/%m/%Y")

            # Build post dictionary
            recent_posts.append({
                "date": date,
                "caption": caption[:100],
                "likes": likes,
                "comments": comments,
                "hashtags": hashtags
            })

            total_likes += likes
            total_comments += comments
            posts_to_check -= 1

        # Engagement trend → average likes/comments per post
        avg_likes = total_likes / len(recent_posts) if recent_posts else 0
        avg_comments = total_comments / len(recent_posts) if recent_posts else 0

        # Simulated follower growth - ideally, track daily and save it somewhere
        today = datetime.date.today()
        followers_growth = [
            {"date": (today - datetime.timedelta(days=i)).strftime("%d/%m"), "followers": profile.followers - i*10}
            for i in reversed(range(6))
        ]

        data = {
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
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
