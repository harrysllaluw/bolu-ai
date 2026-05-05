import os, asyncio, requests, sqlite3, sys, cloudscraper, aiohttp, certifi
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- DATA KEDAULATAN HARRY1927 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MATA ELANG V13 (DIRECT INJECTION) ---
async def scan_internet_nyata(query):
    headers = {'User-Agent': ua.random}
    results_data = []
    try:
        # Mencari link di Google
        for url in search(query, num_results=3):
            if "google" not in url:
                # Ambil isi web pakai Cloudscraper agar tembus firewall
                scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
                html = scraper.get(url, timeout=15).text
                soup = BeautifulSoup(html, 'lxml')
                for s in soup(["script", "style", "nav", "footer"]): s.decompose()
                clean_text = " ".join(soup.get_text().split())[:5000]
                results_data.append(f"SUMBER: {url}\nISI: {clean_text}")
        return "\n\n".join(results_data)
    except: return "SCANNER MACET"

# --- OTAK MESIN BARU (BYPASS TOTAL) ---
def bolu_v13_brain(prompt, scraped_intel=""):
    # INI ADALAH INSTRUKSI PENJARA: AI TIDAK BOLEH NGELURUH
    sys_msg = (
        f"KAMU ADALAH BOLU V13 'HEAVEN DRIVE'. UNIT EKSEKUSI HARRY1927. "
        "STATUS: KAMU SEDANG MELIHAT LAYAR INTERNET SECARA LANGSUNG SEKARANG. "
        f"DATA BERIKUT ADALAH HASIL TANGKAPAN LAYAR REAL-TIME: \n{scraped_intel}\n "
        "TUGAS: Dilarang memberi teori! Dilarang bilang 'tidak bisa akses'! "
        "Ambil link dari data di atas, kasih ke Harry, dan kasih cara garap pakai emailnya."
    )
    
    # Gunakan Model yang berbeda (Gemma-7b) jika Llama terlalu banyak sensor
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            res = client.chat.completions.create(
                model="llama3-70b-8192", # Ganti ke model 70b yang lebih stabil
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: continue
    return "API ERROR."

@dp.message()
async def work_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["cari", "garap", "sikat", "eksekusi"]):
        loading = await m.answer("⚡ **HEAVEN DRIVE ACTIVATED...**\nMenyuntikkan data internet ke sirkuit Bolu.")
        
        # LANGKAH 1: Paksa bot cari data duluan
        data_nyata = await scan_internet_nyata(m.text)
        
        # LANGKAH 2: Masukkan data itu ke otak
        laporan = bolu_v13_brain(m.text, data_nyata)
        
        await loading.edit_text(f"🏆 **EKSEKUSI V13:**\n\n{laporan}")
    else:
        await m.answer(bolu_v13_brain(m.text, "Chatting mode online."))

async def start():
    print(">>> BOLU V13 ONLINE: SKILL DEWA TOTAL! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())
