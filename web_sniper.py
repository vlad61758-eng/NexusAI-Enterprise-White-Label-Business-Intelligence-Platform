import asyncio
import os
import re
import html
from playwright.async_api import async_playwright
import google.generativeai as genai
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ADMIN_ID = os.getenv('ADMIN_ID', '8386760144')

# Налаштування Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Бот для сповіщень
tg_bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

CHANNELS_TO_MONITOR = [
    "freelance_ua", "it_freelance_ua", "upwork_ua"
]

def is_potential_task(text):
    text_lower = text.lower()
    keywords = ['$', 'usd', 'долар', 'грн', 'uah', 'бюджет', 'оплата', 'ціна']
    return any(keyword in text_lower for keyword in keywords)

async def analyze_and_notify(text, channel_name):
    prompt = f"""
    Проаналізуй це завдання з фріланс-каналу: "{text}".

    Твоє завдання - визначити:
    1. Чи вказана ціна або бюджет? Якщо так, чи дорівнює вона або більше 50 доларів (або еквівалент ~2000 грн)?
    2. Чи є завдання відносно нескладним?

    Якщо ОБИДВІ умови виконуються:
    Напиши "ТАК" в першому рядку.
    Потім напиши короткий аналіз.
    В кінці напиши готовий драфт повідомлення замовнику.

    Якщо хоча б одна умова НЕ виконується:
    Напиши "НІ" в першому рядку.
    """
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        response_text = response.text.strip()

        if response_text.startswith("ТАК"):
            safe_text = html.escape(text[:500])
            safe_analysis = html.escape(response_text[3:].strip())
            admin_msg = (
                f"🎯 <b>Знайдено нове завдання (Web Sniper)!</b>\n"
                f"📢 <b>Канал:</b> {html.escape(channel_name)}\n\n"
                f"📝 <b>Оригінал:</b>\n<i>{safe_text}...</i>\n\n"
                f"🤖 <b>Аналіз та Драфт:</b>\n{safe_analysis}"
            )
            if tg_bot:
                await tg_bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")
            print(f"\n[УСПІХ] Знайдено та надіслано ідеальне завдання з {channel_name}!\n")
    except Exception as e:
        print(f"Помилка ШІ: {e}")

async def run_sniper():
    async with async_playwright() as p:
        # Зберігаємо сесію, щоб не логінитись щоразу
        user_data_dir = "./tg_web_session"
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, # True для прихованого режиму, але краще бачити що відбувається
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = await browser.new_page()
        await page.goto("https://web.telegram.org/a/")

        print("\n" + "="*50)
        print("Будь ласка, залогіньтеся в Telegram Web (відскануйте QR або введіть номер).")
        print("Після авторизації скрипт сам почне роботу через 30 секунд...")
        print("="*50 + "\n")

        # Чекаємо поки ви увійдете
        await asyncio.sleep(30)
        print("Починаємо моніторинг!")

        seen_messages = set()

        while True:
            for channel in CHANNELS_TO_MONITOR:
                try:
                    # Переходимо на канал
                    await page.goto(f"https://web.telegram.org/a/#{channel}")
                    await asyncio.sleep(5) # Чекаємо завантаження

                    # Шукаємо повідомлення. Селектор для версії Web A
                    messages = await page.query_selector_all(".message")
                    if not messages:
                        continue

                    # Беремо останні 5 повідомлень
                    for msg in messages[-5:]:
                        text_element = await msg.query_selector(".text-content")
                        if text_element:
                            text = await text_element.inner_text()
                            msg_id = text[:50] # Хеш для унікальності

                            if msg_id not in seen_messages:
                                seen_messages.add(msg_id)
                                if is_potential_task(text):
                                    print(f"Перевірка повідомлення з {channel}...")
                                    asyncio.create_task(analyze_and_notify(text, channel))

                except Exception as e:
                    print(f"Помилка при перевірці {channel}: {e}")

            await asyncio.sleep(20) # Пауза перед наступним колом

if __name__ == "__main__":
    asyncio.run(run_sniper())
