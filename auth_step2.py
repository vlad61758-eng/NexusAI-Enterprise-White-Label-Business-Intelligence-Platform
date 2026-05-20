import os
import sys
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

async def main(code):
    client = TelegramClient('hunter_session', API_ID, API_HASH)
    await client.connect()

    with open('phone_code_hash.txt', 'r') as f:
        phone_code_hash = f.read().strip()

    try:
        await client.sign_in(PHONE_NUMBER, code, phone_code_hash=phone_code_hash)
        print("Successfully logged in!")
    except Exception as e:
        print(f"Error logging in: {e}")

    await client.disconnect()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the code as an argument.")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
