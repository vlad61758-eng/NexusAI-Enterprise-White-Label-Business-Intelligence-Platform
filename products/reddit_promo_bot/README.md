# Reddit Marketing Bot 🚀

This is a Python bot that uses the official Reddit API and Google's Gemini AI to find potential customers and promote your products automatically without looking like spam.

## How it works:
1. It scans specific business subreddits (like r/Entrepreneur, r/marketing) for keywords like "SEO", "cold email", etc.
2. When it finds someone discussing these topics, it sends their post to Gemini AI.
3. The AI writes a highly contextual, helpful, and "human-like" comment addressing their problem.
4. At the end of the helpful advice, it organically recommends your `Sell.app` store.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Reddit API Keys
1. Go to https://www.reddit.com/prefs/apps
2. Scroll to the bottom and click "Create another app..." or "Create App".
3. Name it "PromoBot", select **"script"** as the type.
4. Set the redirect URI to `http://localhost:8080`.
5. Click "Create app".
6. You will now see your **Client ID** (under the name "PromoBot") and **Client Secret**.

### 3. Configure the .env File
Create a `.env` file in this folder and add the following:
```text
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Safety First (Read This)
By default, the script is in **"Test Mode"**. It will find posts and generate comments, but it will only *print* them to your terminal, it will NOT post them to Reddit. This is to protect your account.

When you are ready to actually post:
1. Open `reddit_bot.py`.
2. Find line 75: `# submission.reply(reply_text)`
3. Remove the `#` at the beginning of the line.

### 5. Run the Bot
```bash
python reddit_bot.py
```
*Tip: Only run this 1-2 times a day. If you spam Reddit too fast, your account will be shadowbanned.*