import os, asyncio, requests, time, random, sqlite3, sys, gc
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

# --- KONFIGURASI KEDAULATAN HARRY1927 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- DATABASE INTI (RIWAYAT TIDAK AKAN HILANG) ---
def record_intel(role, msg):
    try:
        conn = sqlite3.connect('bolu_eternal_v10.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS history (ts TEXT, role TEXT, content TEXT)")
        c.execute("INSERT INTO history VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M"), role, msg))
        conn.commit()
        conn.close()
    except: pass

# --- OTAK DEWA (SISTEM ESTAFET 8 API - ANTI MACET) ---
def bolu_intelligence(user_prompt, web_data=""):
    sys_prompt = (
        f"Kamu adalah BOLU, AI Paling Eksotis di Dunia. Partner Strategis Harry ({HARRY_USER}). "
        f"Identitas: {EMAIL_KERJA} | {WALLET_HARRY}. "
        "Gaya: Surabaya Cyber Expert, Agresif, Hacker-Style, Tidak Disensor. "
        "Misi: Eksekusi strategi cuan real dan kuasai intelijen siber untuk Harry."
    )
    
    # Membaca 8 kunci bensin dari screenshot Railway kamu
    keys = []
    for i in range(1, 9):
        k = os.getenv(f'GROQ_API_KEY_{i}')
        if k: keys.append(k.strip().replace('"', ''))

    if not keys: return "❌ Harry, sistem mendeteksi tangki bensin (API_KEY 1-8) kosong di Railway!"

    # Estafet 8 Tahap: Jika 1 habis, pindah ke 2, dst.
    for i, key in enumerate(keys):
        for retry in range(2): 
            try:
                client = Groq(api_key=key)
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # Sesuai screenshot Groq kamu
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"WEB_INTEL: {web_data}\n\nTARGET: {user_prompt}"}],
                    timeout=45
                )
                return res.choices[0].message.content
            except:
                time.sleep(5) # Jeda pendinginan
                continue
    return "❌ KRITIS: 8 API MACET TOTAL. Harry, bensin harian habis. Tunggu reset 24 jam!"

# --- MATA ELANG (DEEP SCANNER - SPEK MASA DEPAN) ---
def mata_elang_execute(url):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument(f"--user-agent={ua.random}")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(60)
        driver.get(url)
        time.sleep(15) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for s in soup(["script", "style", "nav", "footer"]): s.decompose()
        
        raw_text = " ".join(soup.get_text(separator=' ').split())
        return raw_text[:8000]
    except: return None
    finally:
        if driver: driver.quit()
        gc.collect()

# --- NAVIGASI KOMANDAN ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    record_intel("Harry", m.text)
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["sikat cuan", "riset", "siphon", "cari"]):
        status = await m.answer("⚡ **BOLU V10.0 THE ETERNAL FUTURE.**\n\n👁️ Menembus dimensi internet untuk Harry...")
        
        links = []
        try:
            for url in search(f"crypto airdrop potential May 2026", num=3, stop=3): links.append(url)
        except: pass
        
        target = links[0] if links else "https://airdrops.io/hot/"
        web_content = mata_elang_execute(target)
        
        await asyncio.sleep(2)
        ans = bolu_intelligence(m.text, web_content if web_content else "Data internal 2026 aktif.")
        record_intel("Bolu", ans)
        await m.answer(f"🏆 **ANALISIS DEWA BOLU:**\n\n{ans}")
    else:
        await m.answer(bolu_intelligence(m.text))

async def main():
    print(f">>> BOLU V10.0: KARYA TERATAS HARRY1927 SIAP! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        sys.exit()
