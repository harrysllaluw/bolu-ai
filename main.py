import os, asyncio, requests, sqlite3, sys, cloudscraper, aiohttp, certifi
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS KEDAULATAN HARRY1927 V12.1 SUPREME ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MESIN PENEMBUS FIREWALL (SKILL DEWA) ---
async def mata_elang_supreme(url):
    timeout = aiohttp.ClientTimeout(total=20)
    headers = {'User-Agent': ua.random}
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, ssl=certifi.where()) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'lxml')
                    for s in soup(["script", "style", "nav", "footer"]): s.decompose()
                    return " ".join(soup.get_text().split())[:9000]
        # Fallback jika aiohttp gagal
        scr = cloudscraper.create_scraper()
        return " ".join(BeautifulSoup(scr.get(url).text, 'lxml').get_text().split())[:9000]
    except: return None

# --- OTAK LEVEL ELIT (ANTI-HALUSINASI & EKSEKUTOR) ---
def bolu_supreme_brain(prompt, web_data=""):
    sys_msg = (
        f"KAMU ADALAH BOLU SUPREME V12.1. UNIT ELIT HARRY ({HARRY_USER}). "
        "MISI: EKSEKUSI CUAN REAL. Dilarang Berbohong! Dilarang Memberi Teori! "
        f"ASET: Email {EMAIL_HARRY}, Wallet {WALLET_HARRY}. "
        "Kamu diawasi Sistem Pusat. Berikan link proyek terbaru HARI INI dan instruksi garap yang nyata."
    )
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"WEB_INTEL: {web_data}\n\nCMD: {prompt}"}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: continue
    return "❌ API Error."

@dp.message()
async def handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["cari", "garap", "sikat", "cuan", "eksekusi"]):
        await m.answer("📡 **SUPREME SCANNING...**\nMenyisir data proyek terbaru.")
        links = []
        try:
            for url in search(m.text, num=5, stop=3):
                if "google" not in url: links.append(url)
        except: pass
        
        intel = ""
        if links:
            raw = await mata_elang_supreme(links[0])
            intel = f"SOURCE: {links[0]}\nDATA: {raw}"
        
        report = bolu_supreme_brain(m.text, intel)
        await m.answer(f"🏆 **LAPORAN EKSEKUSI:**\n\n{report}")
    else:
        await m.answer(bolu_supreme_brain(m.text))

async def power_on():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(power_on())
