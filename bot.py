from telethon import TelegramClient
import asyncio
import os

api_id = 21627756
api_hash = 'fe77fbf0cae9f7f5ece37659e2466cf1'

source_channel = 'https://t.me/+W_8GQgEVa5s0OWYy'
target_channel = 'https://t.me/jdfhvcghj'

client = TelegramClient('session', api_id, api_hash)

async def main():
    await client.start()

    source = await client.get_entity(source_channel)

    print('تم جلب القناة')

    async for msg in client.iter_messages(source, reverse=True):

        try:
            # فقط صور وفيديو
            if msg.photo or msg.video or msg.document:

                file_path = await msg.download_media()

                if file_path:
                    await client.send_file(
                        target_channel,
                        file_path,
                        caption=msg.text or ''
                    )

                    print(f'تم رفع الوسائط {msg.id}')

                    os.remove(file_path)

        except Exception as e:
            print(f'خطأ: {e}')

asyncio.run(main())