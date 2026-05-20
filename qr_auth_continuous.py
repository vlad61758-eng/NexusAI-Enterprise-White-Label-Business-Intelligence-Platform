import os
import asyncio
import qrcode
import io
import time
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

async def main():
    client = TelegramClient('hunter_session', API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        while True:
            try:
                qr_login = await client.qr_login()
                qr = qrcode.QRCode(version=1, box_size=1, border=1)
                qr.add_data(qr_login.url)
                qr.make(fit=True)

                f = io.StringIO()
                qr.print_ascii(out=f)
                f.seek(0)

                with open('qr_code.txt', 'w') as out_file:
                    out_file.write(f.read())

                print(f"QR generated at {time.strftime('%X')}. Waiting for scan...")
                await qr_login.wait(timeout=20)
                print("Successfully logged in via QR Code!")
                break
            except asyncio.TimeoutError:
                print("Timeout. Regenerating QR...")
                continue
            except Exception as e:
                print(f"Failed to login: {e}")
                break
    else:
        print("Already authorized!")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
