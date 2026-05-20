import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

async def main():
    client = TelegramClient('hunter_session', API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        res = await client.send_code_request(PHONE_NUMBER)
        print(f"Code requested. phone_code_hash: {res.phone_code_hash}")
        # Збережемо phone_code_hash у файл, щоб step2 міг його використати
        with open('phone_code_hash.txt', 'w') as f:
            f.write(res.phone_code_hash)
    else:
        print("Already authorized!")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
