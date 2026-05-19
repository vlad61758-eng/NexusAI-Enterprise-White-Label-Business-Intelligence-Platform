# AI Content Auto-Blogger 🤖✍️

Welcome to your automated content generation machine! This script uses Google's powerful Gemini AI to instantly write high-quality, SEO-optimized blog posts based on a list of keywords.

## What it does:
1. Reads a list of keywords from a text file (`keywords.txt`).
2. Connects to the Gemini AI API.
3. Automatically writes a full, SEO-optimized 500-700 word article for each keyword.
4. Saves each article neatly into a `generated_blogs` folder as Markdown files, ready to be copied into WordPress, Medium, or your website.

## Setup Instructions 🛠️

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*Important for Windows users: When installing, make sure to check the box that says "Add Python to PATH".*

### 2. Get a Free Gemini API Key
1. Go to Google AI Studio: https://aistudio.google.com/
2. Sign in with your Google account.
3. Click "Get API Key" on the left menu and create a new key.

### 3. Install Dependencies
Open your terminal (or Command Prompt) inside this folder and run:
```bash
pip install -r requirements.txt
```

### 4. Add Your API Key
1. In this folder, create a new file named exactly `.env` (don't forget the dot at the beginning).
2. Open the `.env` file in Notepad or any text editor and add this line, pasting the key you got from Google:
```text
GEMINI_API_KEY=your_long_api_key_goes_here
```

## How to Run 🚀

1. Open the file named `keywords.txt` (the script will create a sample one if it doesn't exist).
2. Add the topics you want to write about, **one topic per line**.
3. Open your terminal in this folder and run:
```bash
python ai_blogger.py
```
4. Sit back and watch the AI write your articles! You will find the finished texts in the `generated_blogs` folder.