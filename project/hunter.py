import os
import logging
import asyncio
from telethon import TelegramClient, events
from db import insert_task

logger = logging.getLogger(__name__)

async def run_hunter():
    """Runs the Telethon userbot to monitor channels for tasks."""
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    target_channels_str = os.getenv("TARGET_CHANNELS", "")

    if not all([api_id, api_hash]):
        logger.error("Missing API_ID or API_HASH for Hunter.")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        logger.error("API_ID must be an integer.")
        return

    # Parse target channels
    target_channels = []
    if target_channels_str:
        for c in target_channels_str.split(','):
            c = c.strip()
            if c:
                # Telethon can handle usernames (str) or IDs (int)
                try:
                    target_channels.append(int(c))
                except ValueError:
                    target_channels.append(c)

    if not target_channels:
        logger.warning("No TARGET_CHANNELS specified. The Hunter bot will run but won't monitor anything unless configured.")

    client = TelegramClient('hunter_session', api_id, api_hash)

    @client.on(events.NewMessage(chats=target_channels if target_channels else None))
    async def handler(event):
        try:
            # We assume a micro-task contains certain keywords or structure,
            # or we just process all messages in specific task channels.
            # For this implementation, we will log all text messages in target channels
            # as tasks. In a real scenario, more advanced filtering might be needed.
            message_text = event.message.text

            if not message_text:
                return

            # Simple keyword filter (example)
            keywords = ["task", "job", "bounty", "do this", "need help"]
            if not any(k in message_text.lower() for k in keywords) and target_channels:
                # If we're monitoring specific channels, we might want to capture everything.
                # If we're not filtering by keywords, maybe just capture everything.
                pass

            # Get the message link
            chat = await event.get_chat()

            # Construct a message link (works for public supergroups/channels)
            # For private chats, it might not be a valid clicky link, but useful for reference.
            if hasattr(chat, 'username') and chat.username:
                source_link = f"https://t.me/{chat.username}/{event.message.id}"
            else:
                # Fallback to internal format
                source_link = f"Private Chat/Group ID: {chat.id}, Msg ID: {event.message.id}"

            # Insert into database
            logger.info(f"Hunter found potential task in {source_link}")
            await insert_task(source_link, message_text)

        except Exception as e:
            logger.error(f"Error handling new message in Hunter: {e}")

    logger.info("Starting Hunter client...")

    # Do not prompt for input during main execution
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("User is not authorized! Please run 'python init_session.py' first to log in.")
        return

    logger.info("Hunter client is running and monitoring for tasks.")

    # Run until disconnected
    await client.run_until_disconnected()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_hunter())
