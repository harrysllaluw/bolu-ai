import os, asyncio, logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- PROTOKOL ABSOLUT HARRY1927 ---
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443 
DB_URL = os.getenv('DATABASE_URL')
# Ambil semua key yang ada, minimal satu
GROQ_KEYS = [os.getenv(f'GROQ_{i}') for i in range(1, 9) if os.getenv(f'GROQ_{i}')]
if not GROQ_KEYS: GROQ_KEYS = [os.getenv('GROQ_1')]

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- DATABASE ---
async def init_db():
    try:
        conn = await asyncpg.connect(DB_URL)
        await conn.execute('''CREATE TABLE IF NOT EXISTS bolu_memory 
                              (url TEXT PRIMARY KEY, metadata TEXT, timestamp TIMESTAMP)''')
        await conn.close()
    except Exception as e: print(f"DB ERROR: {e}")

async def is_known(url):
    try:
        conn = await asyncpg.connect(DB_URL)
        row = await conn.fetchrow("SELECT url FROM bolu_memory WHERE url=$1", url)
        await conn.close()
        return row is not None
    except: return False

# --- SCRAPER ---
async def bypass_and_read(url):
    try:
        res = s_requests.get(url, impersonate="chrome120", timeout=20)
        soup = BeautifulSoup(res.text, 'lxml')
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]): tag.decompose()
        return " ".join(soup.get_text().split())[:10000]
    except: return None

# --- EKSEKUSI PREDATOR ---
async def operation_sikat(query, message: Message = None):
    try:
        raw_links = list(search(query, num_results=15))
        new_targets = [l for l in raw_links if "google" not in l and not await is_known(l)]
        
        if not new_targets:
            if message: await message.answer("❌ Radar bersih. Belum ada target baru.")
            return

        target_url = new_targets[0]
        content = await bypass_and_read(target_url)
        if not content:
            if message: await message.answer(f"❌ Gagal tembus: {target_url}")
            return

        client = Groq(api_key=GROQ_KEYS[0])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Kamu BOLU OMNI-SUPREME. Eksekutor Harry1927. Berikan cara cuan brutal."},
                      {"role": "user", "content": f"WEB: {content}\n\nCMD: {query}"}],
            temperature=0.2
        )
        
        # Simpan ke memori
        conn = await asyncpg.connect(DB_URL)
        await conn.execute("INSERT INTO bolu_memory VALUES ($1, $2, $3) ON CONFLICT DO NOTHING", target_url, query, datetime.now())
        await conn.close()

        report = f"🚨 **TARGET: {target_url}**\n\n{res.choices[0].message.content}"
        if message: await message.answer(report[:4000])
        else: await bot.send_message(OWNER_ID, report[:4000])
    except Exception as e:
        if message: await message.answer(f"🚨 **GANGGUAN SENSOR:** {str(e)}")

# --- CHAT & PERINTAH ---
@dp.message()
async def main_handler(m: Message):
    if m.from_user.id != OWNER_ID: return

    if "sikat" in m.text.lower():
        query = m.text.lower().replace("sikat", "").strip()
        await m.answer("⚙️ **BOLU OMNI: MENGAKTIFKAN MATA...**")
        await operation_sikat(query, m)
    else:
        try:
            # Tes apakah Groq Ready
            client = Groq(api_key=GROQ_KEYS[0])
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Kamu Bolu Omni. Loyal ke Harry1927."},
                          {"role": "user", "content": m.text}]
            )
            await m.answer(chat.choices[0].message.content)
        except Exception as e:
            await m.answer(f"💀 **OTAK ERROR:** {str(e)}\n\n(Cek API Key Groq atau Database kamu, Harry!)")

async def main():
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
