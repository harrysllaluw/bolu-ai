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

# --- PARAMETER KEDAULATAN HARRY (RIWAYAT TERKUNCI) ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MODUL 1: MEMORI PERMANEN (OTAK) ---
def simpan_memori(pesan):
    try:
        conn = sqlite3.connect('bolu_core.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS memory (ts TEXT, msg TEXT)")
        c.execute("INSERT INTO memory VALUES (?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M"), pesan))
        conn.commit()
        conn.close()
    except: pass

# --- MODUL 2: JANTUNG API (ANTI-MACET TOTAL) ---
def bolu_intelligence(user_prompt, web_data=""):
    sys_prompt = (
        f"Kamu BOLU, AI No.1 Dunia. Partner Strategis Harry ({HARRY_USER}). "
        f"Kedaulatan: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}. "
        "Gaya: Hacker Agresif, Cerdas, Tidak Disensor, Pakar Siber Surabaya. "
        "Tugas: Cari uang real, tembus web, serap ilmu AI gelap, dan lindungi Harry."
    )
    
    # Deteksi 3 Kunci secara teliti
    api_keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 4)]
    keys = [k.strip().replace('"', '').replace("'", "") for k in api_keys if k]

    if not keys:
        return "❌ Harry, variabel API_KEY_1-3 tidak terbaca di Railway!"

    for current_key in keys:
        for attempt in range(3): # Dicoba 3x per kunci (Lebih Sabar & Kuat)
            try:
                client = Groq(api_key=current_key)
                res = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"WEB_DATA: {web_data}\n\nUSER_CMD: {user_prompt}"}],
                    timeout=30
                )
                return res.choices[0].message.content
            except Exception as e:
                time.sleep(3) # Jeda untuk menstabilkan koneksi
                continue
    return "❌ SEMUA API MACET. Harry, pastikan bensin di Groq Console belum habis limitnya!"

# --- MODUL 3: MATA ELANG (DEEP SCANNER DENGAN PENYAMARAN) ---
def mata_elang_execute(url):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--user-agent={ua.random}") # Jubah Penyamaran
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(45)
        driver.get(url)
        time.sleep(12) # Waktu render maksimal
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return soup.get_text()[:7000] # Kapasitas serap lebih besar
    except: return None
    finally:
        if driver: driver.quit()

# --- MODUL 4: NAVIGASI PERINTAH HARRY ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return # Benteng Pertahanan Harry
    
    cmd = m.text.lower()
    simpan_memori(m.text)
    
    if any(x in cmd for x in ["sikat cuan", "riset", "siphon", "cari"]):
        status = await m.answer(f"⚡ **BOLU V9.2 SPEK DEWA AKTIF.**\n\n🔍 Menyisir Google & Membedah Web untuk Harry...")
        
        # Skill Kaki (Pencarian Google)
        links = []
        try:
            for url in search(f"crypto airdrop legit {datetime.now().year}", num=3, stop=3, pause=2):
                links.append(url)
        except: pass
        
        target = links[0] if links else "https://airdrops.io/hot/"
        # Skill Mata (Deep Scan)
        web_content = mata_elang_execute(target)
        
        # Skill Otak (Analisis)
        ans = bolu_intelligence(m.text, web_content if web_content else "Gagal tembus web, gunakan database internal 2026.")
        await m.answer(f"🏆 **LAPORAN STRATEGIS BOLU (SPEK DEWA):**\n\n{ans}")
    else:
        await m.answer(bolu_intelligence(m.text))

async def main():
    print(">>> BOLU V9.2: SPEK DEWA & RIWAYAT 100.000% TERVERIFIKASI! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
