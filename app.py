from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        result = subprocess.run(
            ["yt-dlp", "-j", url],
            capture_output=True,
            text=True,
            check=True
        )
        info = json.loads(result.stdout)
        if not info.get("url"):
            return jsonify({"error": "Could not extract video URL"}), 500

        return jsonify({
            "title": info.get("title"),
            "download_url": info.get("url"),
            "ext": info.get("ext"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration")
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "yt-dlp failed",
            "details": e.stderr.strip()
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Unexpected server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
