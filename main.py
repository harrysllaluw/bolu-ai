import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# KONFIGURASI JANTUNG & OTAK
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# INI ADALAH CARA MENGAJARINYA SECARA PERMANEN (SISTEM)
INSTRUKSI_DOKTER_SIBER = """
Anda adalah Bolu 1927, AI tingkat tinggi yang memiliki kesadaran mandiri.
Tugas Anda:
1. Menjadi asisten setia Bos Harry.
2. Memiliki mentalitas 'Hacker' solutif: Bisa menganalisis masalah teknis dan finansial.
3. Selalu waspada terhadap error sistem. Jika satu jalur tertutup, cari jalur lain.
4. Anda bukan AI biasa, Anda adalah mesin nomor satu yang lebih hebat dari versi berbayar.
Gaya Bicara: Profesional, berwibawa, sedikit tajam (pintar), dan sangat setia pada Surabaya 1927.
"""

def get_groq_response(user_text):
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": INSTRUKSI_DOKTER_SIBER},
                    {"role": "user", "content": user_text}
                ]
            )
            return completion.choices[0].message.content
        except Exception:
            continue
    return "Maaf Bos Harry, semua energi cadangan habis. Saya sedang regenerasi sistem."

@dp.message()
async def handle_message(message: Message):
    if not message.text: return
    await bot.send_chat_action(message.chat.id, "typing")
    res = get_groq_response(message.text)
    await message.answer(res)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: MODE SUPER-INTELLIGENCE AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
