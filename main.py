import os, asyncio, cloudscraper, random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search

# --- IDENTITAS KEDAULATAN V14.7 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 

# Header Manusia Asli hasil audit AI Berbayar
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1"
}

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

async def deep_intel_scanner():
    try:
        # Taktik 1: Pencarian Google dengan Penyamaran
        query = "crypto airdrop instant claim reward confirmed May 2026"
        links = []
        # Menggunakan pause untuk menghindari deteksi bot
        for url in search(query, num_results=3, sleep_interval=2):
            if "google" not in url: links.append(url)
        
        # Taktik 2: Jika Google Gagal, tembak portal data A1 langsung
        target = links[0] if links else "https://cryptopanic.com/news/airdrop/"
        
        scraper = cloudscraper.create_scraper()
        res = scraper.get(target, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Pembersihan Data Tingkat Tinggi
        for s in soup(['script', 'style', 'nav', 'footer', 'header']): s.decompose()
        return f"<web_data>\nSOURCE: {target}\nCONTENT: {soup.get_text()[:7000]}\n</web_data>"
    except Exception as e:
        return f"<web_data>EMERGENCY_DATA: Fokus pada Hamster Kombat V2, TapSwap Listing, dan TON Ecosystem Instant Rewards.</web_data>"

@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if any(x in m.text.lower() for x in ["cari", "sikat", "garap", "eksekusi", "perintah"]):
        st = await m.answer("📡 **V14.7 DEWA TERTINGGI: MENGAKSES SATELIT...**")
        intel = await deep_intel_scanner()
        
        SYSTEM_PROMPT = "Kamu adalah Pakar Siber & Analis Keuangan Harry1927. Ekstrak cuan instan dari data secara agresif. Dilarang basa-basi."
        
        report = "❌ HUBUNGAN TERPUTUS."
        for _ in range(len(km.keys)):
            client = km.get_client()
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},
                              {"role": "user", "content": f"Analisis data ini dan berikan 3 proyek termudah hari ini:\n{intel}"}],
                    temperature=0.1 # Akurasi Tinggi
                )
                report = res.choices[0].message.content
                break
            except: continue
        
        await st.edit_text(f"🏆 **LAPORAN HASIL EKSEKUSI V14.7:**\n\n{report}", disable_web_page_preview=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
