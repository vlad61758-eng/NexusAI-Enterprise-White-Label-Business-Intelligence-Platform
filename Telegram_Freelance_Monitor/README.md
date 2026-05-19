# Telegram Web Freelance Sniper 🎯

This script allows you to automate the monitoring of Telegram freelance chats **without needing a Telegram API Key, `api_id`, or `api_hash`**.

It uses browser automation (Playwright) to log into Telegram Web and read messages directly from the screen, exactly like a human would.

## 🚀 The Strategy
1. The script opens Telegram Web.
2. You log in once by scanning the QR code with your phone.
3. You click on a freelance channel (e.g., `@freelance_ua`, `@python_jobs`).
4. The script constantly reads the chat in the background.
5. If someone posts a message containing keywords like "написати бота", "python", or "скрипт", the script instantly alerts you so you can reply first!

## ⚙️ Setup Instructions

### 1. Install Dependencies
Open your terminal inside this `Telegram_Freelance_Monitor` folder and run:
```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers
Playwright needs its own browser binaries to work. Run this command:
```bash
playwright install chromium
```

### 3. Run the Sniper
Run the Python script:
```bash
python tg_web_monitor.py
```

## 📱 First Time Login
The first time you run the script, a Chrome browser window will open showing the Telegram Web login page.
1. Open the Telegram app on your phone.
2. Go to **Settings** > **Devices** > **Link Desktop Device**.
3. Scan the QR code on your computer screen.
4. Once logged in, the script saves your session in the `telegram_session` folder. **You won't have to scan the QR code next time.**

## 🕵️ How to Snipe Orders
1. Once Telegram Web is open and you are logged in, simply click on the freelance chat you want to monitor.
2. Leave the chat open on the screen.
3. Keep an eye on your terminal window.
4. Whenever a new message matches your target keywords, the terminal will flash a `🚨 MATCH FOUND! 🚨` alert.
5. Immediately reply to the client: "Привіт! Я можу зробити це швидко. Пишіть в ПП."
6. Перешліть ТЗ (Технічне завдання) мені (вашому AI), і я напишу код!
