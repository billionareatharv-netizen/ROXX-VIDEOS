from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/api/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": "error", "msg": "URL missing"}), 400

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "force_generic_extractor": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get("formats", []):
            formats.append({
                "resolution": f.get("format_note") or f.get("resolution"),
                "ext": f.get("ext"),
                "vcodec": f.get("vcodec"),
                "acodec": f.get("acodec"),
                "size_mb": f.get("filesize") / (1024*1024) if f.get("filesize") else None,
                "url": f.get("url")
            })

        return jsonify({
            "status": "ok",
            "info": {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration_str": info.get("duration_string"),
                "uploader": info.get("uploader"),
                "extractor": info.get("extractor"),
            },
            "formats": formats
        })

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

@app.route("/")
def home():
    return "Railway API Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
