import os
import time
import asyncio
import logging
import requests
import google.generativeai as genai
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # The bot you create via BotFather to send you alerts
MY_CHAT_ID = os.getenv("MY_CHAT_ID")  # Your personal Telegram User ID

# Configuration
TELEGRAM_WEB_URL = "https://web.telegram.org/a/"
USER_DATA_DIR = "./telegram_session"

# Initialize AI if key exists
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    logging.warning("GEMINI_API_KEY not found. AI filtering will be disabled.")

def send_telegram_alert(text):
    """Sends a message to your personal Telegram using the Bot API."""
    if not BOT_TOKEN or not MY_CHAT_ID:
        logging.error("BOT_TOKEN or MY_CHAT_ID missing. Cannot send Telegram alert.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
        logging.info("Successfully forwarded task to your Telegram.")
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

async def analyze_task_complexity(text):
    """Uses AI to determine if a task is simple enough to do in 5-10 minutes."""
    if not GEMINI_API_KEY:
        # Fallback to basic keyword matching if AI is not configured
        easy_keywords = ["простий", "швидко", "фікс", "помилка", "парсер", "скрипт", "simple", "fix", "easy"]
        if any(word in text.lower() for word in easy_keywords):
            return True, "Basic keyword match"
        return False, "Not simple"

    prompt = f"""
    You are an elite Senior Python Developer. I am looking for very simple, quick freelance coding tasks.
    Read the following job description from a Telegram chat:

    "{text}"

    Can this task be completed (coded, tested, and delivered) by a Senior AI-assisted developer within 5 to 10 minutes?
    Look for things like: simple bots, basic web scraping, bug fixes, script modifications, or API connections.

    Respond STRICTLY with "YES" or "NO" on the first line.
    On the second line, give a very brief 1-sentence explanation of why.
    """

    try:
        # To avoid rate limits on free Gemini, only analyze messages that seem like actual job postings
        # (e.g. have a price symbol, or words like "потрібен", "need", "бюджет", "budget")
        trigger_words = ["need", "потрібен", "ищу", "шукаю", "$", "budget", "бюджет", "task", "завдання", "заказ"]
        if not any(word in text.lower() for word in trigger_words):
            return False, "Does not look like a job posting."

        response = model.generate_content(prompt)
        result = response.text.strip().split('\n')
        decision = result[0].strip().upper()
        reason = result[1] if len(result) > 1 else "No reason provided."

        if "YES" in decision:
            return True, reason
        return False, reason
    except Exception as e:
        logging.error(f"AI analysis failed: {e}")
        return False, "AI Error"

async def monitor_chat(page):
    """Monitors the currently open chat for new messages."""
    logging.info("Starting SMART Sniper... monitoring messages.")

    seen_messages = set()

    while True:
        try:
            message_elements = await page.query_selector_all('.message-text')

            # Check the most recent messages. Initially we check more to catch up on old tasks.
            # Use -20 to check the last 20 messages on the first run, then it will only process new ones
            for msg_elem in message_elements[-20:]:
                text = await msg_elem.inner_text()
                # If message is too short, it's likely just chat, not a job posting
                if len(text) < 15:
                    continue

                msg_id = await msg_elem.evaluate('(node) => node.parentElement.id') or text

                if msg_id not in seen_messages:
                    seen_messages.add(msg_id)

                    # 1. Analyze Complexity with AI
                    is_simple, reason = await analyze_task_complexity(text)

                    # 2. If AI says it's a 5-10 min job, alert the user
                    if is_simple:
                        logging.warning(f"🎯 EASY TASK FOUND! Reason: {reason}")

                        alert_message = (
                            f"🟢 <b>Легке завдання знайдено (5-10 хв)!</b>\n\n"
                            f"<b>Текст:</b>\n<i>{text}</i>\n\n"
                            f"<b>Думка AI:</b> {reason}\n\n"
                            f"Відповідай замовнику швидше!"
                        )
                        send_telegram_alert(alert_message)

                        # Sleep briefly to avoid spamming the AI API if chat is hyper-active
                        await asyncio.sleep(5)

        except Exception as e:
            pass

        await asyncio.sleep(2) # Refresh interval

async def main():
    print("="*50)
    print("🧠 Smart AI Telegram Freelance Sniper 🧠")
    print("="*50)

    if not BOT_TOKEN or not MY_CHAT_ID:
        print("⚠️ WARNING: BOT_TOKEN or MY_CHAT_ID not found in .env file.")
        print("Alerts will only be printed to this console, not sent to your phone.")
        print("="*50)

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = await browser.new_page()
        await page.goto(TELEGRAM_WEB_URL)

        logging.info("Waiting for Telegram Web to load...")
        try:
            await page.wait_for_selector('.chat-list', timeout=60000)
            logging.info("✅ Logged in successfully!")
        except Exception:
            logging.error("❌ Login timeout. Please scan the QR code and restart.")
            await browser.close()
            return

        print("\n" + "="*50)
        print("INSTRUCTIONS:")
        print("1. Click on the freelance channel you want to monitor.")
        print("2. The AI will read every new message.")
        print("3. If it decides the coding task takes 5-10 minutes, it will forward it to your Telegram phone app!")
        print("="*50 + "\n")

        await monitor_chat(page)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Smart Sniper...")
