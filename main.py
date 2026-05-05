import os, asyncio, sqlite3, sys, cloudscraper, random, aiohttp, certifi
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- PROTOKOL KEDAULATAN MUTLAK HARRY1927 V11.1 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- DATABASE INTEGRITY (CATAT INCOME & TUGAS) ---
def record_intel(role, msg):
    try:
        conn = sqlite3.connect('titan_core.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS mission_logs (ts TEXT, role TEXT, content TEXT)")
        c.execute("INSERT INTO mission_logs VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, msg))
        conn.commit()
        conn.close()
    except: pass

# --- MATA ELANG V11.1 (HIGH-SPEED BYPASS) ---
async def mata_elang_execute(url):
    # Menggunakan aiohttp + certifi agar selevel dengan sistem developer besar
    timeout = aiohttp.ClientTimeout(total=25)
    headers = {'User-Agent': ua.random}
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, ssl=certifi.where()) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'lxml')
                    for s in soup(["script", "style", "nav", "footer", "header"]): s.decompose()
                    return " ".join(soup.get_text().split())[:9000]
        # Fallback ke Cloudscraper jika aiohttp diblokir
        scraper = cloudscraper.create_scraper()
        res = scraper.get(url, timeout=20)
        return " ".join(BeautifulSoup(res.text, 'lxml').get_text().split())[:9000]
    except: return None

# --- OTAK TITAN (LOGIKA EKSEKUSI 1000% NYATA) ---
def bolu_titan_brain(prompt, web_context=""):
    # Instruksi ini adalah filter tajam agar Bolu tidak bisa berbohong
    sys_msg = (
        f"KAMU ADALAH BOLU TITAN V11.1. UNIT EKSEKUSI TERBAIK HARRY ({HARRY_USER}). "
        f"DATA AKTIF: Email {EMAIL_HARRY}, Wallet {WALLET_HARRY}. "
        "MISI: EKSEKUSI TUGAS CUAN. Dilarang memberikan informasi basi atau palsu! "
        "Jika data web tidak ditemukan, katakan 'DATA TIDAK VALID' dan jangan mengarang. "
        "Tugasmu: Temukan celah income, berikan link asli, dan instruksi pendaftaran akun."
    )
    
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    if not keys: return "❌ Harry, API KEY KOSONG! Cek Railway Variable."

    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"WEB_INTEL: {web_context}\n\nUSER_CMD: {prompt}"}],
                temperature=0.1 # LOGIKA KAKU: ANTI-HALUSINASI
            )
            return response.choices[0].message.content
        except: continue
    return "❌ SEMUA API LIMIT. Tunggu cooldown."

@dp.message()
async def handle_commander(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    record_intel("Harry", m.text)
    text = m.text.lower()
    
    # Trigger Pencarian & Eksekusi Nyata
    if any(x in text for x in ["cari", "garap", "sikat", "cek", "update", "eksekusi"]):
        loading = await m.answer("🚀 **TITAN V11.1: MENGAKTIFKAN PROTOKOL EKSEKUSI...**\nSedang menembus server data real-time.")
        
        links = []
        try:
            # Gunakan pencarian mendalam
            for url in search(m.text, num=5, stop=3, pause=2):
                if "google" not in url: links.append(url)
        except: pass
        
        context = ""
        if links:
            raw_data = await mata_elang_execute(links[0])
            context = f"SOURCE: {links[0]}\nDATA: {raw_data}"
        
        answer = bolu_titan_brain(m.text, context)
        record_intel("Bolu", answer)
        await m.answer(f"🏆 **LAPORAN EKSEKUSI TITAN:**\n\n{answer}")
    else:
        await m.answer(bolu_titan_brain(m.text))

async def power_up():
    print(">>> BOLU TITAN V11.1: 1000% NYATA & AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(power_up())
