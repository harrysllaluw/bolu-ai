import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- IDENTITAS MUTLAK BOLU V12.9 ---
TOKEN = '8709757602:AAEyEPKGtWuXIoYEwUgCCD5LQqTecZ8LA3A'
OWNER_ID = 728762443 

# SUNTIKAN: SCANNING JELI 8 API GROQ
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

    def get_next_key(self):
        if not GROQ_KEYS: return None
        key = GROQ_KEYS[self.key_index]
        self.key_index = (self.key_index + 1) % len(GROQ_KEYS)
        return key

    async def scrape_dewa(self, url):
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer", "header"]): 
                s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: 
            return ""

    async def eksekusi_pintar(self, prompt, context, acc_no, is_chat=False):
        """Logika Anti-Limit: Pindah API otomatis jika limit habis"""
        if not GROQ_KEYS: 
            return "❌ API KEY TIDAK TERDETEKSI DI RAILWAY."

        for _ in range(len(GROQ_KEYS)):
            current_key = self.get_next_key()
            try:
                client = Groq(api_key=current_key)
                if is_chat:
                    sys_msg = "Kamu Bolu, asisten setia Harry1927. Jawab cerdas dan agresif."
                else:
                    sys_msg = (f"IDENTITAS: BOLU SUPREME V12.9. EKSEKUTOR HARRY1927. AKUN: {acc_no}. "
                               "LOGIKA: PREDATOR EKONOMI. Berikan instruksi klik dan link presisi.")

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}, 
                              {"role": "user", "content": f"DATA: {context}\n\nCMD: {prompt}"}],
                    temperature=0.1
                )
                return res.choices[0].message.content
            except Exception:
                logging.warning(f"Kunci API nomor {self.key_index} limit, mencoba kunci lain...")
                continue
        
        return "❌ SEMUA API KEY LIMIT. HARAP TUNGGU BEBERAPA SAAT."

bolu = BoluSupreme()

async def cari_target_otomatis():
    query = random.choice(["new crypto airdrop 2026", "incentivized testnet confirmed list"])
    links = []
    try:
        for url in search(query, num_results=3):
            if "google" not in url: 
                links.append(url)
                break
    except: 
        pass
    
    if links:
        try:
            await bot.send_message(OWNER_ID, f"🎯 **TARGET DITEMUKAN!**\n\nLink: {links[0]}\n\nKetik 'Sikat' untuk eksekusi massal.")
        except: 
            pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    status = await m.answer("⚡ **BOLU V12.9: MENGAKTIFKAN 8 OTAK (ROTASI AKTIF)...**")
    
    query = m.text.lower().replace("sikat", "").strip() or "airdrop terbaru"
    links = []
    try:
        for url in search(query, num_results=1): 
            links.append(url)
    except: 
        pass
    
    if not links: 
        return await status.edit_text("❌ TIDAK ADA TARGET.")
    
    raw_data = await bolu.scrape_dewa(links[0])
    tasks = [bolu.eksekusi_pintar(m.text, raw_data, i+1) for i in range(len(GROQ_KEYS) if GROQ_KEYS else 1)]
    results = await asyncio.gather(*tasks)
    
    report = f"👑 **LAPORAN DIREKTUR HARRY1927**\n🌐 Target: {links[0]}\n\n"
    for i, res in enumerate(results):
        report += f"👤 **AKUN {i+1}:**\n{res}\n\n"
    
    if len(report) > 4000:
        for i in range(0, len(report), 4000): 
            await m.answer(report[i:i+4000])
    else:
        await status.edit_text(report, disable_web_page_preview=True)

@dp.message()
async def handler_chat(m: Message):
    if m.from_user.id != OWNER_ID: return
    jawaban = await bolu.eksekusi_pintar(m.text, "Mode Chat", 0, is_chat=True)
    await m.answer(jawaban)

async def main():
    scheduler.add_job(cari_target_otomatis, 'interval', hours=1)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.9 SUPREME: ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
