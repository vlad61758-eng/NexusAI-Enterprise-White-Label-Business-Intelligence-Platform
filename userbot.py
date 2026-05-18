import os
import sys
import logging
import asyncio
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.types import User

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("userbot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("UserBot")

# Load environment variables
load_dotenv()

# Read configurations
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
TARGET_CHATS_STR = os.getenv('TARGET_CHATS', '')
KEYWORDS_STR = os.getenv('KEYWORDS', '')
ADMIN_CHAT = os.getenv('ADMIN_CHAT', 'me')

# Validate required variables
if not API_ID or not API_HASH:
    logger.error("API_ID or API_HASH not found in .env file. Please configure them.")
    sys.exit(1)

# Parse lists
TARGET_CHATS = [chat.strip() for chat in TARGET_CHATS_STR.split(',') if chat.strip()]
KEYWORDS = [kw.strip().lower() for kw in KEYWORDS_STR.split(',') if kw.strip()]

# Initialize the Telethon client
# Using a session file named 'userbot_session'
client = TelegramClient('userbot_session', int(API_ID), API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHATS if TARGET_CHATS else None))
async def handle_new_message(event):
    """
    Listens to new messages in target chats and scans for keywords.
    """
    message_text = event.message.text
    if not message_text:
        return

    message_text_lower = message_text.lower()

    # Check if any keyword is in the message
    matched_keywords = [kw for kw in KEYWORDS if kw in message_text_lower]

    if matched_keywords:
        logger.info(f"Keyword matched: {matched_keywords} in chat {event.chat_id}")
        await process_lead(event, matched_keywords)

async def process_lead(event, matched_keywords):
    """
    Processes a matched message by sending an alert and saving to Excel.
    """
    try:
        sender = await event.get_sender()
        chat = await event.get_chat()

        # Get sender info
        username = getattr(sender, 'username', 'N/A')
        username_str = f"@{username}" if username and username != 'N/A' else "N/A"

        first_name = getattr(sender, 'first_name', '') or ''
        last_name = getattr(sender, 'last_name', '') or ''
        name = f"{first_name} {last_name}".strip() or "N/A"

        # Get chat info
        chat_title = getattr(chat, 'title', str(event.chat_id))

        # Format message link if possible
        if hasattr(chat, 'username') and chat.username:
            message_link = f"https://t.me/{chat.username}/{event.id}"
        else:
            # Private group format
            message_link = f"https://t.me/c/{str(event.chat_id).replace('-100', '')}/{event.id}"

        # Message snippet
        message_text = event.message.text
        snippet = message_text[:100] + "..." if len(message_text) > 100 else message_text

        matched_kw_str = ", ".join(matched_keywords)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare alert message
        alert_msg = (
            f"🚨 **Lead Alert!**\n\n"
            f"**Keyword(s):** {matched_kw_str}\n"
            f"**Chat:** {chat_title}\n"
            f"**Sender:** {name} ({username_str})\n"
            f"**Link:** [Go to Message]({message_link})\n\n"
            f"**Snippet:**\n{snippet}"
        )

        # Send alert
        await client.send_message(ADMIN_CHAT, alert_msg, link_preview=False)
        logger.info(f"Alert sent to admin chat ({ADMIN_CHAT})")

        # Save to Excel
        save_to_excel({
            "Date": current_time,
            "Username": username_str,
            "Name": name,
            "Matched Keyword": matched_kw_str,
            "Chat": chat_title,
            "Message Link": message_link,
            "Snippet": snippet
        })

    except Exception as e:
        logger.error(f"Error processing lead: {e}")

def save_to_excel(data, filename="leads.xlsx"):
    """
    Saves a dictionary of data to an Excel file using pandas.
    """
    df_new = pd.DataFrame([data])

    try:
        # If file exists, append to it
        if os.path.exists(filename):
            df_existing = pd.read_excel(filename)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(filename, index=False)
        else:
            # Create new file
            df_new.to_excel(filename, index=False)
        logger.info(f"Lead saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving to Excel: {e}")

async def main():
    logger.info("Starting Telegram UserBot...")
    try:
        await client.start()
        logger.info("Client started successfully.")

        me = await client.get_me()
        logger.info(f"Logged in as {me.first_name} (@{me.username})")

        logger.info("Bot is running and listening for messages...")
        await client.run_until_disconnected()

    except FloodWaitError as e:
        logger.warning(f"Flood wait error. Sleeping for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    try:
        # Run the async main function
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("UserBot stopped by user.")
