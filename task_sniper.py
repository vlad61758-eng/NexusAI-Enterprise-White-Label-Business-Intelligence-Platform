import asyncio
import os
import re
import html
import google.generativeai as genai
from telethon import TelegramClient, events
from dotenv import load_dotenv

# aiogram для відправки результатів адміну
from aiogram import Bot

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ADMIN_ID = os.getenv('ADMIN_ID')

if not all([API_ID, API_HASH, BOT_TOKEN, GEMINI_API_KEY, ADMIN_ID]):
    print("Будь ласка, переконайтеся, що всі змінні в .env задані!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

tg_bot = Bot(token=BOT_TOKEN)

# Можна задати ID або юзернейми каналів для моніторингу
# Якщо пустий список, Telethon буде слухати всі канали, на які підписаний
CHANNELS_TO_MONITOR = [
    # 'freelance', 'upwork_ua'
]

client = TelegramClient('hunter_session', int(API_ID), API_HASH)

def is_potential_task(text):
    # Попередня дуже груба фільтрація на наявність $ або гривень чи слова ціна
    text_lower = text.lower()
    keywords = ['$', 'usd', 'долар', 'грн', 'uah', 'бюджет', 'оплата', 'ціна']
    return any(keyword in text_lower for keyword in keywords)

async def analyze_task_with_gemini(text, channel_name, msg_link):
    prompt = f"""
    Проаналізуй це завдання з фріланс-каналу: "{text}".

    Твоє завдання - визначити:
    1. Чи вказана ціна або бюджет? Якщо так, чи дорівнює вона або більше 50 доларів (або еквівалент в іншій валюті, наприклад ~2000 грн)?
    2. Чи є завдання відносно нескладним (не потребує місяців розробки, можна виконати за кілька годин або днів)?

    Якщо ОБИДВІ умови виконуються (ціна >= 50$ І завдання нескладне):
    Напиши "ТАК" в першому рядку.
    Потім напиши короткий аналіз завдання.
    В кінці напиши готовий драфт повідомлення замовнику (привітання, інтерес, чому ти підходиш для цього).

    Якщо хоча б одна умова НЕ виконується:
    Напиши "НІ" в першому рядку.
    """

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        response_text = response.text.strip()

        if response_text.startswith("ТАК"):
            # Екрануємо текст, щоб уникнути помилок Telegram HTML parse
            safe_text = html.escape(text[:500])
            safe_analysis = html.escape(response_text[3:].strip())

            # Формуємо повідомлення для адміна
            admin_msg = (
                f"🎯 <b>Знайдено нове завдання!</b>\n"
                f"📢 <b>Канал:</b> {html.escape(channel_name)}\n"
                f"🔗 <b>Посилання:</b> {msg_link}\n\n"
                f"📝 <b>Оригінал:</b>\n<i>{safe_text}...</i>\n\n"
                f"🤖 <b>Аналіз та Драфт відповіді:</b>\n{safe_analysis}"
            )

            await tg_bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")
            print(f"Відправлено завдання адміну з каналу {channel_name}")

    except Exception as e:
        print(f"Помилка при роботі з Gemini або відправці повідомлення: {e}")


@client.on(events.NewMessage(chats=CHANNELS_TO_MONITOR if CHANNELS_TO_MONITOR else None))
async def handler(event):
    if event.is_channel:
        chat = await event.get_chat()
        channel_name = chat.title or chat.username or "Невідомий канал"

        # Формуємо посилання на повідомлення (працює якщо канал публічний)
        msg_link = f"https://t.me/{chat.username}/{event.id}" if chat.username else f"Повідомлення ID: {event.id}"

        text = event.message.message

        if text and is_potential_task(text):
            print(f"Знайдено потенційне завдання в {channel_name}. Аналізуємо...")
            # Запускаємо аналіз у фоні, щоб не блокувати отримання нових повідомлень
            asyncio.create_task(analyze_task_with_gemini(text, channel_name, msg_link))

async def main():
    print("Запуск Smart Sniper...")
    await client.start()
    print("Моніторинг каналів увімкнено. Очікування нових завдань...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
