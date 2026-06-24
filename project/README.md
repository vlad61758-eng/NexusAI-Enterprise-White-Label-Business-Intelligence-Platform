# Telegram Auto-Task System

This repository contains a two-bot system built with Python, `telethon`, `aiogram`, and the Gemini AI API.

1. **The Task Hunter**: A userbot (`telethon`) that monitors specific Telegram channels for micro-tasks and logs them into a local SQLite database.
2. **The Task Executor**: A bot (`aiogram`) that polls the database, processes tasks using the Gemini AI model, and forwards the results directly to your Telegram account.

## Requirements

- Python 3.9+
- A [Telegram API ID and Hash](https://my.telegram.org/apps) (for the Hunter userbot)
- A [Telegram Bot Token](https://core.telegram.org/bots#how-do-i-create-a-bot) from @BotFather
- Your personal Telegram Chat ID (you can get this from bots like @userinfobot)
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and fill in your details:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and provide your credentials:
   - `GEMINI_API_KEY`: Your Google Gemini API Key
   - `BOT_TOKEN`: Your Telegram Bot Token
   - `MY_CHAT_ID`: Your personal Telegram Chat ID
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `TARGET_CHANNELS`: (Optional) Comma-separated list of channel IDs/usernames to monitor.

3. **Initialize the Telethon Session:**
   Because `telethon` requires a one-time login using your phone number and a verification code, you must initialize the session manually first:
   ```bash
   python init_session.py
   ```
   Follow the on-screen prompts to log in. This will generate a `hunter_session.session` file locally.

4. **Run the Main System:**
   Once the session is created, you can run the autonomous agents:
   ```bash
   python main.py
   ```

The system will now run concurrently. The Hunter will log tasks to `tasks.db`, and the Executor will process them and message you on Telegram.
