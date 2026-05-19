import os
import asyncio
import logging
from telethon import TelegramClient
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_session():
    """Initializes the Telethon session by prompting the user for phone/code."""
    load_dotenv()

    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        logger.error("API_ID and API_HASH must be set in .env to initialize the session.")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        logger.error("API_ID must be an integer.")
        return

    logger.info("Starting Telethon client for initialization...")
    client = TelegramClient('hunter_session', api_id, api_hash)

    await client.start()

    if await client.is_user_authorized():
        logger.info("Session successfully authorized. You can now run the main bot.")
    else:
        logger.error("Failed to authorize the session.")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(init_session())
