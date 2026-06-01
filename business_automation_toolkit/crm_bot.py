import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# Admin ID can be a comma-separated list of IDs, or a single ID
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "YOUR_ADMIN_ID_HERE")
try:
    ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip().isdigit()]
except ValueError:
    ADMIN_IDS = []

# Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Handles the /start command from customers."""
    welcome_text = (
        "👋 Welcome to our Support Bot!\n\n"
        "Please send your inquiry here, and our team will get back to you shortly."
    )
    await message.answer(welcome_text)

@dp.message(Command("reply"))
async def cmd_reply(message: Message):
    """
    Handles the /reply command from admins.
    Usage: /reply <user_id> <message>
    """
    if message.from_user.id not in ADMIN_IDS and len(ADMIN_IDS) > 0:
        await message.answer("❌ You are not authorized to use this command.")
        return

    # Parse the command
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠️ Usage: /reply <user_id> <message>")
        return

    try:
        user_id = int(args[1])
        reply_text = args[2]

        # Send the reply to the user
        await bot.send_message(chat_id=user_id, text=f"👨‍💻 Support Reply:\n\n{reply_text}")
        await message.answer("✅ Reply sent successfully.")

    except ValueError:
        await message.answer("❌ Invalid User ID. Please provide a numeric ID.")
    except Exception as e:
        logging.error(f"Failed to send reply to {args[1]}: {e}")
        await message.answer("❌ Failed to send reply. The user might have blocked the bot.")

@dp.message(F.text & ~F.text.startswith('/'))
async def forward_to_admin(message: Message):
    """Forwards incoming customer messages to the admin(s)."""
    # Prevent bot from forwarding its own messages or commands

    user = message.from_user

    # We remove parse_mode for the main text to avoid markdown injection issues
    # from random characters in the user's name or message.
    user_info = f"User: {user.full_name}\nUsername: @{user.username}\nID: {user.id}"

    forward_text = f"📩 New Inquiry\n\n{user_info}\n\nMessage:\n{message.text}\n\nTo reply, use:\n/reply {user.id} <your message>"

    if not ADMIN_IDS:
         logging.warning("No ADMIN_IDS set. Received a message but don't know where to forward it.")
         await message.answer("Our team is currently unavailable. Please try again later.")
         return

    success_count = 0
    for admin_id in ADMIN_IDS:
        try:
            # Removed parse_mode to prevent malicious or accidental markdown injection errors
            await bot.send_message(chat_id=admin_id, text=forward_text)
            success_count += 1
        except Exception as e:
            logging.error(f"Failed to forward message to admin {admin_id}: {e}")

    if success_count > 0:
        await message.answer("✅ Your message has been sent to our team. We will reply soon.")
    else:
        await message.answer("❌ Sorry, we couldn't deliver your message at this time.")

async def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
         logging.error("BOT_TOKEN is not set. Please update your .env file.")
         return

    if not ADMIN_IDS:
        logging.warning("ADMIN_IDS is not set properly. Bot won't be able to forward messages.")

    logging.info("Starting Telegram Mini-CRM Bot...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
         logging.error(f"Bot polling stopped due to an error: {e}")
    finally:
         await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
