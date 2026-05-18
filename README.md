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

### 4. Run the Bot
Run the script using:
```bash
python userbot.py
```
*Note: The first time you run the script, it will ask for your phone number and a login code sent to your Telegram app to authenticate your session.*

## Files
- `userbot.py`: The main script.
- `.env`: Your private configuration file.
- `requirements.txt`: Python dependencies.
- `leads.xlsx`: Automatically generated file containing saved leads.
- `userbot.log`: Log file for monitoring the script's activity and errors.
