import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# 1. AMBIL KUNCI
KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3')
]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_groq_response(user_text):
    for key in KEYS:
        if not key:
            continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                # GANTI KE MODEL TERBARU: llama3-8b-8192 -> llama-3.1-8b-instant
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Anda adalah Bolu, asisten profesional."},
                    {"role": "user", "content": user_text}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error kunci: {e}")
            continue
    return "Maaf Bos Harry, bensin habis. Coba lagi nanti."

@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return
    await bot.send_chat_action(message.chat.id, "typing")
    res = get_groq_response(message.text)
    await message.answer(res)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 AKTIF DENGAN MESIN BARU <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
