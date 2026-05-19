import asyncio
import os
import logging
import google.generativeai as genai
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from db import get_uncompleted_task, mark_task_completed

logger = logging.getLogger(__name__)

# Constants
POLLING_INTERVAL = 10  # Seconds to wait between DB checks

async def process_task(task, bot: Bot, my_chat_id: str):
    """Processes a single task using Gemini and sends it to Telegram."""
    task_id = task['id']
    source_link = task['source_link']
    instructions = task['instructions']

    logger.info(f"Processing task {task_id} from {source_link}")

    try:
        # Prompt Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        system_prompt = (
            "You are an autonomous AI agent expert at completing micro-tasks. "
            "You will be given instructions. Flawlessly execute the micro-task and "
            "provide the final result. Keep the response concise and strictly focused "
            "on the required output."
        )

        prompt = f"{system_prompt}\n\nTask Instructions:\n{instructions}"

        # Async call is available for generative AI models, although standard generate_content might be synchronous.
        # generate_content_async is preferred.
        response = await model.generate_content_async(prompt)

        gemini_output = response.text

        # Format the message
        message_text = (
            f"<b>✅ Task Completed!</b>\n\n"
            f"<b>Source:</b> {source_link}\n\n"
            f"<b>Result:</b>\n{gemini_output}"
        )

        # Send to Telegram
        # In case the message is too long, we might need to chunk it, but for micro-tasks it should be fine
        if len(message_text) > 4000:
            message_text = message_text[:4000] + "... [TRUNCATED]"

        await bot.send_message(chat_id=my_chat_id, text=message_text, disable_web_page_preview=True)

        # Mark as completed
        await mark_task_completed(task_id)
        logger.info(f"Successfully processed and delivered task {task_id}")

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        error_str = str(e).lower()

        # Implement robust error handling for API rate limits and connection issues
        if "429" in error_str or "too many requests" in error_str or "quota" in error_str:
            logger.warning("Rate limit hit or quota exceeded for Gemini API. Waiting before retrying...")
            await asyncio.sleep(60) # Backoff for 60 seconds
            # Do not mark as completed, it will be retried
            return

        try:
            error_msg = f"<b>❌ Error executing task {task_id}:</b>\n<code>{str(e)}</code>"
            await bot.send_message(chat_id=my_chat_id, text=error_msg)
        except TelegramAPIError as te:
            if "RetryAfter" in str(te) or "retry after" in str(te).lower():
                 logger.warning(f"Telegram API Rate Limit. {te}")
                 await asyncio.sleep(30)
            else:
                 logger.error(f"Failed to send error message to Telegram: {te}")

        # We'll mark the task as completed to avoid infinite retry loops on bad prompts/errors
        # unless it was a rate limit handled above.
        await mark_task_completed(task_id)

async def run_executor():
    """Main loop for the Executor Bot."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    bot_token = os.getenv("BOT_TOKEN")
    my_chat_id = os.getenv("MY_CHAT_ID")

    if not all([gemini_api_key, bot_token, my_chat_id]):
        logger.error("Missing required environment variables for Executor.")
        return

    # Configure Gemini
    genai.configure(api_key=gemini_api_key)

    # Configure Telegram Bot
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    logger.info("Executor bot started polling for tasks...")

    try:
        while True:
            try:
                task = await get_uncompleted_task()

                if task:
                    await process_task(task, bot, my_chat_id)
                else:
                    # No pending tasks, wait before polling again
                    await asyncio.sleep(POLLING_INTERVAL)
            except Exception as e:
                logger.error(f"Error in executor loop: {e}")
                await asyncio.sleep(POLLING_INTERVAL)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_executor())
