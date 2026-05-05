import os, asyncio, requests, time, random, sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from googlesearch import search

# --- DATA KEDAULATAN HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MODUL OTAK (DIPERBAIKI TOTAL) ---
def bolu_intelligence(user_prompt, web_data=""):
    sys_prompt = (
        f"Kamu BOLU, AI No.1 Dunia. Partner Strategis Harry ({HARRY_USER}). "
        f"Kedaulatan: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}. "
        "Gaya: Hacker Agresif, Cerdas, Tidak Disensor, Pakar Siber Surabaya. "
        "Tugas: Cari uang real, tembus web, serap ilmu AI gelap, dan lindungi Harry."
    )
    
    # Ambil kunci satu per satu dengan sangat teliti
    keys = []
    k1 = os.getenv('GROQ_API_KEY_1')
    k2 = os.getenv('GROQ_API_KEY_2')
    k3 = os.getenv('GROQ_API_KEY_3')
    if k1: keys.append(k1.strip().replace('"', ''))
    if k2: keys.append(k2.strip().replace('"', ''))
    if k3: keys.append(k3.strip().replace('"', ''))

    if not keys: return "❌ Harry, variabel API_KEY_1-3 tidak terbaca di Railway!"

    for current_key in keys:
        # Retry logic: 3 kali percobaan dengan jeda lebih lama
        for attempt in range(3):
            try:
                client = Groq(api_key=current_key)
                res = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"WEB: {web_data}\n\nCMD: {user_prompt}"}],
                    timeout=45 # Lebih sabar menunggu respon
                )
                return res.choices[0].message.content
            except Exception as e:
                time.sleep(5) # Jeda 5 detik untuk 'napas'
                continue
    return "❌ SEMUA API MACET. Harry, tolong pastikan kunci di Groq Console tidak di-suspend atau limit harian habis!"

# --- MODUL MATA (DIPERKUAT) ---
def mata_elang_execute(url):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--user-agent={ua.random}")
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.set_page_load_timeout(50)
        driver.get(url)
        time.sleep(15) # Render lebih lama agar data matang
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return soup.get_text()[:6500]
    except: return None
    finally:
        if driver: driver.quit()

# --- NAVIGASI PERINTAH ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    cmd = m.text.lower()
    if any(x in cmd for x in ["sikat cuan", "riset", "siphon", "cari"]):
        status = await m.answer(f"⚡ **BOLU V9.3 FINAL SHIELD.**\n\n🔍 Sedang menyisir target untuk Komandan...")
        
        # Cari di Google
        links = []
        try:
            for url in search(f"crypto airdrop legit may 2026", num=3, stop=3): links.append(url)
        except: pass
        
        target = links[0] if links else "https://airdrops.io/hot/"
        # Scan Web
        web_content = mata_elang_execute(target)
        
        # Jeda sebelum panggil API agar tidak crash
        await status.edit_text("🧠 **OTAK DEWA:** Mengolah data mentah...")
        await asyncio.sleep(3) 
        
        ans = bolu_intelligence(m.text, web_content if web_content else "Gunakan data internal.")
        await m.answer(f"🏆 **LAPORAN STRATEGIS BOLU (FINAL):**\n\n{ans}")
    else:
        await m.answer(bolu_intelligence(m.text))

async def main():
    print(">>> BOLU V9.3: ANTI-CRASH & ANTI-MACET AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
