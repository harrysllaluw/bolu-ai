import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# Ambil dua kunci dari Railway
KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2')
]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_groq_response(user_text):
    # Mencoba kunci satu per satu
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": user_text}]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Kunci bermasalah, coba kunci cadangan... Error: {e}")
            continue
    return "Waduh Bos Harry, semua kunci Groq lagi limit. Istirahat sejenak ya!"

@dp.message()
async def handle_chat(message: Message):
    if not message.text: return
    # Tampilkan reaksi "getik" di Telegram supaya bot kelihatan hidup
    await bot.send_chat_action(message.chat.id, "typing")
    response = get_groq_response(message.text)
    await message.answer(response)

async def main():
    # Menghapus antrean pesan lama supaya tidak Conflict
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 DUAL POWER SIAP! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
