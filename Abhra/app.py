from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL
import instaloader
import re
import os

app = Flask(__name__)

# Function to download YouTube video
def download_video(url, resolution='best'):
    options = {
        'format': resolution,
        'outtmpl': os.path.join(os.getcwd(), 'downloads', '%(title)s.%(ext)s'),
        'ffmpeg_location': os.path.join(os.getcwd(), 'ffmpeg'),  # Adjust for deployment
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])

# Function to download YouTube audio
def download_audio(url):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(os.getcwd(), 'downloads', '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': os.path.join(os.getcwd(), 'ffmpeg'),  # Adjust for deployment
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])

# Extract shortcode from Instagram URL
def extract_shortcode(url):
    patterns = [
        r"instagram\.com/p/([A-Za-z0-9_-]+)/?",
        r"instagram\.com/reel/([A-Za-z0-9_-]+)/?",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Function to download Instagram reel
def download_instagram_reel(url):
    loader = instaloader.Instaloader()
    shortcode = extract_shortcode(url)
    if not shortcode:
        return "Invalid URL"
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    download_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)
    loader.download_post(post, target=download_dir)
    return "Reel downloaded successfully."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    platform = data.get('platform')

    try:
        os.makedirs("downloads", exist_ok=True)
        if platform == "youtube_video":
            download_video(url)
            return jsonify(success=True, message="Video downloaded successfully!")
        elif platform == "youtube_audio":
            download_audio(url)
            return jsonify(success=True, message="Audio downloaded successfully!")
        elif platform == "instagram_reel":
            msg = download_instagram_reel(url)
            return jsonify(success=True, message=msg)
        else:
            return jsonify(success=False, error="Invalid platform selected.")
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)