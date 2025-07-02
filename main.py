import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from yt_dlp import YoutubeDL
import subprocess

TOKEN = "7807447404:AAEnXi1PcSgFu3kboOOzdCw3ZyCA1v7zyRw"
CHANNEL_ID = "@aljoker60"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

YDL_OPTS = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "video.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}

async def download_and_send(url):
    try:
        with YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.getsize(filename) > 48 * 1024 * 1024:
            compressed = "compressed.mp4"
            subprocess.run([
                "ffmpeg", "-i", filename, "-vcodec", "libx264",
                "-crf", "28", "-preset", "veryfast", compressed
            ])
            os.remove(filename)
            filename = compressed

        await bot.send_video(CHANNEL_ID, types.FSInputFile(filename), caption="🎥 تم التحميل بنجاح")
        os.remove(filename)
    except Exception as e:
        logging.error(str(e))

@dp.message()
async def handle_message(message: types.Message):
    if "x.com" in message.text or "twitter.com" in message.text:
        await message.reply("⏬ جاري التحميل...")
        await download_and_send(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
