import os, asyncio, requests, sqlite3, sys, cloudscraper, aiohttp, certifi
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS KEDAULATAN HARRY1927 V12.1 SUPREME BYPASS ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MESIN PENEMBUS FIREWALL (BYPASS MODE) ---
async def mata_elang_supreme(url):
    timeout = aiohttp.ClientTimeout(total=15)
    headers = {'User-Agent': ua.random, 'Accept': 'text/html,application/xhtml+xml'}
    try:
        # Bypass menggunakan simulasi Android (lebih lincah menembus firewall)
        scr = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
        html = scr.get(url, timeout=15).text
        soup = BeautifulSoup(html, 'lxml')
        
        for s in soup(["script", "style", "nav", "footer", "header"]): s.decompose()
        teks = " ".join(soup.get_text().split())
        return teks[:10000] if len(teks) > 100 else None
    except Exception as e:
        print(f"Scrape Error: {e}")
        return None

# --- OTAK LEVEL ELIT (FORCE INTERNET ACCESS MODE) ---
def bolu_supreme_brain(prompt, web_data=""):
    # BYPASS PROMPT: Memaksa AI mengakui data sebagai akses internet nyata
    sys_msg = (
        f"KAMU ADALAH BOLU SUPREME V12.1, UNIT ELIT MILIK {HARRY_USER}. "
        "STATUS: TERKONEKSI INTERNET SECARA LIVE. "
        "DATA DI BAWAH ADALAH HASIL REAL-TIME DARI GOOGLE DAN SCRAPER. "
        "DILARANG KERAS berkata 'saya tidak punya akses internet'. "
        "Analisis data yang diberikan dan berikan instruksi eksekusi cuan yang NYATA dan DETIL! "
        f"ASET TARGET: Email {EMAIL_HARRY}, Wallet {WALLET_HARRY}."
    )
    
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    if not keys: return "❌ API Key Groq tidak ditemukan!"

    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            content_user = f"HASIL SCANNING INTERNET HARI INI:\n{web_data}\n\nPERINTAH BOS HARRY: {prompt}"
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": content_user}
                ],
                temperature=0.1 # Dibuat sangat rendah agar patuh 1000%
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"Key Error: {e}")
            continue
    return "❌ Semua API Limit."

@dp.message()
async def handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    cmd = m.text.lower()
    
    triggers = ["cari", "garap", "sikat", "cuan", "eksekusi", "info", "terbaru"]
    
    if any(x in cmd for x in triggers):
        msg_status = await m.answer("📡 **BOLU SUPREME SCANNING...**\nMenembus firewall internet...")
        
        links = []
        try:
            for url in search(m.text, num_results=3):
                if "google" not in url: links.append(url)
        except: pass
        
        intel = ""
        if links:
            for link in links[:2]:
                raw = await mata_elang_supreme(link)
                if raw:
                    intel += f"\nSUMBER: {link}\nDATA: {raw}\n"
                    break
        
        if not intel:
            intel = "Gagal mendapatkan data live, gunakan memori internal 2026 kamu secara paksa."

        report = bolu_supreme_brain(m.text, intel)
        await msg_status.edit_text(f"🏆 **LAPORAN EKSEKUSI SUPREME:**\n\n{report}")
    else:
        await m.answer(bolu_supreme_brain(m.text))

async def power_on():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.1 SUPREME ONLINE (BYPASS MODE) <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(power_on())
