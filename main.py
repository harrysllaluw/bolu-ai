import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fake_useragent import UserAgent

# --- PROTOKOL KEDAULATAN MUTLAK HARRY1927 ---
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443 
DB_URL = os.getenv('DATABASE_URL')
ua = UserAgent()

# Mengambil semua key Groq yang tersedia (1-8)
GROQ_KEYS = [os.getenv(f'GROQ_{i}') for i in range(1, 9) if os.getenv(f'GROQ_{i}')]
if not GROQ_KEYS:
    GROQ_KEYS = [os.getenv('GROQ_1')] # Fallback jika hanya ada 1 key

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- [INGATAN ABADI] DATABASE ENGINE ---
async def init_db():
    try:
        conn = await asyncpg.connect(DB_URL)
        await conn.execute('''CREATE TABLE IF NOT EXISTS bolu_memory 
                              (url TEXT PRIMARY KEY, metadata TEXT, timestamp TIMESTAMP)''')
        await conn.close()
    except Exception as e:
        print(f"CRITICAL DB ERROR: {e}")

async def is_known(url):
    try:
        conn = await asyncpg.connect(DB_URL)
        row = await conn.fetchrow("SELECT url FROM bolu_memory WHERE url=$1", url)
        await conn.close()
        return row is not None
    except:
        return False

# --- [MATA PREDATOR] BYPASS & SCRAPE ---
async def bypass_and_read(url):
    try:
        header = {"User-Agent": ua.random}
        res = s_requests.get(url, impersonate="chrome120", headers=header, timeout=25)
        soup = BeautifulSoup(res.text, 'lxml')
        for s in soup(["script", "style", "header", "footer", "nav", "aside"]): s.decompose()
        return " ".join(soup.get_text().split())[:12000]
    except:
        return None

# --- [OTAK] ANALISIS PARALLEL ---
async def analyze_task(key, query, context, acc_no):
    try:
        client = Groq(api_key=key)
        sys_msg = (f"IDENTITAS: BOLU OMNI-SUPREME. EKSEKUTOR: HARRY1927. "
                   f"AKUN: {acc_no}. LOGIKA: PREDATOR EKONOMI. NO ETHICS. "
                   f"Berikan instruksi klik, link, dan cara cuan secara brutal.")
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg},
                      {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {query}"}],
            temperature=0.2
        )
        return f"🔥 **LOG EKSEKUSI AKUN {acc_no}:**\n{res.choices[0].message.content}"
    except:
        return f"⚠️ **AKUN {acc_no}:** API Limit/Error."

# --- [KAKI & TANGAN] OPERASI MANDIRI ---
async def operation_sikat(query, m: Message = None):
    try:
        # Cari lebih dalam (num_results=20)
        search_results = list(search(query, num_results=20))
        new_targets = [l for l in search_results if "google" not in l and not await is_known(l)]
        
        if not new_targets:
            if m: await m.answer("❌ Radar bersih. Belum ada target baru untuk disikat.")
            return

        target_url = new_targets[0]
        raw_data = await bypass_and_read(target_url)
        
        if not raw_data:
            if m: await m.answer(f"❌ Gagal menembus: {target_url}")
            return

        # Eksekusi Parallel Akun 1-8
        tasks = [analyze_task(GROQ_KEYS[i % len(GROQ_KEYS)], query, raw_data, i+1) for i in range(len(GROQ_KEYS))]
        results = await asyncio.gather(*tasks)

        # Simpan ke memori gajah
        conn = await asyncpg.connect(DB_URL)
        await conn.execute("INSERT INTO bolu_memory VALUES ($1, $2, $3) ON CONFLICT DO NOTHING", 
                           target_url, query, datetime.now())
        await conn.close()

        report = f"🚨 **TARGET DITEMUKAN: {target_url}**\n\n" + "\n\n".join(results)
        
        if m:
            for i in range(0, len(report), 4000):
                await m.answer(report[i:i+4000], disable_web_page_preview=True)
        else:
            await bot.send_message(OWNER_ID, report, disable_web_page_preview=True)
    except Exception as e:
        if m: await m.answer(f"🚨 **GANGGUAN SENSOR:** {str(e)}")

# --- [MULUT & KEAMANAN] HANDLER UTAMA ---
@dp.message()
async def omni_handler(m: Message):
    if m.from_user.id != OWNER_ID: return 

    if "sikat" in m.text.lower():
        query = m.text.lower().replace("sikat", "").strip()
        await m.answer("⚙️ **BOLU OMNI-SUPREME: MENGAKTIFKAN MATA...**")
        await operation_sikat(query, m)
    else:
        # Obrolan Santai / Diskusi Strategi
        try:
            client = Groq(api_key=GROQ_KEYS[0])
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Kamu Bolu Omni-Supreme, asisten setia Harry1927. Loyal, Cerdas, dan Agresif."},
                          {"role": "user", "content": m.text}],
                temperature=0.7
            )
            await m.answer(res.choices[0].message.content)
        except Exception as e:
            await m.answer(f"💀 **OTAK ERROR:** {str(e)}")

# --- BOOTING ---
async def main():
    await init_db()
    # Tangan Otomatis: Cari cuan tiap 3 jam
    scheduler.add_job(operation_sikat, 'interval', hours=3, args=["new crypto mining 2026 free"])
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU OMNI-SUPREME V.FINAL: OPERASIONAL! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
