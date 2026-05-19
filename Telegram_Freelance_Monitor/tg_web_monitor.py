import os
import time
import asyncio
from playwright.async_api import async_playwright
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Keywords to look for in job postings
KEYWORDS = ["потрібен бот", "python", "script", "скрипт", "автоматизація", "написати бота", "telegram bot"]

# Configuration
TELEGRAM_WEB_URL = "https://web.telegram.org/a/"
USER_DATA_DIR = "./telegram_session"

async def monitor_chat(page):
    """Monitors the currently open chat for keywords."""
    logging.info("Starting to monitor for new messages...")

    # Keep track of messages we've already seen
    seen_messages = set()

    while True:
        try:
            # Look for message bubbles in Telegram Web A
            # The class names might change slightly depending on Telegram updates,
            # 'message' or '.message-text' are standard target classes.
            message_elements = await page.query_selector_all('.message-text')

            # Only check the last few messages to be fast
            for msg_elem in message_elements[-5:]:
                text = await msg_elem.inner_text()
                msg_id = await msg_elem.evaluate('(node) => node.parentElement.id') or text

                if msg_id not in seen_messages:
                    seen_messages.add(msg_id)
                    text_lower = text.lower()

                    if any(keyword in text_lower for keyword in KEYWORDS):
                        logging.warning(f"🚨 MATCH FOUND! 🚨\nText: {text}\n----------------------")
                        # Here you could trigger a system sound
                        # print('\a')  # Beep sound

        except Exception as e:
            # Ignore minor DOM exceptions when messages move
            pass

        await asyncio.sleep(2) # Check every 2 seconds

async def main():
    print("="*50)
    print("🚀 Telegram Web Freelance Sniper 🚀")
    print("="*50)
    print("Note: This script uses Playwright to control Telegram Web.")
    print("It bypasses the need for an API Key or api_hash/api_id.")

    async with async_playwright() as p:
        # Launch browser in non-headless mode so the user can scan the QR code
        # User Data Dir saves the session so you don't have to scan QR every time
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False, # Set to False so you can see the browser
            viewport={'width': 1280, 'height': 800}
        )

        page = await browser.new_page()
        await page.goto(TELEGRAM_WEB_URL)

        logging.info("Waiting for Telegram Web to load...")

        # Wait for the chat list to appear (indicates successful login)
        try:
            # Wait up to 60 seconds for the user to scan the QR code if needed
            await page.wait_for_selector('.chat-list', timeout=60000)
            logging.info("✅ Logged in successfully!")
        except Exception:
            logging.error("❌ Login timeout. Please scan the QR code and restart the script.")
            await browser.close()
            return

        print("\n" + "="*50)
        print("INSTRUCTIONS:")
        print("1. Click on the freelance channel you want to monitor in the browser.")
        print("2. The script will continuously read new messages in the open chat.")
        print("3. When a keyword is found, it will print a 🚨 WARNING 🚨 in this console.")
        print("="*50 + "\n")

        # Start monitoring loop
        await monitor_chat(page)

        # Clean up (won't be reached unless monitor_chat breaks)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping monitor...")
