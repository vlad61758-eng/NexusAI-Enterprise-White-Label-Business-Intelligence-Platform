# Telegram Lead Generation & Keyword Monitoring UserBot

This is a production-ready Telegram UserBot script built with Python and Telethon. It is designed for B2B lead generation and keyword monitoring. The bot listens to specific groups or chats, scans incoming messages for predefined keywords, and alerts you instantly while saving the lead data to an Excel file.

## Features

- **24/7 Monitoring**: Listens to targeted Telegram groups/chats.
- **Keyword Matching**: Scans messages for case-insensitive keywords.
- **Instant Alerts**: Forwards formatted alerts to your "Saved Messages" or a private admin channel.
- **Data Export**: Automatically logs leads (Username, Name, Date, Keyword, Message snippet, Link) to an Excel file (`leads.xlsx`).
- **Resilient**: Includes error handling for flood waits and connection drops.

## Prerequisites

- **Python 3.8+** installed on your system.
- A Telegram account to act as the UserBot.
- Telegram API credentials (`API_ID` and `API_HASH`).

## Step 1: Get Your API Credentials

1. Log in to your Telegram account at [https://my.telegram.org](https://my.telegram.org).
2. Click on **API development tools**.
3. Fill in the form to create a new application (the details don't matter much).
4. Note down your **`App api_id`** and **`App api_hash`**. You will need these in the next step.

## Step 2: Setup

1. **Clone or download** this repository to your machine.
2. **Open a terminal** or command prompt in the folder containing the script.
3. **Install the required libraries** by running:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configuration

1. Rename the `.env.example` file to `.env` (make sure it doesn't have a `.txt` extension!).
2. Open the `.env` file in a text editor (like Notepad or VS Code) and fill in your details:

   ```ini
   # Your Telegram API ID and Hash (from Step 1)
   API_ID=1234567
   API_HASH=your_api_hash_here

   # Comma-separated list of chats to monitor (e.g., @group1, @group2 or group ID like -100123456789)
   TARGET_CHATS=@example_group1,@example_group2

   # Comma-separated list of keywords to look for
   KEYWORDS=lead,marketing,b2b,buy,need

   # Where to send the alerts. Use 'me' to send to your Saved Messages, or a specific channel/username
   ADMIN_CHANNEL=me
   ```

## Step 4: Run the Bot

1. In your terminal, run the script:
   ```bash
   python bot.py
   ```
2. **First Time Login**: The first time you run the script, Telegram will ask you to log in.
   - Enter your phone number with the country code (e.g., `+1234567890`).
   - Enter the login code sent to your Telegram app.
   - If you have Two-Step Verification (2FA) enabled, it will ask for your password.
3. Once logged in, a `userbot_session.session` file will be created. Keep this file safe! The bot will now run continuously and monitor the chats.

## Checking Your Leads

- **Alerts**: You will receive a message in your specified `ADMIN_CHANNEL` (e.g., your Saved Messages) whenever a keyword is triggered.
- **Excel File**: Open the `leads.xlsx` file generated in the folder to see a structured list of all captured leads.

## Stopping the Bot
To stop the script, press `Ctrl + C` in the terminal window.
