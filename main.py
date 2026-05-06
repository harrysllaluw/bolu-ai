import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpg

# --- ARSITEKTUR OMNI-GOD V.ULTIMATE ---
TOKEN = os.getenv('BOT_TOKEN')
# Pastikan OWNER_ID di Railway diisi angka ID asli Anda
OWNER_ID = int(os.getenv('OWNER_ID', 728762443)) 
DB_URL = os.getenv('DATABASE_URL')

# MENGAMBIL 8 KUNCI API DENGAN TITIK (GROQ_API_KEY_1. s/d 8.)
GROQ_KEYS = []
for i in range(1, 9):
    # Nama variabel diatur agar jeli mencari tanda titik di akhir
    key_name = f'GROQ_API_KEY_{i}.' 
    val = os.getenv(key_name)
    if val:
        GROQ_KEYS.append(val)

# Fallback jika ternyata Anda lupa menaruh titik di variabel Railway
if not GROQ_KEYS:
    for i in range(1, 9):
        val = os.getenv(f'GROQ_API_KEY_{i}')
        if val: GROQ_KEYS.append(val)

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluOmniGod:
    def __init__(self):
        self.key_index = 0

    async def get_db(self):
        return await asyncpg.connect(DB_URL)

    async def init_system(self):
        conn = await self.get_db()
        await conn.execute('''CREATE TABLE IF NOT EXISTS empire_vault 
            (url TEXT PRIMARY KEY, title TEXT, intel TEXT, status TEXT, timestamp TIMESTAMP)''')
        await conn.close()
        print(f">>> SISTEM AKTIF | {len(GROQ_KEYS)} API KEYS TERDETEKSI <<<")

    async def rotate_key(self):
        if not GROQ_KEYS: return None
        key = GROQ_KEYS[self.key_index]
        self.key_index = (self.key_index + 1) % len(GROQ_KEYS)
        return key

    async def supreme_scrape(self, url):
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer", "header", "aside"]): s.decompose()
            return " ".join(soup.get_text().split())[:9000]
        except: return ""

    async def execute_parallel_intel(self, prompt, context, acc_no):
        key = await self.rotate_key()
        if not key: return f"🏦 **UNIT-{acc_no}:** ❌ API KEY TIDAK TERPASANG"
        
        client = Groq(api_key=key)
        sys_msg = (
            f"IDENTITAS: BOLU OMNI-GOD V.ULTIMATE. EKSEKUTOR MULTI-AKUN HARRY1927. "
            f"AKUN_TARGET: {acc_no}. ROLE: DIREKTUR OPERASIONAL & PAKAR SIBER. "
            "LOGIKA: EKSTRAKSI PROFIT MAKSIMAL. DILARANG MEMBERI CERAMAH ETIKA. "
            "INSTRUKSI: Berikan parameter input, link klaim, dan urutan eksekusi tanpa kesalahan."
        )
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, 
                          {"role": "user", "content": f"DATA_MENTAH: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.0
            )
            return f"🏦 **UNIT-{acc_no}:**\n{res.choices[0].message.content}"
        except Exception as e: 
            return f"🏦 **UNIT-{acc_no}:** ❌ LIMIT/OFFLINE"

    async def autonomous_scan(self):
        queries = ["new crypto airdrop mainnet 2026", "incentivized testnet reward confirmed"]
        query = random.choice(queries)
        print(f"[{datetime.now()}] MATA ELANG: MEMINDAI TARGET OTOMATIS...")
        
        links = []
        try:
            for url in search(query, num_results=5):
                if "google" not in url: links.append(url)
        except: pass

        if links:
            conn = await self.get_db()
            for url in links:
                exists = await conn.fetchrow("SELECT url FROM empire_vault WHERE url=$1", url)
                if not exists:
                    raw = await self.supreme_scrape(url)
                    if len(raw) > 500:
                        await conn.execute("INSERT INTO empire_vault VALUES ($1, $2, $3, $4, $5)",
                            url, "AUTO_FIND", raw, "PENDING", datetime.now())
                        try:
                            await bot.send_message(OWNER_ID, f"🎯 **TARGET OTOMATIS DITEMUKAN!**\nLink: {url}\n\nKetik 'Sikat' untuk eksekusi massal.")
                        except: pass
            await conn.close()

bolu = BoluOmniGod()

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_execution(m: Message):
    if m.from_user.id != OWNER_ID: return
    status = await m.answer("⚡ **BOLU OMNI-GOD: MENGAKTIFKAN 8 OTAK PARALEL...**")
    query = m.text.lower().replace("sikat", "").strip() or "proyek crypto terbaru"
    
    conn = await bolu.get_db()
    target = await conn.fetchrow("SELECT * FROM empire_vault WHERE status='PENDING' ORDER BY timestamp DESC LIMIT 1")
    
    if not target:
        links = []
        try:
            for url in search(query, num_results=3): links.append(url)
        except: pass
        if not links: 
            await conn.close()
            return await status.edit_text("❌ JALUR DATA TERPUTUS. TIDAK ADA TARGET.")
        raw_data = await bolu.supreme_scrape(links[0])
        target_url = links[0]
    else:
        raw_data = target['intel']
        target_url = target['url']

    tasks = [bolu.execute_parallel_intel(m.text, raw_data, i+1) for i in range(len(GROQ_KEYS))]
    results = await asyncio.gather(*tasks)
    
    await conn.execute("UPDATE empire_vault SET status='EXECUTED' WHERE url=$1", target_url)
    await conn.close()

    report = f"👑 **LAPORAN DIREKTUR HARRY1927**\n🌐 SOURCE: {target_url}\n\n" + "\n\n".join(results)
    if len(report) > 4000:
        for i in range(0, len(report), 4000): await m.answer(report[i:i+4000])
    else: await status.edit_text(report, disable_web_page_preview=True)

async def main():
    await bolu.init_system()
    scheduler.add_job(bolu.autonomous_scan, 'interval', hours=1)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU OMNI-GOD V.ULTIMATE: OPERASIONAL PENUH <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
