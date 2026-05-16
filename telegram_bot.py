import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import urllib.request
import json

# Встановлення рівня логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота (заглушка для токена)
# УВАГА: Замість "YOUR_BOT_TOKEN_HERE" потрібно вставити справжній токен від BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Створення об'єктів бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_exchange_rates():
    """Функція для отримання курсу валют."""
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        rates = data.get('rates', {})

        uah_rate = rates.get('UAH')
        eur_rate = rates.get('EUR')
        gbp_rate = rates.get('GBP')

        if not uah_rate:
            return "❌ Не вдалося отримати курс гривні."

        result = (
            "📊 Актуальний курс валют:\n"
            f"💵 1 USD = {uah_rate:.2f} UAH\n"
            f"💶 1 EUR = {(uah_rate/eur_rate):.2f} UAH\n"
            f"💷 1 GBP = {(uah_rate/gbp_rate):.2f} UAH"
        )
        return result
    except Exception as e:
        return f"❌ Помилка при отриманні даних: {e}"

# Обробник команди /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! 👋 Я простий бот, створений Jules.\nНатисни /rates, щоб побачити актуальний курс валют!")

# Обробник команди /rates
@dp.message(Command("rates"))
async def cmd_rates(message: types.Message):
    # Показуємо користувачеві, що бот обробляє запит
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    rates_text = get_exchange_rates()
    await message.answer(rates_text)

# Обробник будь-якого іншого тексту
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(f"Ти сказав: '{message.text}'.\n\nЩоб дізнатися курс валют, використовуй команду /rates.")

async def main():
    # Запуск процесу поллінгу (очікування нових повідомлень)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Помилка при запуску бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
