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
        f"👋 Привіт, {message.from_user.first_name}!\n\n"
        "Я — ваш персональний менеджер. Ви, мабуть, перейшли сюди, "
        "бо вас зацікавила наша **B2B AI-система для генерації лідів у Telegram**.\n\n"
        "Ця система 24/7 моніторить нішеві чати за ключовими словами і миттєво "
        "пересилає вам гарячі запити від потенційних клієнтів прямо в особисті повідомлення.\n\n"
        "👇 Оберіть опцію нижче, щоб дізнатися більше або придбати:"
    )

    # Створення інлайн-клавіатури
    builder = InlineKeyboardBuilder()
    builder.button(text="❓ Як це працює?", callback_data="info_how_it_works")
    builder.button(text="💻 Купити скрипт ($50)", callback_data="buy_script")
    builder.button(text="🚀 Купити 'Під Ключ' ($200)", callback_data="buy_turnkey")
    builder.button(text="👤 Зв'язатися зі мною", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")

    builder.adjust(1, 1, 1, 1) # По одній кнопці в ряд

    await message.answer(welcome_text, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "info_how_it_works")
async def callback_how_it_works(callback: CallbackQuery):
    text = (
        "🔍 **Як це працює?**\n\n"
        "1. Ми підключаємо ваш особистий або технічний акаунт до списку з десятків тематичних чатів.\n"
        "2. Бот 24/7 сканує кожне нове повідомлення на задані ключові слова (наприклад: *потрібен дизайнер, шукаю підрядника*).\n"
        "3. Щойно знаходиться збіг — бот моментально пересилає вам ліда в 'Збережені повідомлення' або адмін-чат.\n"
        "4. Усі ліди автоматично зберігаються в Excel для зручної CRM-роботи.\n\n"
        "Це легальний та швидкий спосіб знаходити гарячих клієнтів раніше за конкурентів!"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "buy_script")
async def callback_buy_script(callback: CallbackQuery):
    text = (
        "💻 **Покупка скрипта ($50)**\n\n"
        "Ви отримаєте архів із повним вихідним кодом на Python (Telethon + Pandas), "
        "детальну інструкцію `README.md` щодо налаштування та запуску на вашому ПК або сервері.\n\n"
        f"Для оплати (USDT / Crypto / Карта) та отримання файлів, напишіть власнику: {OWNER_USERNAME}"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "buy_turnkey")
async def callback_buy_turnkey(callback: CallbackQuery):
    text = (
        "🚀 **Послуга 'Під Ключ' ($200)**\n\n"
        "Вам не потрібно знати програмування чи орендувати сервери. Ми зробимо все за вас!\n\n"
        "✅ Підбір релевантних чатів для вашої ніші.\n"
        "✅ Налаштування технічного акаунта Telegram.\n"
        "✅ Встановлення та запуск системи на нашому хмарному сервері (VPS) для роботи 24/7.\n"
        "✅ 1 місяць технічної підтримки та безкоштовної заміни ключових слів.\n\n"
        f"Готові масштабувати продажі? Напишіть мені для обговорення деталей: {OWNER_USERNAME}"
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
