@app.route("/audit", methods=["GET"])
def audit():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        loader = instaloader.Instaloader()

        # profile fetch
        profile = instaloader.Profile.from_username(loader.context, username)

        # some dummy return to test JSON
        return jsonify({
            "username": profile.username,
            "followers": profile.followers
        })

    except Exception as e:
        print("🚫 ERROR:", str(e))  # Shows in Render Logs
        return jsonify({
            "error": "Backend crashed",
            "details": str(e)
        }), 500
