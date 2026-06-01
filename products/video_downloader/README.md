# Universal Social Video Downloader 🎬📥

A lightning-fast Python script to download videos in the highest possible quality from over 100+ platforms, including TikTok (often without watermarks), Instagram Reels, YouTube Shorts, Twitter/X, and more.

## Perfect for:
- SMM (Social Media Managers) building content banks.
- Video editors looking for high-quality source material.
- Content creators archiving their work.

## Setup Instructions

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*Important for Windows users: When installing, make sure to check the box that says "Add Python to PATH".*

### 2. Install Dependencies
Open your terminal (or Command Prompt) inside this folder and run:
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (Optional but Recommended)
For downloading very high quality videos (like 4K YouTube) where audio and video are separate, the script needs `ffmpeg` installed on your system.
- **Mac:** `brew install ffmpeg`
- **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin` folder to your System PATH.

## How to Run 🚀

Just open your terminal in this folder and run:
```bash
python downloader.py
```
The script will ask you to paste a link. Paste it, hit Enter, and the video will be saved in a newly created `downloads` folder!

You can also run it directly with the link:
```bash
python downloader.py "https://www.tiktok.com/@user/video/123456789"
```