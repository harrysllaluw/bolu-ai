import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

# Ambil Variables
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# Konfigurasi AI - Cara Panggil Paling Aman
genai.configure(api_key=GEMINI_KEY)

# Pakai model 'gemini-pro' dengan penanganan error manual
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def chat_handler(message: Message):
    if not message.text: return
    try:
        # Panggil AI tanpa ribet
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message.text)
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Bolu paham, tapi bingung mau jawab apa...")
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Bolu lagi meditasi sebentar, coba chat lagi ya Bos!")

async def main():
    # Hapus Webhook lama agar tidak bentrok (PENTING!)
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU SUDAH MELEK & SIAP TEMPUR! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
