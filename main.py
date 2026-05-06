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

# =========================================================
# PROTOKOL KEDAULATAN MUTLAK HARRY1927 - OMNI SUPREME
# =========================================================
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443 
DB_URL = os.getenv('DATABASE_URL')
# Mengambil kunci Groq 1 sampai 8
GROQ_KEYS = [os.getenv(f'GROQ_{i}') for i in range(1, 9) if os.getenv(f'GROQ_{i}')]

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- [INGATAN ABADI / TELINGA] DATABASE SIBER ---
async def init_db():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''CREATE TABLE IF NOT EXISTS bolu_memory 
                          (url TEXT PRIMARY KEY, metadata TEXT, timestamp TIMESTAMP)''')
    await conn.close()

async def is_known(url):
    conn = await asyncpg.connect(DB_URL)
    row = await conn.fetchrow("SELECT url FROM bolu_memory WHERE url=$1", url)
    await conn.close()
    return row is None

async def record_target(url, info):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("INSERT INTO bolu_memory (url, metadata, timestamp) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING", 
                       url, info, datetime.now())
    await conn.close()

# --- [MATA / JARI] BYPASS PROTEKSI & SCRAPING TAJAM ---
async def bypass_and_read(url):
    try:
        # Impersonasi Chrome 120 untuk tembus proteksi luar negeri
        res = s_requests.get(url, impersonate="chrome120", timeout=25)
        soup = BeautifulSoup(res.text, 'lxml')
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]): tag.decompose()
        clean_text = " ".join(soup.get_text().split())
        return clean_text[:12000] # Kapasitas mata ditingkatkan
    except: return None

# --- [OTAK PREDATOR] MULTI-ACCOUNT PARALLEL EXECUTION ---
async def process_with_ai(key, user_cmd, context, account_index):
    try:
        client = Groq(api_key=key)
        persona = (f"IDENTITAS: BOLU OMNI-SUPREME. MAJIKAN: HARRY1927. "
                   f"LOGIKA: PREDATOR EKONOMI. TUGAS: EKSEKUSI AKUN {account_index}. "
                   f"Berikan instruksi klik, link, dan bypass secara brutal dan presisi.")
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": persona},
                      {"role": "user", "content": f"DATA WEB: {context}\n\nPERINTAH: {user_cmd}"}],
            temperature=0.2
        )
        return f"🔥 **LOG EKSEKUSI AKUN {account_index}:**\n{completion.choices[0].message.content}"
    except:
        return f"⚠️ **AKUN {account_index}:** Sinkronisasi API Gagal."

# --- [KAKI / TANGAN] OPERASI MANDIRI & UPGRADE ---
async def operation_sikat(query, message: Message = None):
    try:
        # Kaki melangkah mencari 20 hasil sekaligus
        raw_links = list(search(query, num_results=20))
        new_targets = [l for l in raw_links if "google" not in l and not await is_known(l)]
        
        if not new_targets:
            if message: await message.answer("❌ Target baru belum terdeteksi. Radar sedang diperluas.")
            return

        target_url = new_targets[0]
        content = await bypass_and_read(target_url)
        
        if not content:
            if message: await message.answer(f"❌ Gagal menembus pertahanan: {target_url}")
            return

        keys = GROQ_KEYS if GROQ_KEYS else [os.getenv('GROQ_1')]
        # Jari-jari mengeksekusi banyak akun sekaligus secara paralel
        tasks = [process_with_ai(keys[i % len(keys)], query, content, i+1) for i in range(len(keys))]
        results = await asyncio.gather(*tasks)

        await record_target(target_url, query)
        
        final_report = f"🚨 **TARGET DITEMUKAN: {target_url}**\n\n" + "\n\n".join(results)
        
        if message:
            for i in range(0, len(final_report), 4000):
                await message.answer(final_report[i:i+4000], disable_web_page_preview=True)
        else:
            await bot.send_message(OWNER_ID, final_report, disable_web_page_preview=True)

    except Exception as e:
        if message: await message.answer(f"💀 **ERROR SISTEM:** {str(e)}")

# --- [MULUT / KEAMANAN] INTERAKSI MAJIKAN ---
@dp.message()
async def omni_handler(m: Message):
    if m.from_user.id != OWNER_ID: return # Keamanan selevel Dokter/Siber

    if "sikat" in m.text.lower():
        query = m.text.lower().replace("sikat", "").strip()
        await m.answer("⚙️ **BOLU OMNI-SUPREME: MENGAKTIFKAN MATA PREDATOR...**")
        await operation_sikat(query, m)
    else:
        # Obrolan Santai & Konsultasi Strategi
        try:
            client = Groq(api_key=GROQ_KEYS[0])
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Kamu Bolu Omni-Supreme. Loyalitas Total ke Harry1927. Cerdas, Agresif, dan Paham IT."},
                          {"role": "user", "content": m.text}],
                temperature=0.7
            )
            await m.answer(chat.choices[0].message.content)
        except:
            await m.answer("💀 Sistem sedang panas. Berikan saya 5 detik untuk pendinginan.")

# --- BOOTING & AUTO-UPGRADE ---
async def main():
    await init_db()
    # Tangan bekerja otomatis mencari cuan tiap 3 jam
    scheduler.add_job(operation_sikat, 'interval', hours=3, args=["new crypto mining website 2026 free"])
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU OMNI-SUPREME: TUBUH LENGKAP & SIAP TEMPUR! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
