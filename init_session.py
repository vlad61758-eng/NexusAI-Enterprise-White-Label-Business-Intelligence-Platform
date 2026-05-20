import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

async def main():
    if not API_ID or not API_HASH:
        print("Помилка: API_ID та API_HASH не знайдені у файлі .env")
        return

    print("Ініціалізація сесії Telegram...")
    # Створюємо сесію, якщо вона ще не створена.
    # Це синхронно запитає номер телефону та код підтвердження.
    client = TelegramClient('hunter_session', int(API_ID), API_HASH)
    await client.start()
    print("Сесію успішно створено та збережено в 'hunter_session.session'!")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
