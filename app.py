from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    options = {
        "quiet": True,
        "cookiefile": "cookies.txt",  # Make sure this file is uploaded with the build
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
        "format": "best[ext=mp4]/best",
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

            # Check formats for a downloadable URL
            formats = info.get("formats", [])
            mp4_format = next((f for f in formats if f.get("ext") == "mp4" and f.get("url")), None)

            if mp4_format:
                return jsonify({"download_url": mp4_format["url"]})
            else:
                return jsonify({"error": "MP4 format not found in available formats."}), 500

    except Exception as e:
        return jsonify({"error": "yt-dlp failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
