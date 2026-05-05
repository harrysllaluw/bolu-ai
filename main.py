import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, exceptions
from aiogram.types import Message
from groq import Groq

# 1. KONFIGURASI IDENTITAS & KUNCI
KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3')
]
TOKEN = os.getenv('BOT_TOKEN')

# Sistem Log untuk memantau kesehatan bot
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_groq_response(user_text):
    """Sistem Dokter: Mencoba setiap kunci dengan tenang sampai berhasil"""
    for i, key in enumerate(KEYS):
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[
                    # Instruksi Karakter: Dokter Profesional & Cerdas
                    {"role": "system", "content": "Anda adalah Bolu, asisten cerdas dengan gaya bicara profesional, tenang, dan solutif seperti seorang ahli. Gunakan bahasa Indonesia yang baik."},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Kunci {i+1} Gagal: {e}")
            continue # Lanjut ke kunci cadangan
            
    return "Mohon maaf Bos Harry, saat ini semua sistem cadangan saya sedang penuh. Saya akan segera kembali aktif setelah masa pemulihan singkat."

@dp.message()
async def handle_chat(message: Message):
    if not message.text: return
    
    # Efek visual: Mengetik...
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = get_groq_response(message.text)
        await message.answer(response)
    except exceptions.TelegramRetryAfter as e:
        # Jika Telegram limit, tunggu sebentar lalu kirim lagi
        await asyncio.sleep(e.retry_after)
        await message.answer(get_groq_response(message.text))
    except Exception as e:
        logging.error(f"Masalah tak terduga: {e}")

async def main():
    """Sistem Utama: Membersihkan sisa-sisa 'hantu' sebelum mulai"""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print(">>> BOLU 1927: SISTEM DOKTER PROFESIONAL AKTIF! <<<")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Gagal memulai sistem: {e}")

if __name__ == '__main__':
    asyncio.run(main())
