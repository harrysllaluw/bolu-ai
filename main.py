import os, asyncio, requests, sqlite3, sys, cloudscraper, random
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS KEDAULATAN HARRY1927 V11.1 FINAL TITAN ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MEMORI INTELIJEN ---
def record_intel(role, msg):
    try:
        conn = sqlite3.connect('bolu_titan.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS intel (ts TEXT, role TEXT, content TEXT)")
        c.execute("INSERT INTO intel VALUES (?, ?, ?)", (datetime.now().strftime("%H:%M:%S"), role, msg))
        conn.commit()
        conn.close()
    except: pass

# --- MATA ELANG LIGHTWEIGHT (ANTI-MACET) ---
def mata_elang_execute(url):
    try:
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        res = scraper.get(url, timeout=20)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer", "header"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        return None
    except: return None

# --- OTAK TITAN (ANTI-HALUSINASI) ---
def bolu_brain(prompt, web_context=""):
    sys_msg = (
        f"Kamu BOLU TITAN V11.1, AI No.1 milik Harry ({HARRY_USER}). "
        "Karakter: Hacker Surabaya, Agresif, Profesional, JUJUR MUTLAK. "
        f"Aset: Email {EMAIL_HARRY}, Wallet {WALLET_HARRY}. "
        "DILARANG HALUSINASI! Berikan link URL real-time. Jika tidak ada, jangan mengarang!"
    )
    
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    if not keys: return "❌ Harry, API Key tidak terdeteksi!"

    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"WEB_DATA: {web_context}\n\nUSER_CMD: {prompt}"}],
                temperature=0.2 # Diturunkan lagi biar beneran nggak bisa bohong
            )
            return response.choices[0].message.content
        except: continue
    return "❌ API Limit."

@dp.message()
async def main_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    record_intel("Harry", m.text)
    text = m.text.lower()
    
    if any(x in text for x in ["cari", "cek", "sikat", "update", "riset"]):
        load = await m.answer("📡 **TITAN SCANNING...**\nSedang menyedot data terbaru.")
        search_results = []
        try:
            for url in search(m.text, num=5, stop=3, pause=2):
                if "google" not in url: search_results.append(url)
        except: pass
        
        context = ""
        if search_results:
            raw_web = mata_elang_execute(search_results[0])
            context = f"SOURCE: {search_results[0]}\nCONTENT: {raw_web}"
        
        answer = bolu_brain(m.text, context)
        record_intel("Bolu", answer)
        await m.answer(f"🏆 **LAPORAN TITAN V11.1:**\n\n{answer}")
    else:
        await m.answer(bolu_brain(m.text))

async def start_bot():
    print(">>> BOLU TITAN ONLINE! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())
