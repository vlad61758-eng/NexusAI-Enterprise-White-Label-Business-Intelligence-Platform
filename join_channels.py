import asyncio
import random
import os
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Приклад списку каналів. Заповніть вашими цільовими каналами фрілансу (50 штук)
CHANNELS_TO_JOIN = [
    "freelance", "upwork_ua", "freelance_ua_job", "it_freelance_ua",
    # Додайте інші посилання або юзернейми сюди
]

async def join_channels():
    if not API_ID or not API_HASH:
        print("Будь ласка, вкажіть API_ID та API_HASH у файлі .env.")
        return

    print("Підключення до Telegram...")
    client = TelegramClient('hunter_session', int(API_ID), API_HASH)
    await client.start()

    print("Підключено! Починаємо підписку на канали...")

    for channel in CHANNELS_TO_JOIN:
        try:
            print(f"Спроба підписатися на {channel}...")
            await client(JoinChannelRequest(channel))
            print(f"Успішно підписано на {channel}.")

            # Рандомний інтервал 20-40 секунд між підписками
            delay = random.randint(20, 40)
            print(f"Очікування {delay} секунд перед наступною підпискою...")
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            print(f"Помилка FloodWait: потрібно почекати {e.seconds} секунд.")
            print("Чекаємо необхідний час...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Не вдалося підписатися на {channel}: {e}")

    print("Завершено підписку на канали.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(join_channels())
