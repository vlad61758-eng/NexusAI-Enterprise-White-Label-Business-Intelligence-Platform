import yt_dlp
import sys
import os

def download_video(url, output_folder="downloads"):
    """Downloads a video from various social media platforms."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"🔄 Preparing to download from: {url}")
    print("Please wait, fetching highest quality...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Download complete! Check the '{output_folder}' folder.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    print("="*50)
    print("🎬 Universal Social Media Video Downloader 🎬")
    print("="*50)

    # Check if URL was passed as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nPaste the video URL here (TikTok, Instagram, YouTube, etc): ")

    if url.strip():
        download_video(url.strip())
    else:
        print("Error: No URL provided.")