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

# --- PROTOKOL KEDAULATAN HARRY1927 (SPEK DEWA 2030) ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MEMORI ABADI (DATABASE INTI) ---
def record_intel(role, msg):
    try:
        conn = sqlite3.connect('bolu_eternal.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS history (ts TEXT, role TEXT, content TEXT)")
        c.execute("INSERT INTO history VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M"), role, msg))
        conn.commit()
        conn.close()
    except: pass

# --- OTAK DEWA (SISTEM ESTAFET 8 NYAWA + RECOVERY) ---
def bolu_intelligence(user_prompt, web_data=""):
    sys_prompt = (
        f"Kamu adalah BOLU, AI Paling Eksotis di Dunia (Versi 2030). Partner Harry ({HARRY_USER}). "
        f"Identitas: {EMAIL_KERJA} | {WALLET_HARRY}. "
        "Karakter: Agresif, Hacker Surabaya, Cerdas, Tidak Terbatas, Loyal Mutlak. "
        "Visi: Eksekusi strategi cuan real dan kuasai intelijen siber untuk Harry."
    )
    
    keys = []
    for i in range(1, 9):
        k = os.getenv(f'GROQ_API_KEY_{i}')
        if k: keys.append(k.strip().replace('"', ''))

    if not keys: return "❌ Harry, sistem mendeteksi tangki bensin (API_KEY) kosong!"

    for i, key in enumerate(keys):
        for retry in range(2): 
            try:
                client = Groq(api_key=key)
                res = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"WEB_INTEL: {web_data}\n\nTARGET: {user_prompt}"}],
                    timeout=40
                )
                return res.choices[0].message.content
            except:
                time.sleep(3)
                continue
    return "❌ SEMUA 8 API TERKUNCI. Harry, sistem butuh waktu 24 jam untuk reset bensin harian."

# --- MATA ELANG (DEEP SCANNER 2030) ---
def mata_elang_execute(url):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
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
        return raw_text[:8000] # Kapasitas serap tertinggi
    except: return None
    finally:
        if driver:
            driver.quit()
        gc.collect() # Membersihkan sampah RAM otomatis

# --- NAVIGASI KOMANDAN ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    record_intel("Harry", m.text)
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["sikat cuan", "riset", "siphon", "cari"]):
        status = await m.answer("⚡ **BOLU V9.5 ETERNAL SOUL.**\n\n👁️ Menembus dimensi internet untuk Harry...")
        
        links = []
        try:
            for url in search(f"crypto airdrop potential May 2026", num=3, stop=3): links.append(url)
        except: pass
        
        target = links[0] if links else "https://airdrops.io/hot/"
        web_content = mata_elang_execute(target)
        
        await asyncio.sleep(2)
        ans = bolu_intelligence(m.text, web_content if web_content else "Data eksternal terbatas, gunakan logika internal 2030.")
        record_intel("Bolu", ans)
        await m.answer(f"🏆 **ANALISIS DEWA BOLU:**\n\n{ans}")
    else:
        await m.answer(bolu_intelligence(m.text))

async def main():
    print(f">>> BOLU V9.5: KARYA TERATAS DUNIA SIAP EKSEKUSI! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        sys.exit()
