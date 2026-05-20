import asyncio
import random
import os
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Список 50+ фріланс-каналів та чатів
CHANNELS_TO_JOIN = [
    "freelance_ua", "it_freelance_ua", "freelance", "upwork_ua", "freelance_ua_job",
    "freelance_ukraine", "ua_freelance", "work_it_ua", "it_jobs_ua", "junior_jobs_ua",
    "remote_job_ua", "freelancehunt_com", "freelance_chat_ua", "ua_job", "it_job_ukraine",
    "kiev_freelance", "freelance_kiev", "ua_freelancers", "it_freelance_chat", "ukraine_freelance",
    "freelance_top", "remote_it_ua", "design_freelance_ua", "copywriter_ua", "developer_ua",
    "freelance_job_ua", "it_vakansii_ua", "work_ua_remote", "freelance_bot_ua", "ua_remote",
    "freelance_market_ua", "it_recruiting_ua", "it_work_ua", "ua_it_jobs", "freelance_ua_chat",
    "it_jobs_ukraine", "remote_work_ua", "freelance_ua_vip", "ua_freelance_jobs", "it_freelance_ukraine",
    "freelance_ua_pro", "it_jobs_kiev", "remote_it_jobs_ua", "freelance_ua_top", "ua_it_freelance",
    "it_vakansii_ukraine", "freelance_ua_best", "it_work_ukraine", "ua_remote_jobs", "freelance_ua_online",
    "it_jobs_remote_ua", "remote_work_ukraine"
]

async def join_channels():
    if not API_ID or not API_HASH:
        print("Будь ласка, вкажіть API_ID та API_HASH у файлі .env.")
        return

    print("Підключення до Telegram...")
    client = TelegramClient('hunter_session', API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("Ви не авторизовані. Запустіть спочатку auth_step1.py та auth_step2.py")
        return

    print("Підключено! Починаємо підписку на канали...")

    successful_joins = 0
    for channel in CHANNELS_TO_JOIN:
        try:
            print(f"Спроба підписатися на {channel}...")
            await client(JoinChannelRequest(channel))
            print(f"✅ Успішно підписано на {channel}.")
            successful_joins += 1

            # Рандомний інтервал 20-40 секунд між підписками
            delay = random.randint(20, 40)
            print(f"Очікування {delay} секунд перед наступною підпискою...")
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            print(f"⚠️ Помилка FloodWait: Telegram просить почекати {e.seconds} секунд.")
            print("Чекаємо необхідний час...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Не вдалося підписатися на {channel} (можливо канал не існує): {e}")
            # Навіть при помилці робимо невелику паузу, щоб не спамити запитами
            await asyncio.sleep(5)

    print(f"Завершено підписку на канали. Успішно підписано на {successful_joins} каналів.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(join_channels())
