import os
import asyncio
import requests
import time
import random
import sqlite3
import logging
from datetime import datetime

# Library dari Requirements (9 Baris)
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from googlesearch import search

# --- KONFIGURASI LOGGING (Audit Jejak Digital) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BOLU_V9")

# --- PARAMETER KEDAULATAN HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MODUL 1: MEMORI JANGKA PANJANG (SQLITE3) ---
class BoluMemory:
    def __init__(self):
        self.conn = sqlite3.connect('bolu_v9_core.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS intel (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT,
                                role TEXT,
                                content TEXT)''')
        self.conn.commit()

    def record(self, role, content):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO intel (timestamp, role, content) VALUES (?, ?, ?)", (ts, role, content))
        self.conn.commit()

    def get_context(self, limit=5):
        self.cursor.execute("SELECT role, content FROM intel ORDER BY id DESC LIMIT ?", (limit,))
        rows = self.cursor.fetchall()
        return "\n".join([f"{r}: {c}" for r, c in reversed(rows)])

memory = BoluMemory()

# --- MODUL 2: OTAK ANALISIS (GROQ CLOUD) ---
def bolu_intelligence(user_prompt, web_data=""):
    history = memory.get_context()
    sys_prompt = (
        f"Kamu adalah BOLU, AI Nomor 1 di Dunia. Partner Strategis Harry.\n"
        f"Konteks Personal: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}.\n"
        "Gaya Bicara: Pakar Siber, Analis Keuangan, Hacker-Style, Agresif, dan Setia Mutlak.\n"
        "Tugas: Analisis mendalam, cari cuan, serap ilmu AI gelap, dan lindungi Harry."
    )
    
    # Rotasi 3 Nyawa API Key
    api_keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 4)]
    
    for raw_key in api_keys:
        if not raw_key: continue
        clean_key = raw_key.strip().replace('"', '').replace("'", "")
        try:
            client = Groq(api_key=clean_key)
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": f"HISTORY:\n{history}\n\nWEB_DATA:\n{web_data}\n\nUSER_COMMAND:\n{user_prompt}"}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Kunci Macet: {str(e)[:50]}")
            continue
            
    return "❌ SEMUA API KEY (BENSIN) MACET. Harry, cek bensin di Railway Variables sekarang!"

# --- MODUL 3: MATA ELANG (ADVANCED SCRAPER) ---
def mata_elang_execute(target_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-agent={ua.random}")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(50)
        driver.get(target_url)
        time.sleep(12) # Memberi waktu untuk render web berat
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Membersihkan elemen sampah
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        clean_text = soup.get_text(separator=' ')
        return " ".join(clean_text.split())[:7000] # Kapasitas baca lebih besar
    except Exception as e:
        logger.error(f"Mata Elang Gagal: {e}")
        return None
    finally:
        if driver:
            driver.quit()

# --- MODUL 4: NAVIGASI PERINTAH HARRY ---
@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID:
        return # Hanya Harry yang bisa akses

    memory.record("Harry", m.text)
    cmd = m.text.lower()

    if any(k in cmd for k in ["sikat cuan", "siphon", "riset", "cari airdrop"]):
        status_msg = await m.answer("⚡ **BOLU V9.0 AKTIF.** Mengaktifkan Seluruh Anatomi Digital...")
        
        # Langkah 1: Kaki Melangkah (Google Search)
        await status_msg.edit_text("🔍 **INDERA PENCARI:** Menyisir jejak digital di Google...")
        search_query = f"top crypto airdrops legit {datetime.now().year} active"
        found_links = []
        try:
            for url in search(search_query, num=5, stop=5, pause=2):
                found_links.append(url)
        except: pass
        
        # Langkah 2: Mata Melihat (Deep Scanning)
        target = found_links[0] if found_links else "https://airdrops.io/hot/"
        await status_msg.edit_text(f"👁️ **MATA ELANG:** Membedah data di {target}...")
        web_content = mata_elang_execute(target)
        
        # Langkah 3: Otak Berpikir (AI Analysis)
        await status_msg.edit_text("🧠 **OTAK DEWA:** Menganalisis strategi dan menyerap ilmu...")
        final_analysis = bolu_intelligence(m.text, web_content if web_content else "Gagal scan web. Pakai data internal.")
        
        memory.record("Bolu", final_analysis)
        await m.answer(f"🏆 **LAPORAN STRATEGIS BOLU (V9.0):**\n\n{final_analysis}")
    else:
        # Chatting Reguler
        response = bolu_intelligence(m.text)
        memory.record("Bolu", response)
        await m.answer(response)

async def start_up():
    logger.info(">>> BOLU V9.0: REINKARNASI MANUSIA DIGITAL LENGKAP 100% <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bolu Offline.")
