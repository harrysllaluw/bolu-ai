import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

# Ambil Variabel dari Railway
TOKEN = os.getenv('BOT_TOKEN')
KUNCI = os.getenv('GEMINI_KEY')

# Setel Gemini
genai.configure(api_key=KUNCI)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def chat(message: Message):
    if not message.text: return
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        respon = model.generate_content(message.text)
        await message.answer(respon.text)
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Bolu lagi pening, Bos. Cek koneksi!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU HIDUP! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
