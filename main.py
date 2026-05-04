import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import google.generativeai as genai

# Ambil Variabel dari Railway
TOKEN = os.getenv('TOKEN_BOT')
KUNCI_GEMINI = os.getenv('KUNCI_GEMINI')

# Konfigurasi AI
genai.configure(api_key=KUNCI_GEMINI)

# Inisialisasi Bot
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_chat(message: Message):
    if not message.text:
        return
    
    try:
        # Panggil AI Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message.text)
        
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Bolu paham, tapi bingung mau jawab apa.")
            
    except Exception as e:
        print(f"Kesalahan: {e}")
        await message.answer("Bolu lagi merenung sebentar, coba ngobrol lagi nanti ya.")

async def main():
    # Hapus Webhook lama agar tidak bertabrakan
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU SUDAH MELEK & SIAP TEMPUR! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
