import os
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN not found in .env file.")
    exit(1)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# List of active user chat IDs to send alerts to
# In a real app, you'd save this to a database like SQLite
active_users = set()

# Configuration
CHECK_INTERVAL_SECONDS = 300  # Check every 5 minutes
ALERT_THRESHOLD_PERCENT = 2.0  # Alert if price moves 2% up or down
TARGET_SYMBOL = "BTCUSDT"

# Global state to keep track of the last known price
last_known_price = None

def get_crypto_price(symbol):
    """Fetches the current price of a symbol from the Binance Public API."""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Welcome message and add user to active list."""
    user_id = message.from_user.id
    active_users.add(user_id)

    welcome_text = (
        "🚀 **Crypto Tracker Bot is Online!**\n\n"
        f"You are now subscribed to price alerts for {TARGET_SYMBOL.replace('USDT', '')}.\n"
        f"I will notify you immediately if the price changes by more than {ALERT_THRESHOLD_PERCENT}% "
        f"within a {CHECK_INTERVAL_SECONDS // 60}-minute window.\n\n"
        "Commands:\n"
        "/price - Get current price\n"
        "/stop - Stop receiving alerts"
    )
    await message.answer(welcome_text, parse_mode="Markdown")
    logging.info(f"User {user_id} started the bot.")

@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    """Remove user from active list."""
    user_id = message.from_user.id
    if user_id in active_users:
        active_users.remove(user_id)
    await message.answer("🛑 You have been unsubscribed from price alerts. Send /start to subscribe again.")
    logging.info(f"User {user_id} stopped alerts.")

@dp.message(Command("price"))
async def cmd_price(message: types.Message):
    """Force check the current price."""
    price = get_crypto_price(TARGET_SYMBOL)
    if price:
        await message.answer(f"💰 Current {TARGET_SYMBOL.replace('USDT', '')} Price: **${price:,.2f}**", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Could not fetch price right now. Try again later.")

async def price_checker_worker():
    """Background task that checks the price periodically and sends alerts."""
    global last_known_price

    # Wait a moment before starting to let the bot initialize
    await asyncio.sleep(5)

    while True:
        try:
            current_price = get_crypto_price(TARGET_SYMBOL)

            if current_price and last_known_price:
                # Calculate percentage change
                change_percent = ((current_price - last_known_price) / last_known_price) * 100

                if abs(change_percent) >= ALERT_THRESHOLD_PERCENT:
                    direction = "🚀 SURGING" if change_percent > 0 else "🩸 DUMPING"
                    icon = "🟢" if change_percent > 0 else "🔴"

                    alert_msg = (
                        f"{icon} **ALERT: {TARGET_SYMBOL.replace('USDT', '')} is {direction}!**\n\n"
                        f"Price changed by **{change_percent:.2f}%**\n"
                        f"Old Price: ${last_known_price:,.2f}\n"
                        f"New Price: **${current_price:,.2f}**"
                    )

                    # Broadcast to all active users
                    for user_id in list(active_users):
                        try:
                            await bot.send_message(user_id, alert_msg, parse_mode="Markdown")
                        except Exception as e:
                            logging.error(f"Failed to send alert to {user_id}: {e}")

                    # Update last known price after alerting
                    last_known_price = current_price

            # If it's the first run, just set the initial price
            elif current_price and not last_known_price:
                last_known_price = current_price
                logging.info(f"Initial price set to ${current_price}")

        except Exception as e:
            logging.error(f"Error in price checker worker: {e}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

async def main():
    logging.info("Starting bot...")

    # Start the background price checking loop
    asyncio.create_task(price_checker_worker())

    # Start polling for Telegram messages
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())