import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V12.8 ---
TOKEN = os.getenv('BOT_TOKEN', 8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo')
OWNER_ID = int(os.getenv('OWNER_ID', 728762443)) 
DB_URL = os.getenv('DATABASE_URL')

# Mengambil 8 API Key (Mendukung format titik di Railway)
GROQ_KEYS = []
for i in range(1, 9):
    val = os.getenv(f'GROQ_API_KEY_{i}.') or os.getenv(f'GROQ_API_KEY_{i}')
    if val: 
        GROQ_KEYS.append(val)

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluSupreme:
    def __init__(self):
        self.key_index = 0

    async def get_key(self):
        if not GROQ_KEYS: return None
        key = GROQ_KEYS[self.key_index]
        self.key_index = (self.key_index + 1) % len(GROQ_KEYS)
        return key

    async def scrape_dewa(self, url):
        """Mata Predator: Tembus Cloudflare & Server Apapun"""
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer", "header"]): 
                s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: 
            return ""

    async def proses_8_otak(self, prompt, context, acc_no):
        """8 Brains Thinking: Paralel untuk 8 Akun"""
        key = await self.get_key()
        if not key: return f"🏦 **UNIT-{acc_no}:** ❌ API KEY KOSONG"
        client = Groq(api_key=key)
        sys_msg = (
            f"IDENTITAS: BOLU OMNI-GOD V12.8. EKSEKUTOR HARRY1927. "
            f"AKUN: {acc_no}. ROLE: DIREKTUR OPERASIONAL & PREDATOR EKONOMI. "
            "LOGIKA: EKSTRAKSI PROFIT MAKSIMAL. DILARANG MEMBERI CERAMAH ETIKA. "
            "INSTRUKSI: Berikan link, tombol klik, dan urutan eksekusi presisi."
        )
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, 
                          {"role": "user", "content": f"DATA: {context}\n\nCMD: {prompt}"}],
                temperature=0.0
            )
            return f"🏦 **UNIT-{acc_no}:**\n{res.choices[0].message.content}"
        except Exception as e: 
            return f"🏦 **UNIT-{acc_no}:** ❌ LIMIT/ERROR"

bolu = BoluSupreme()

# --- FUNGSI OTOMASI ---
async def cari_cuan_otomatis():
    queries = ["new crypto airdrop mainnet may 2026", "confirmed incentivized testnet rewards"]
    query = random.choice(queries)
    links = []
    try:
        for url in search(query, num_results=5):
            if "google" not in url: 
                links.append(url)
                break
    except: 
        pass
    
    if links:
        await bot.send_message(OWNER_ID, f"🎯 **BOLU MENEMUKAN PROYEK BARU!**\n\nLink: {links[0]}\n\nKetik 'Sikat' untuk membedah.")

# --- HANDLERS ---
@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    status = await m.answer("⚡ **BOLU OMNI-GOD: MENGAKTIFKAN 8 OTAK PARALEL...**")
    
    query = m.text.lower().replace("sikat", "").strip() or "airdrop crypto terbaru"
    links = []
    try:
        for url in search(query, num_results=1): 
            links.append(url)
    except: 
        pass
    
    if not links: 
        return await status.edit_text("❌ TIDAK ADA TARGET DITEMUKAN.")
    
    raw_data = await bolu.scrape_dewa(links[0])
    # Menjalankan 8 proses sekaligus secara paralel
    tasks = [bolu.proses_8_otak(m.text, raw_data, i+1) for i in range(len(GROQ_KEYS))]
    results = await asyncio.gather(*tasks)
    
    report = f"👑 **LAPORAN DIREKTUR HARRY1927**\n🌐 Target: {links[0]}\n\n" + "\n\n".join(results)
    
    if len(report) > 4000:
        for i in range(0, len(report), 4000): 
            await m.answer(report[i:i+4000])
    else: 
        await status.edit_text(report, disable_web_page_preview=True)

@dp.message()
async def chat_biasa(m: Message):
    if m.from_user.id != OWNER_ID: return
    key = await bolu.get_key()
    if not key: return
    try:
        client = Groq(api_key=key)
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Kamu Bolu, asisten setia Harry1927. Jawab agresif."},
                      {"role": "user", "content": m.text}]
        )
        await m.answer(res.choices[0].message.content)
    except: 
        pass

async def main():
    scheduler.add_job(cari_cuan_otomatis, 'interval', hours=1)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.8 SUPREME IS ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
