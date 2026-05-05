import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# Ambil semua kunci dari Railway
KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3')
]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_groq_response(user_text):
    # Mencoba satu per satu kunci jika terjadi error limit
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama3-8b-8192",  # Model ini lebih lancar untuk akun gratis
                messages=[{"role": "user", "content": user_text}]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Kunci bermasalah, pindah ke kunci berikutnya... Error: {e}")
            continue
    return "Waduh Bos Harry, semua 'bensin' (API Key) sudah habis. Coba lagi nanti ya!"

@dp.message()
async def handle_chat(message: Message):
    if not message.text: return
    await bot.send_chat_action(message.chat.id, "typing")
    response = get_groq_response(message.text)
    await message.answer(response)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 TRIPLE POWER AKTIF! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
