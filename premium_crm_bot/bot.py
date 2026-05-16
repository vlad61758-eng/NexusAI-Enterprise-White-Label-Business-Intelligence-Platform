import asyncio
import logging
import os
import aiosqlite
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Завантаження змінних оточення
load_dotenv('config.env')
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    logging.warning("BOT_TOKEN is not set in config.env!")

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обробники
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обробник команди /start. Показує головне меню."""
    # Реєстрація клієнта
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT OR IGNORE INTO clients (user_id, username, full_name) VALUES (?, ?, ?)',
            (message.from_user.id, message.from_user.username, message.from_user.full_name)
        )
        await db.commit()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог товарів", callback_data="show_catalog")],
        [InlineKeyboardButton(text="👤 Мій профіль", callback_data="my_profile")]
    ])

    await message.answer(
        f"Привіт, {message.from_user.first_name}! 👋\n\n"
        "Ласкаво просимо до нашого магазину. Оберіть пункт меню нижче:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "show_catalog")
async def process_show_catalog(callback: types.CallbackQuery):
    """Показує список товарів з БД."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT id, name, price FROM products') as cursor:
            products = await cursor.fetchall()

    if not products:
        await callback.message.answer("Каталог поки порожній 😔")
        await callback.answer()
        return

    keyboard_builder = []
    for prod_id, name, price in products:
        keyboard_builder.append(
            [InlineKeyboardButton(text=f"{name} — ${price:.2f}", callback_data=f"buy_{prod_id}")]
        )

    # Кнопка повернення
    keyboard_builder.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_builder)

    await callback.message.edit_text(
        "🛍 <b>Каталог товарів:</b>\nОберіть те, що вас цікавить:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: types.CallbackQuery):
    """Повертає в головне меню."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог товарів", callback_data="show_catalog")],
        [InlineKeyboardButton(text="👤 Мій профіль", callback_data="my_profile")]
    ])

    await callback.message.edit_text(
        "Головне меню. Оберіть пункт:",
        reply_markup=keyboard
    )
    await callback.answer()

# --- FSM для оформлення замовлення ---
class OrderForm(StatesGroup):
    waiting_for_phone = State()

@dp.callback_query(F.data.startswith("buy_"))
async def process_buy_product(callback: types.CallbackQuery, state: FSMContext):
    """Обробка натискання на товар."""
    product_id = int(callback.data.split("_")[1])

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT name, price, description FROM products WHERE id = ?', (product_id,)) as cursor:
            product = await cursor.fetchone()

    if product:
        name, price, desc = product
        # Зберігаємо вибраний товар в стан FSM
        await state.update_data(product_id=product_id, product_name=name, price=price)

        await callback.message.answer(
            f"🛒 Ви обрали:\n<b>{name}</b>\nОпис: {desc}\nЦіна: ${price:.2f}\n\n"
            "📞 Щоб оформити замовлення, будь ласка, надішліть ваш <b>номер телефону</b>:",
            parse_mode="HTML"
        )
        await state.set_state(OrderForm.waiting_for_phone)
    await callback.answer()

@dp.message(OrderForm.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    """Отримання телефону і збереження замовлення."""
    phone = message.text
    user_data = await state.get_data()
    product_id = user_data['product_id']
    product_name = user_data['product_name']
    price = user_data['price']
    user_id = message.from_user.id

    # Оновлюємо телефон клієнта в БД та створюємо замовлення
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE clients SET phone = ? WHERE user_id = ?', (phone, user_id))
        await db.execute('INSERT INTO orders (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
        await db.commit()

    await message.answer(
        "✅ <b>Замовлення успішно оформлено!</b>\n"
        "Наш менеджер зв'яжеться з вами найближчим часом.",
        parse_mode="HTML"
    )

    # Сповіщення адміністратору
    if ADMIN_ID and ADMIN_ID != "YOUR_ADMIN_ID_HERE":
        admin_text = (
            "🚨 <b>Нове замовлення!</b>\n\n"
            f"👤 Клієнт: @{message.from_user.username} (ID: {user_id})\n"
            f"📞 Телефон: <code>{phone}</code>\n\n"
            f"📦 Товар: <b>{product_name}</b>\n"
            f"💰 Сума: ${price:.2f}"
        )
        try:
            await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Не вдалося відправити сповіщення адміну: {e}")

    await state.clear()

# Налаштування БД
DB_PATH = 'crm_database.db'

async def init_db():
    """Ініціалізація бази даних та створення таблиць, якщо їх немає."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблиця товарів
        await db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL
            )
        ''')
        # Таблиця клієнтів
        await db.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                phone TEXT
            )
        ''')
        # Таблиця замовлень
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                status TEXT DEFAULT 'Нове',
                FOREIGN KEY (user_id) REFERENCES clients (user_id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Додавання тестових товарів, якщо таблиця порожня
        cursor = await db.execute('SELECT COUNT(*) FROM products')
        count = await cursor.fetchone()
        if count[0] == 0:
            test_products = [
                ('🚀 VIP Консультація', 'Годинна сесія з експертом', 50.0),
                ('📚 Доступ до закритої групи', 'Місячна підписка на ексклюзивний контент', 30.0),
                ('📦 Базовий пакет послуг', 'Стандартний набір послуг для старту', 15.0)
            ]
            await db.executemany('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', test_products)

        await db.commit()
    logging.info("База даних успішно ініціалізована.")

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting bot...")

    await init_db()

    try:
        if BOT_TOKEN and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
            await dp.start_polling(bot)
        else:
            logging.error("Бот не запущено через відсутність токена. Встановіть BOT_TOKEN у config.env.")
    except Exception as e:
        logging.error(f"Критична помилка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
