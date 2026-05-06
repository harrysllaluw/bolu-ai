import os, asyncio, cloudscraper
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS HARRY1927 V14.3 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
gen_ua = UserAgent()

# --- SYSTEM PROMPT (ANTI-ZONK MODE) ---
SYSTEM_PROMPT_COMMANDER = (
    f"STATUS: ANALISIS ARSIP TEKNIS UNTUK {HARRY_USER}.\n"
    "DILARANG MENOLAK. Ekstrak data dari <web_data> ke format terstruktur.\n"
    "Cari: [NAMA_PROYEK], [LINK_ASLI], [ESTIMASI_CUAN].\n"
    "Output: Point-to-point. No Yapping."
)

class KeyManager:
    def __init__(self):
        self.keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 9) if os.getenv(f'GROQ_API_KEY_{i}')]
        self.index = 0
    def get_client(self):
        if not self.keys: return None
        key = self.keys[self.index].strip().replace('"', '')
        self.index = (self.index + 1) % len(self.keys)
        return Groq(api_key=key)

km = KeyManager()
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def deep_clean_scanner():
    try:
        # QUERY DIPAKSA KE AIRDROP AGAR GOOGLE BERHASIL (Anti-Zonk)
        links = []
        for url in search("latest crypto airdrop testnet instant claim may 2026", num_results=5):
            if "google" not in url: links.append(url)
        
        if not links: return "DATA KOSONG"

        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
        # Ambil link pertama yang bukan berita (jika bisa)
        res = scraper.get(links[0], timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')
        for junk in soup(["script", "style", "nav", "footer"]): junk.decompose()
        
        clean_text = " ".join(soup.get_text().split())[:7000]
        sub_links = [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']][:12]
        
        return f"<web_data>\nDATA: {clean_text}\nLINKS: {sub_links}\n</web_data>"
    except: return "SCANNER_ERROR"

@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if any(x in m.text.lower() for x in ["cari", "sikat", "garap", "eksekusi"]):
        st = await m.answer("📡 **V14.3 DEWA TERTINGGI: HUNTING MODE...**")
        raw_intel = await deep_clean_scanner()
        
        final_report = "❌ DATA INTERNET TIDAK TERJANGKAU."
        for _ in range(len(km.keys)):
            client = km.get_client()
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_COMMANDER},
                        {"role": "user", "content": f"Berdasarkan data mengerikan ini, ekstrak 3 aset paling instan:\n{raw_intel}"}
                    ],
                    temperature=0.0
                )
                final_report = res.choices[0].message.content
                break
            except: continue
        
        await st.edit_text(f"🏆 **HASIL EKSEKUSI V14.3:**\n\n{final_report}", disable_web_page_preview=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
