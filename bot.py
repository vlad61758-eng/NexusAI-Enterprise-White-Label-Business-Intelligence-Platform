import os
import sys
import logging
import asyncio
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, rpcerrorlist

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Read configurations
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
TARGET_CHATS_STR = os.getenv('TARGET_CHATS', '')
KEYWORDS_STR = os.getenv('KEYWORDS', '')
ADMIN_CHANNEL = os.getenv('ADMIN_CHANNEL', 'me')

# Validate required variables
if not API_ID or not API_HASH:
    logger.error("API_ID or API_HASH is missing in the .env file. Please check your configuration.")
    sys.exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    logger.error("API_ID must be an integer.")
    sys.exit(1)

# Parse lists
TARGET_CHATS = [chat.strip() for chat in TARGET_CHATS_STR.split(',') if chat.strip()]
KEYWORDS = [kw.strip().lower() for kw in KEYWORDS_STR.split(',') if kw.strip()]

if not TARGET_CHATS:
    logger.warning("No TARGET_CHATS defined in .env. The bot will not monitor any chats.")
if not KEYWORDS:
    logger.warning("No KEYWORDS defined in .env. The bot will monitor but won't match any keywords.")

# ==========================================
# 2. DATA EXPORT LOGIC
# ==========================================
EXCEL_FILE = 'leads.xlsx'

def save_lead_to_excel(username, name, matched_keyword, message_snippet, chat_title, message_link):
    """
    Saves the lead data to an Excel file using pandas.
    """
    data = {
        'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'Username': [f"@{username}" if username else "No username"],
        'Name': [name or "Unknown"],
        'Matched Keyword': [matched_keyword],
        'Message Snippet': [message_snippet],
        'Chat': [chat_title],
        'Message Link': [message_link]
    }

    df_new = pd.DataFrame(data)

    try:
        if os.path.exists(EXCEL_FILE):
            # Append to existing file
            with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                # Find the max row
                startrow = writer.sheets['Sheet1'].max_row
                df_new.to_excel(writer, sheet_name='Sheet1', startrow=startrow, header=False, index=False)
        else:
            # Create new file
            df_new.to_excel(EXCEL_FILE, sheet_name='Sheet1', index=False)
        logger.info(f"Lead saved to {EXCEL_FILE}")
    except Exception as e:
        logger.error(f"Error saving lead to Excel: {e}")

# ==========================================
# 3. CORE LOGIC
# ==========================================

# Initialize the Telethon client
# Using 'userbot_session' session name, which creates userbot_session.session file
client = TelegramClient('userbot_session', API_ID, API_HASH)

def check_keywords(text):
    """
    Checks if any of the keywords exist in the text (case-insensitive).
    Returns the first matched keyword, or None if no match.
    """
    if not text:
        return None

    text_lower = text.lower()
    for kw in KEYWORDS:
        if kw in text_lower:
            return kw
    return None

@client.on(events.NewMessage(chats=TARGET_CHATS if TARGET_CHATS else None))
async def handler(event):
    """
    Handles new incoming messages in the targeted chats.
    """
    message_text = event.raw_text

    # Check for keywords
    matched_keyword = check_keywords(message_text)

    if matched_keyword:
        sender = await event.get_sender()
        chat = await event.get_chat()

        # Get sender details
        username = getattr(sender, 'username', None)
        first_name = getattr(sender, 'first_name', '')
        last_name = getattr(sender, 'last_name', '')
        name = f"{first_name} {last_name}".strip()

        chat_title = getattr(chat, 'title', 'Private Chat')

        # Try to generate a message link
        try:
            if getattr(chat, 'username', None):
                msg_link = f"https://t.me/{chat.username}/{event.id}"
            else:
                msg_link = f"https://t.me/c/{chat.id}/{event.id}"
                # t.me/c/ links work for private groups if the user is a member,
                # but id must be manipulated sometimes (e.g. removing -100 prefix)
                if str(chat.id).startswith('-100'):
                    msg_link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"
        except Exception:
            msg_link = "Link unavailable"

        # Truncate message for snippet
        snippet = message_text[:100] + "..." if len(message_text) > 100 else message_text

        # Save to Excel
        save_lead_to_excel(
            username=username,
            name=name,
            matched_keyword=matched_keyword,
            message_snippet=snippet,
            chat_title=chat_title,
            message_link=msg_link
        )

        # Format the alert message
        alert_msg = (
            f"🚨 **New Lead Detected!**\n\n"
            f"**Keyword:** `{matched_keyword}`\n"
            f"**Chat:** {chat_title}\n"
            f"**Sender:** {name} " + (f"(@{username})" if username else "") + "\n\n"
            f"**Message:**\n_{snippet}_\n\n"
            f"🔗 [Go to Message]({msg_link})"
        )

        # Send alert to Admin
        try:
            await client.send_message(ADMIN_CHANNEL, alert_msg)
            logger.info(f"Alert sent to {ADMIN_CHANNEL} for keyword '{matched_keyword}'")
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

# ==========================================
# 4. MAIN LOOP WITH ERROR HANDLING
# ==========================================

async def main():
    while True:
        try:
            logger.info("Starting UserBot...")
            await client.start()
            logger.info(f"Monitoring chats: {TARGET_CHATS}")
            logger.info(f"Monitoring keywords: {KEYWORDS}")
            logger.info("UserBot is running. Press Ctrl+C to stop.")

            # Run the client until disconnected
            await client.run_until_disconnected()
        except FloodWaitError as e:
            logger.warning(f"Flood wait error. Sleeping for {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
        except rpcerrorlist.AuthKeyDuplicatedError:
            logger.error("Session revoked or duplicated. Please delete the session file and re-authenticate.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.info("Reconnecting in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("UserBot stopped manually.")
