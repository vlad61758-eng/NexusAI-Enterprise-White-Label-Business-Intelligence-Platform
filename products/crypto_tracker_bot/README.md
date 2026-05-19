# Crypto Price Tracker Bot 📈📉

Never miss a major market move again! This automated Telegram bot constantly monitors the cryptocurrency market (via the free Binance public API) and instantly messages you when there is a sudden spike or dump in price.

## Features:
- 24/7 background price monitoring.
- Instant Telegram notifications for sudden price changes.
- Customizable alert thresholds (default: 2% change in 5 minutes).
- Lightweight and easy to run on any computer or cheap VPS server.

## Setup Instructions 🛠️

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*Important for Windows users: When installing, make sure to check the box that says "Add Python to PATH".*

### 2. Get a Telegram Bot Token
1. Open Telegram and search for `@BotFather`.
2. Send the command `/newbot` and follow the steps to give your bot a name and username.
3. BotFather will give you an **API Token** (a long string of numbers and letters). Copy this.

### 3. Install Dependencies
Open your terminal (or Command Prompt) inside this folder and run:
```bash
pip install -r requirements.txt
```

### 4. Add Your Token
1. In this folder, create a new file named exactly `.env` (don't forget the dot).
2. Open the `.env` file in a text editor and add this line, pasting the token you got from BotFather:
```text
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## How to Run & Customization 🚀

### Running the Bot
Open your terminal in this folder and run:
```bash
python tracker_bot.py
```
Leave this window open! As long as the terminal is running, the bot is active.

### Using the Bot
1. Open Telegram and find your newly created bot.
2. Click **Start** (or type `/start`).
3. You are now subscribed! The bot will message you if the price moves drastically.
4. Type `/price` at any time to check the current market price.

### Customizing Alerts
If you want to change the coin or the sensitivity, open `tracker_bot.py` in a text editor and change these lines near the top:
```python
CHECK_INTERVAL_SECONDS = 300  # How often to check (in seconds)
ALERT_THRESHOLD_PERCENT = 2.0  # Percentage change required to trigger an alert
TARGET_SYMBOL = "BTCUSDT"     # The coin to track (e.g., ETHUSDT, SOLUSDT)
```