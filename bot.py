
from telethon import TelegramClient
import asyncio
import os

# الإعدادات
api_id = 21627756
api_hash = 'fe77fbf0cae9f7f5ece37659e2466cf1'

source_channel = 'https://t.me/+W_8GQgEVa5s0OWYy'
target_channel = 'https://t.me/jdfhvcghj'


start_message_id = 356

client = TelegramClient('session', api_id, api_hash)

async def main():
    await client.start()

    # جلب القنوات
    source = await client.get_entity(source_channel)
    target = await client.get_entity(target_channel)

    print(f'تم جلب القناة، سأبدأ من الرسالة رقم {start_message_id}')

    count = 0

    # جلب الرسائل من start_message_id وطالع
    async for msg in client.iter_messages(
        source,
        min_id=start_message_id - 1,
        reverse=True
    ):

        if msg.id < start_message_id:
            continue

        try:
            # إذا تحتوي وسائط
            if msg.photo or msg.video or msg.document:

                print(f'جاري تحميل الرسالة {msg.id}...')

                file_path = await msg.download_media()

                if file_path:

                    await client.send_file(
                        target,
                        file_path,
                        caption=msg.text or ''
                    )

                    count += 1

                    print(f'✅ تم نقل الرسالة {msg.id} | العدد الكلي: {count}')

                    # حذف الملف بعد الإرسال
                    if os.path.exists(file_path):
                        os.remove(file_path)

                else:
                    print(f'⚠️ فشل تحميل الوسائط من الرسالة {msg.id}')

            else:
                # إذا رسالة نصية فقط
                if msg.text:
                    await client.send_message(
                        target,
                        msg.text
                    )

                    count += 1

                    print(f'✅ تم نقل رسالة نصية {msg.id} | العدد الكلي: {count}')

                else:
                    print(f'⏭️ تم تخطي الرسالة {msg.id}')

        except Exception as e:
            print(f'❌ خطأ في الرسالة {msg.id}: {e}')
            continue

    print(f'\n✨ انتهى النقل بنجاح! تم نقل {count} رسالة/ملف')

# تشغيل السكربت
asyncio.run(main())
