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
        logger.warning("No TARGET_CHANNELS specified. Exiting Hunter to avoid monitoring all private chats globally.")
        return

    client = TelegramClient('hunter_session', api_id, api_hash)

    import google.generativeai as genai
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)

    @client.on(events.NewMessage(chats=target_channels))
    async def handler(event):
        try:
            message_text = event.message.text
            if not message_text:
                return

            # Filter by keywords. Return early if no match, avoiding logging irrelevant messages.
            keywords = ["task", "job", "bounty", "do this", "need help"]
            if not any(k in message_text.lower() for k in keywords):
                return

            # Parse instructions using Gemini if available, otherwise just use raw text
            final_instructions = message_text
            if gemini_api_key:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (
                        "Extract the core task instructions and requirements from the following text. "
                        "Format it cleanly so it is ready to be executed by another AI agent.\n\n"
                        f"Text:\n{message_text}"
                    )
                    response = await model.generate_content_async(prompt)
                    if response.text:
                        final_instructions = response.text
                except Exception as e:
                    logger.error(f"Error extracting structured task with Gemini: {e}")
                    # Fallback to raw text

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
            await insert_task(source_link, final_instructions)

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
