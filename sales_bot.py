import os
import sys
import logging
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Налаштування логування
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("SalesBot")

# Завантаження змінних середовища
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@your_username")

if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    logger.error("BOT_TOKEN не знайдено в .env файлі. Будь ласка, налаштуйте його.")
    sys.exit(1)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обробник команди /start. Вітає користувача та пропонує меню послуг.
    """
    welcome_text = (
        f"Вітаю, {message.from_user.first_name}. 💎\n\n"
        "Ви знаходитесь в офіційному боті **AI LeadGen Pro** — преміального рішення для "
        "автоматичного пошуку гарячих B2B клієнтів у Telegram.\n\n"
        "Наш штучний інтелект безперервно аналізує сотні чатів і миттєво доставляє цільові запити "
        "прямо у вашу CRM або особисті повідомлення.\n\n"
        "Оберіть формат співпраці нижче:"
    )

    # Створення преміум інлайн-клавіатури
    builder = InlineKeyboardBuilder()
    builder.button(text="ℹ️ Як працює AI LeadGen", callback_data="info_how_it_works")
    builder.button(text="📁 Ліцензія: Скрипт ($50)", callback_data="buy_script")
    builder.button(text="💎 Ліцензія + VIP Підтримка ($100)", callback_data="buy_turnkey")
    builder.button(text="👨‍💻 Зв'язок із розробником", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")

    builder.adjust(1, 1, 1, 1)

    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "info_how_it_works")
async def callback_how_it_works(callback: CallbackQuery):
    text = (
        "⚙️ **Архітектура AI LeadGen Pro**\n\n"
        "1. **Моніторинг:** Система підключається до вашого акаунта і сканує вибрані цільові чати 24/7.\n"
        "2. **Аналіз Контексту:** Нейромережа (OpenAI) аналізує останні повідомлення, виявляючи реальний намір клієнта купити послугу.\n"
        "3. **Авто-відповідь:** AI формує природну, нешаблонну відповідь і миттєво зв'язується з лідом, обходячи спам-фільтри.\n"
        "4. **Експорт:** Всі дані ліда синхронізуються у вашу таблицю.\n\n"
        "Ви купуєте інструмент, який генерує прибуток на автопілоті. Налаштування залишається на вашому боці, але ви завжди контролюєте процес."
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "buy_script")
async def callback_buy_script(callback: CallbackQuery):
    text = (
        "📁 **Ліцензія: AI Script ($50)**\n\n"
        "Ви купуєте повний доступ до вихідного коду (Python, Telethon, OpenAI) та покрокову документацію "
        "для самостійного розгортання на вашому ПК або сервері.\n\n"
        "💳 **Реквізити для оплати (50 USDT, мережа TRC20):**\n"
        "`TSP2tJbLpfR1YvRz4VY67nMMXi6PTa6mfK`\n\n"
        f"Для отримання файлів надішліть підтвердження транзакції: {OWNER_USERNAME}"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "buy_turnkey")
async def callback_buy_turnkey(callback: CallbackQuery):
    text = (
        "💎 **Ліцензія + VIP Підтримка ($100)**\n\n"
        "Ви отримуєте систему AI LeadGen Pro, інструкції для самостійного встановлення, **АЛЕ** "
        "також отримуєте мою особисту підтримку. Якщо у вас виникнуть труднощі під час налаштування — "
        "я підкажу, допоможу вирішити помилки та проконсультую щодо найкращих практик використання.\n\n"
        "💳 **Реквізити для оплати (100 USDT, мережа TRC20):**\n"
        "`TSP2tJbLpfR1YvRz4VY67nMMXi6PTa6mfK`\n\n"
        f"Для початку співпраці надішліть підтвердження транзакції: {OWNER_USERNAME}"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

async def main():
    logger.info("Запуск Telegram Sales Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем.")
