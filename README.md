# Telegram B2B Lead Generation UserBot

A production-ready Telegram UserBot script designed for B2B lead generation and keyword monitoring. The script runs on your Telegram account to listen to specific groups/chats for keywords, and instantly sends you an alert and saves the lead into an Excel file.

## Features

- **Keyword Monitoring**: Monitors a list of target chats for specific keywords (case-insensitive).
- **Instant Alerts**: Forwards matched messages to your "Saved Messages" or a specified admin channel with formatted details (Sender, chat, snippet, and link).
- **Data Export**: Automatically saves all leads to an Excel file (`leads.xlsx`) with their username, name, date, matched keyword, and a message snippet.
- **Robustness**: Includes exception handling (e.g., FloodWaitError) to ensure 24/7 uptime.

## Setup Instructions

### 1. Get Telegram API Credentials
1. Go to [https://my.telegram.org/apps](https://my.telegram.org/apps) and log in with your Telegram account.
2. Under "API development tools", fill out the form to create a new application (you can use random names for App Title and Short Name).
3. Once created, copy the **`App api_id`** and **`App api_hash`**.

### 2. Configure the Script
1. Rename the `.env.example` file to `.env`.
2. Open `.env` in a text editor.
3. Replace the placeholder values with your own:
   - **`API_ID`**: Your App api_id from step 1.
   - **`API_HASH`**: Your App api_hash from step 1.
   - **`TARGET_CHATS`**: A comma-separated list of chats to monitor (e.g., `@python_chat, https://t.me/tech_group`). Leave empty or remove to monitor *all* your chats.
   - **`KEYWORDS`**: A comma-separated list of keywords to look for (e.g., `developer, python, looking for job`).
   - **`ADMIN_CHAT`**: The chat where alerts will be sent. Use `me` for your Saved Messages, or provide a specific chat ID/username.

### 3. Install Dependencies
You need Python 3 installed. Open your terminal or command prompt and run:
```bash
pip install -r requirements.txt
```

### 4. Run the UserBot (Lead Generator)
Run the script using:
```bash
python userbot.py
```
*Note: The first time you run the script, it will ask for your phone number and a login code sent to your Telegram app to authenticate your session.*

### 5. Setup and Run the Sales Bot (Optional)
If you want to resell this tool or act as a manager, you can run the accompanying Sales Bot:
1. Create a new bot using `@BotFather` on Telegram and get the Token.
2. In your `.env` file, add `BOT_TOKEN=your_token` and `OWNER_USERNAME=@your_username`.
3. Run the sales bot using:
```bash
python sales_bot.py
```
This bot provides a menu for clients to learn about the system and purchase it from you directly!

### 6. Fully Automated Passive Income System (Optional)
Instead of manually selling the bot, you can launch the fully automated Crypto E-commerce Site and Reddit Bot.
1. Run `python app.py` to start the Flask Web Store. Clients can visit this site, see your USDT address, enter their Transaction ID, and instantly download the `AI_LeadGen_Pro.zip` file.
2. Configure your Reddit API credentials in `.env` (Get them from `https://www.reddit.com/prefs/apps`).
3. Run `python reddit_bot.py`. This bot will scan business subreddits (e.g. r/Entrepreneur) and use Gemini AI to automatically reply to people looking for leads, directing them to your website.

**To run 24/7 on a VPS ($5/month):**
Upload the files to a Linux VPS (like DigitalOcean or Hetzner). Use `tmux` or create systemd service files (`/etc/systemd/system/leadgen-store.service`) to keep `app.py` and `reddit_bot.py` running forever in the background!

## Files
- `userbot.py`: The main UserBot script (Lead Generator).
- `sales_bot.py`: The Aiogram Sales Manager Bot.
- `app.py` & `templates/`: Automated Crypto Checkout Web Server.
- `reddit_bot.py`: Reddit marketing bot using AI.
- `AI_LeadGen_Pro.zip`: The packaged product for clients to download.
- `.env`: Your private configuration file.
- `requirements.txt`: Python dependencies.
- `leads.xlsx`: Automatically generated file containing saved leads.
