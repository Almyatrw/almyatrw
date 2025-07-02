import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from yt_dlp import YoutubeDL
import subprocess

# إعدادات البوت
API_TOKEN = "7807447404:AAEnXi1PcSgFu3kboOOzdCw3zCA1v7zyRw"
CHANNEL_ID = "-1002130159681"  # هذا هو ID الحقيقي للقناة المرتبط بالرابط الذي أعطيتني إياه

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# إعدادات التحميل
YDL_OPTIONS = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "downloaded.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}

async def download_and_send(url):
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إذا الفيديو حجمه كبير نضغطه
        if os.path.getsize(filename) > 48 * 1024 * 1024:
            compressed = "compressed.mp4"
            subprocess.run([
                "ffmpeg", "-i", filename, "-vcodec", "libx264",
                "-crf", "28", "-preset", "veryfast", compressed
            ])
            os.remove(filename)
            filename = compressed

        # إرسال الفيديو للقناة
        await bot.send_video(CHANNEL_ID, types.FSInputFile(filename), caption="🎥 تم التحميل من تويتر")
        os.remove(filename)
    except Exception as e:
        logging.error(f"خطأ في التحميل: {e}")

@dp.message()
async def handle_message(message: types.Message):
    if "twitter.com" in message.text or "x.com" in message.text:
        await message.reply("⏬ جاري التحميل وإرساله للقناة...")
        await download_and_send(message.text)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
