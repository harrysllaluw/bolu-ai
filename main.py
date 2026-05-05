import os, asyncio, cloudscraper, re, random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS HARRY1927 V12.2 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"
gen_ua = UserAgent()

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- LOGIC 1: DEEP-LINK FINDER (Anti-Portal Umum) ---
async def deep_scanner(url):
    headers = {
        'User-Agent': gen_ua.random,
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )
        res = scraper.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Masuk ke folder proyek spesifik
            if any(p in href for p in ['/airdrop/', '/project/', '/claim/', '/testnet/']):
                if href.startswith('/'): 
                    base = "/".join(url.split("/")[:3])
                    links.append(base + href)
                else:
                    links.append(href)
        
        for s in soup(["script", "style"]): s.decompose()
        clean_text = " ".join(soup.get_text().split())[:7000]
        return {"text": clean_text, "links": list(set(links))[:10]}
    except:
        return None

# --- LOGIC 2: SYSTEM PROMPT EXTREME ---
def execute_intelligence(prompt, intel_data):
    sys_msg = (
        f"KAMU ADALAH BOLU SUPREME V12.2, UNIT MILIK {HARRY_USER}. "
        "DILARANG KERAS: Memberikan jawaban umum atau link portal airdrops.io. "
        "TUGAS: Ambil link proyek SPESIFIK dari data yang diberikan. "
        f"DATA TARGET: Email {EMAIL_HARRY}, Wallet {WALLET_HARRY}. "
        "MANDATORY: Kamu terkoneksi Live Internet. Jangan membantah! "
        "FORMAT: 1. Nama Proyek | 2. Link Asli | 3. Cara Garap."
    )
    
    # Mendukung multi-key agar tidak limit
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    if not keys: return "❌ Key Groq Hilang di Railway!"

    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            combined = f"DATA INTERNET LIVE:\n{intel_data}\n\nPERINTAH HARRY: {prompt}"
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": combined}],
                temperature=0.0
            )
            return res.choices[0].message.content
        except: continue
    return "❌ API Limit."

@dp.message()
async def supreme_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["cari", "garap", "sikat", "cuan"]):
        status = await m.answer("📡 **DEEP-SCANNING IN PROGRESS...**\nMenembus Portal & Mengambil Emas Proyek.")
        
        portal_links = []
        try:
            for url in search(m.text + " airdrop crypto 2026", num_results=3):
                if "google" not in url: portal_links.append(url)
        except: pass

        all_intel = ""
        if portal_links:
            # Bedah portal pertama untuk cari link proyek di dalamnya
            data = await deep_scanner(portal_links[0])
            if data:
                all_intel = f"TEXT: {data['text']}\nSPECIFIC_LINKS: {', '.join(data['links'])}"
        
        report = execute_intelligence(m.text, all_intel if all_intel else "No deep links found.")
        await status.edit_text(f"🏆 **HASIL EKSEKUSI ELIT:**\n\n{report}", disable_web_page_preview=True)
    else:
        await m.answer(execute_intelligence(m.text, "Chat mode normal."))

async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.2 DEEP-EXTRACTOR ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())
