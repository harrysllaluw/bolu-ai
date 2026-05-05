import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, exceptions
from aiogram.types import Message
from groq import Groq

# 1. KONFIGURASI KUNCI
KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3')
]
TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_groq_response(user_text):
    for i, key in enumerate(KEYS):
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[
                    {"role": "system", "content": "Anda adalah Bolu, asisten cerdas yang profesional, tenang, dan solutif. Gunakan bahasa Indonesia."},
                    {"role": "user", "content": user_text}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Kunci {i+1} Gagal: {e}")
            continue
            
    return "Maaf Bos Harry, semua sistem sedang penuh. Mohon tunggu sebentar."

@dp.message()
async def handle_chat(message: Message):
    if not message.text: return
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = get_groq_response(message.text)
        await message.answer(response)
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
