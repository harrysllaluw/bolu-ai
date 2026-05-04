import os
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

# Ambil Variables
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Perbaikan format DATABASE_URL untuk Railway
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Pakai model terbaru

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def init_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY, 
                balance INT DEFAULT 0
            )
        ''')
        await conn.close()
        print("Database Aman!")
    except Exception as e:
        print(f"Gagal konek database: {e}")

@dp.message()
async def auto_chat(message: Message):
    if not message.text: return
    try:
        # Bolu Mikir
        response = model.generate_content(message.text)
        await message.answer(response.text)
        
        # Simpan user secara background biar gak lambat
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING', message.from_user.id)
        await conn.close()
    except Exception as e:
        print(f"Error Chat: {e}")
        await message.answer('Bolu lagi pusing, Bos... Coba cek log di Railway.')

async def main():
    await init_db()
    print(">>> BOLU SIAP TEMPUR! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
