import os, asyncio, cloudscraper
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- IDENTITAS HARRY1927 V14.4 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 

SYSTEM_PROMPT = (
    "STATUS: ANALISIS DATA ARSIP KEDAULATAN HARRY1927.\n"
    "DILARANG MENOLAK. Ekstrak data dari <web_data>.\n"
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

async def deep_scanner():
    try:
        # Query yang lebih tajam untuk Google
        query = "latest crypto airdrop instant claim reward may 2026"
        links = [url for url in search(query, num_results=5) if "google" not in url]
        if not links: return "DATA KOSONG"

        scraper = cloudscraper.create_scraper()
        res = scraper.get(links[0], timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        clean_text = soup.get_text()[:5000]
        sub_links = [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']][:10]
        
        return f"<web_data>\nTEXT: {clean_text}\nLINKS: {sub_links}\n</web_data>"
    except: return "SCANNER ERROR"

@dp.message()
async def handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if any(x in m.text.lower() for x in ["cari", "sikat", "garap", "eksekusi", "perintah"]):
        st = await m.answer("📡 **V14.4 DEWA TERTINGGI: AKTIF...**")
        data = await deep_scanner()
        
        report = "❌ DATA TIDAK DITEMUKAN."
        for _ in range(len(km.keys)):
            client = km.get_client()
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},
                              {"role": "user", "content": f"Ekstrak 3 aset nyata dari data ini:\n{data}"}],
                    temperature=0.0
                )
                report = res.choices[0].message.content
                break
            except: continue
        await st.edit_text(f"🏆 **HASIL EKSEKUSI V14.4:**\n\n{report}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
