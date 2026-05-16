import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
import urllib.request
import json
import requests

# Встановлення рівня логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Визначаємо стани (FSM) для запам'ятовування контексту розмови
class WeatherForm(StatesGroup):
    waiting_for_city = State()

def get_exchange_rates():
    """Функція для отримання курсу валют та крипти."""
    fiat_url = "https://open.er-api.com/v6/latest/USD"
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    try:
        # Отримуємо фіатні курси
        req = urllib.request.urlopen(fiat_url)
        data = json.loads(req.read().decode('utf-8'))
        rates = data.get('rates', {})

        uah_rate = rates.get('UAH')
        eur_rate = rates.get('EUR')
        gbp_rate = rates.get('GBP')

        # Отримуємо курс Bitcoin
        btc_req = requests.get(crypto_url, timeout=5)
        btc_data = btc_req.json()
        btc_usd = btc_data.get('bitcoin', {}).get('usd', 0)

        if not uah_rate:
            return "❌ Не вдалося отримати курс фіатних валют."

        result = (
            "📊 <b>Актуальний курс валют:</b>\n\n"
            f"💵 1 USD = {uah_rate:.2f} UAH\n"
            f"💶 1 EUR = {(uah_rate/eur_rate):.2f} UAH\n"
            f"💷 1 GBP = {(uah_rate/gbp_rate):.2f} UAH\n"
            f"💰 1 BTC = {btc_usd:,.0f} USD"
        )
        return result
    except Exception as e:
        return f"❌ Помилка при отриманні даних: {e}"

def get_weather(city: str):
    """Отримує погоду за допомогою wttr.in"""
    try:
        # m = метрична система (градуси Цельсія), format = кастомний формат
        url = f"https://wttr.in/{city}?format=%l:+%c+%t,+%w&m"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "Unknown location" not in response.text:
            return f"🌤 <b>Погода:</b>\n{response.text.strip()}"
        else:
            return f"❌ Не вдалося знайти місто: <b>{city}</b>"
    except Exception as e:
        return f"❌ Помилка сервісу погоди."

def get_main_keyboard():
    """Створює клавіатуру з кнопками під повідомленням (Inline)"""
    builder = InlineKeyboardBuilder()
    builder.button(text="💱 Курс валют", callback_data="action_rates")
    builder.button(text="🌤 Погода", callback_data="action_weather")
    builder.button(text="🎲 Кинути кубик", callback_data="action_dice")
    # Розміщуємо кнопки: 2 в першому ряду, 1 в другому
    builder.adjust(2, 1)
    return builder.as_markup()

# Обробник команди /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # Скидаємо стан, якщо він був

    welcome_text = (
        f"Привіт, {message.from_user.first_name}! 👋\n\n"
        "Я просунутий бот, створений Jules.\n"
        "Тепер я вмію набагато більше! Використовуй меню нижче, щоб перевірити мої функції:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# --- Обробка натискань на кнопки ---

@dp.callback_query(F.data == "action_rates")
async def process_rates_button(callback: types.CallbackQuery):
    await callback.answer("Завантажую курси...", show_alert=False) # Спливаюче повідомлення
    rates_text = get_exchange_rates()
    # Редагуємо повідомлення, залишаючи кнопки
    await callback.message.edit_text(rates_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@dp.callback_query(F.data == "action_dice")
async def process_dice_button(callback: types.CallbackQuery):
    await callback.answer()
    # Відправляємо інтерактивний кубик (анімація Telegram)
    await callback.message.answer_dice(emoji="🎲")
    # Після цього знову показуємо меню
    await callback.message.answer("Ось твоє меню:", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "action_weather")
async def process_weather_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    # Просимо користувача ввести місто і переводимо бота в стан очікування вводу
    await callback.message.answer("✍️ Напиши назву міста, щоб дізнатися погоду (наприклад: <i>Kyiv</i>, <i>Lviv</i>, <i>London</i>):", parse_mode="HTML")
    await state.set_state(WeatherForm.waiting_for_city)

# --- Обробка вводу міста (FSM) ---

@dp.message(WeatherForm.waiting_for_city)
async def process_city_input(message: types.Message, state: FSMContext):
    city_name = message.text

    # Показуємо статус "Набирає повідомлення..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    weather_info = get_weather(city_name)

    await message.answer(weather_info, reply_markup=get_main_keyboard(), parse_mode="HTML")

    # Виходимо зі стану
    await state.clear()

# Обробник будь-якого іншого тексту (якщо бот не в стані очікування міста)
@dp.message(StateFilter(None))
async def echo_message(message: types.Message):
    await message.answer(
        "Я тебе не зовсім зрозумів. 🤷‍♂️\nСкористайся кнопками нижче:",
        reply_markup=get_main_keyboard()
    )

async def main():
    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Помилка при запуску бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
