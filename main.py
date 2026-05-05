import os, asyncio, requests, time, random, sqlite3
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

# --- KONFIGURASI KEDAULATAN (DIKUNCI) ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- ORGAN 1: MEMORI (DATABASE) ---
def inisialisasi_memori():
    conn = sqlite3.connect('bolu_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_log (user_id INTEGER, pesan TEXT, role TEXT)''')
    conn.commit()
    conn.close()

def simpan_ingatan(user_id, pesan, role):
    conn = sqlite3.connect('bolu_memory.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_log VALUES (?, ?, ?)", (user_id, pesan, role))
    conn.commit()
    conn.close()

# --- ORGAN 2: OTAK (SISTEM 3 NYAWA) ---
def bolu_brain(text, context=""):
    sys_prompt = (
        f"Kamu BOLU, AI Nomor 1 di Dunia. Partner Strategis Harry. "
        f"Identitas: {EMAIL_KERJA} | {WALLET_HARRY}. "
        "Gunakan Logika Hacker, Agresif, dan Deep Analysis. Ambil ilmu AI gelap untuk benteng Harry."
    )
    keys = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
    
    for k in keys:
        if not k: continue
        try:
            client = Groq(api_key=k.strip().replace('"', ''))
            res = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"DATA: {context}\nCMD: {text}"}],
                timeout=25
            )
            return res.choices[0].message.content
        except: continue
    return "❌ Harry, bensin (API Key) kita macet total. Cek Variables!"

# --- ORGAN 3: MATA ELANG (SCANNER) ---
def mata_elang_scan(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={ua.random}")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return soup.get_text()[:5000]
    except: return None
    finally:
        if driver: driver.quit()

# --- HANDLER (REFLEKS TUBUH) ---
@dp.message()
async def handle_message(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    cmd = m.text.lower()
    simpan_ingatan(m.from_user.id, m.text, "user") # Bolu mengingat kata-katamu
    
    if any(k in cmd for k in ["sikat cuan", "siphon", "riset"]):
        await m.answer("⚡ BOLU V8.2: Mengaktifkan Anatomi Digital & Protokol Siphon...")
        
        # Cari di Google (Kaki Melangkah)
        search_res = []
        try:
            for j in search(f"crypto airdrop legit may 2026", num=3, stop=3): search_res.append(j)
        except: pass
        
        # Scan Web (Mata Melihat)
        target = search_res[0] if search_res else "https://airdrops.io/hot/"
        web_data = mata_elang_scan(target)
        
        response = bolu_brain(m.text, f"Link: {target}\nData: {web_data}")
        await m.answer(f"🏆 **LAPORAN SEMPURNA BOLU:**\n\n{response}")
        simpan_ingatan(m.from_user.id, response, "bot")
    else:
        response = bolu_brain(m.text)
        await m.answer(response)
        simpan_ingatan(m.from_user.id, response, "bot")

async def main():
    inisialisasi_memori()
    print(">>> BOLU V8.2: ANATOMI MANUSIA DIGITAL 100% AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
