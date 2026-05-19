import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram.enums import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Bot and Dispatcher
# Note: Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Bad words list for anti-spam/profanity filter
BAD_WORDS = ['spam', 'scam', 'crypto', 'fake', 'link']

async def is_admin(message: Message):
    """Helper function to check if the user is an admin."""
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return chat_member.status in ['administrator', 'creator']

@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    """Sends a welcome message and explains the bot's capabilities."""
    help_text = (
        "🤖 <b>Pro AI Telegram Admin Bot</b>\n\n"
        "I am your dedicated group management assistant!\n\n"
        "<b>Features:</b>\n"
        "✨ Auto-welcome new users\n"
        "🛡️ Anti-spam (deletes bad words)\n"
        "🤐 <code>/mute [minutes]</code> (Reply to a message, Admins only)\n"
        "🔨 <code>/ban</code> (Reply to a message, Admins only)\n\n"
        "Add me to your group and make me an Admin to get started!"
    )
    await message.reply(help_text)

@dp.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    """Welcomes new users to the group."""
    for new_member in message.new_chat_members:
        welcome_msg = (
            f"Welcome to the group, <b>{new_member.first_name}</b>! 🎉\n"
            f"Please read the rules and enjoy your stay."
        )
        await message.reply(welcome_msg)

@dp.message(Command("mute"))
async def mute_user(message: Message, command: Command):
    """Mutes a user for a specified number of minutes. Admins only."""
    if not await is_admin(message):
        await message.reply("❌ You must be an admin to use this command.")
        return

    if not message.reply_to_message:
        await message.reply("⚠️ You need to reply to the user's message to mute them.")
        return

    # Check if a time was provided
    args = message.text.split()[1:]
    mute_minutes = 10 # default 10 minutes
    if args and args[0].isdigit():
        mute_minutes = int(args[0])

    target_user_id = message.reply_to_message.from_user.id
    target_user_name = message.reply_to_message.from_user.first_name

    # Current time + mute_minutes
    import time
    until_date = int(time.time()) + (mute_minutes * 60)

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply(f"🤐 <b>{target_user_name}</b> has been muted for {mute_minutes} minutes.")
    except Exception as e:
        await message.reply(f"❌ Failed to mute user. Ensure I have admin rights. Error: {e}")

@dp.message(Command("ban"))
async def ban_user(message: Message):
    """Bans a user from the group. Admins only."""
    if not await is_admin(message):
        await message.reply("❌ You must be an admin to use this command.")
        return

    if not message.reply_to_message:
        await message.reply("⚠️ You need to reply to the user's message to ban them.")
        return

    target_user_id = message.reply_to_message.from_user.id
    target_user_name = message.reply_to_message.from_user.first_name

    try:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=target_user_id)
        await message.reply(f"🔨 <b>{target_user_name}</b> has been banned from the group.")
    except Exception as e:
        await message.reply(f"❌ Failed to ban user. Ensure I have admin rights. Error: {e}")

@dp.message()
async def anti_spam_filter(message: Message):
    """Filters out messages containing bad words."""
    if not message.text:
        return

    text_lower = message.text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            try:
                await message.delete()
                warning_msg = await message.answer(
                    f"⚠️ <b>{message.from_user.first_name}</b>, your message was deleted for containing a prohibited word."
                )
                # Optionally delete the warning message after a few seconds
                await asyncio.sleep(5)
                await warning_msg.delete()
            except Exception as e:
                logging.error(f"Failed to delete message or send warning: {e}")
            break # No need to check other words if one is already found

async def main():
    print("Bot is starting...")
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
