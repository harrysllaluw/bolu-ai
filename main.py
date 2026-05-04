import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

# AMBIL VARIABEL (Harus pas dengan nama di Railway!)
TOKEN = os.getenv('BOT_TOKEN')
KUNCI = os.getenv('GEMINI_KEY')

# Konfigurasi AI
genai.configure(api_key=KUNCI)

# Inisialisasi Bot
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Bolu lagi pening, Bos. Cek log atau kunci Gemini!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU SIAP TEMPUR! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
