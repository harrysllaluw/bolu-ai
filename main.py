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

# --- DATA KERAMAT HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- JANTUNG OTAK (SISTEM ANTI-MACET) ---
def bolu_intelligence(user_prompt, web_data=""):
    sys_prompt = f"Kamu BOLU, AI No.1 Dunia. Partner Strategis Harry ({EMAIL_KERJA}). Gunakan Logika Hacker & Cuan."
    
    # Memasukkan kunci secara manual agar tidak ada yang terlewat
    keys = []
    if os.getenv('GROQ_API_KEY_1'): keys.append(os.getenv('GROQ_API_KEY_1'))
    if os.getenv('GROQ_API_KEY_2'): keys.append(os.getenv('GROQ_API_KEY_2'))
    if os.getenv('GROQ_API_KEY_3'): keys.append(os.getenv('GROQ_API_KEY_3'))

    if not keys:
        return "❌ Harry, cek Railway Variables. Nama kunci harus GROQ_API_KEY_1 sampai 3!"

    for current_key in keys:
        clean_key = current_key.strip().replace('"', '').replace("'", "")
        # Mencoba 2 kali per kunci agar lebih kuat (Retry Logic)
        for _ in range(2): 
            try:
                client = Groq(api_key=clean_key)
                res = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"DATA WEB: {web_data}\n\nPERINTAH: {user_prompt}"}],
                    timeout=25
                )
                return res.choices[0].message.content
            except Exception as e:
                print(f"DEBUG: Kunci/Koneksi bermasalah, jeda 2 detik...")
                time.sleep(2)
                continue
    
    return "❌ SEMUA API KEY MACET. Harry, pastikan bensin di Groq Console belum habis limitnya!"

# --- MATA ELANG (SCANNER) ---
def mata_elang_execute(url):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--user-agent={ua.random}")
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.set_page_load_timeout(40)
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return soup.get_text()[:6000]
    except: return None
    finally:
        if driver: driver.quit()

# --- PENANGAN PESAN ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    cmd = m.text.lower()
    if any(x in cmd for x in ["sikat cuan", "riset", "siphon", "cari"]):
        await m.answer("⚡ BOLU V9.1: Mengaktifkan Mata Elang & Mencari Jalur Cuan...")
        
        # Cari link lewat Google
        links = []
        try:
            for url in search(f"crypto airdrop legit {datetime.now().year}", num=3, stop=3):
                links.append(url)
        except: pass
        
        target = links[0] if links else "https://airdrops.io/hot/"
        web_content = mata_elang_execute(target)
        ans = bolu_intelligence(m.text, web_content if web_content else "Gunakan data internal.")
        await m.answer(f"🏆 **LAPORAN BOLU:**\n\n{ans}\n\nEmail: {EMAIL_KERJA}")
    else:
        await m.answer(bolu_intelligence(m.text))

async def main():
    print(">>> BOLU V9.1: SISTEM ANTI-MACET AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
