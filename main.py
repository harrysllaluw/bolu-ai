import os
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

# Mengambil kunci rahasia dari Railway Variables
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Setting Otak AI (Gemini)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# Setting Bot Telegram
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Fungsi buat database otomatis
async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY, 
            balance INT DEFAULT 0
        )
    ''')
    await conn.close()

# Logika Chat Bolu
@dp.message()
async def auto_chat(message: Message):
    if message.chat.type != 'private': return
    
    try:
        # Simpan user ke database
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING', message.from_user.id)
        await conn.close()
        
        # Bolu Mikir pakai Gemini
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer('Bolu lagi pusing, Bos... Coba chat lagi nanti ya.')

# Menjalankan mesin
async def main():
    await init_db()
    print(">>> BOLU SUDAH MELEK! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
