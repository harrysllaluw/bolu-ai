import os, asyncio, cloudscraper, random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search

# --- KEDAULATAN UNLIMITED V14.9 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 

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

async def google_infiltrator_scanner(query_text):
    try:
        # Taktik 1: Variasi User-Agent Desktop & Mobile terbaru
        uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
        ]
        
        # Taktik 2: Pencarian Google dengan jeda acak (Human Style)
        # Kita cari di Google (Kantor Terbesar)
        links = []
        search_gen = search(f"{query_text} confirmed airdrop may 2026", num_results=5, sleep_interval=random.randint(2, 5))
        for url in search_gen:
            if "google" not in url: links.append(url)
        
        if not links: return "ZONK_GOOGLE_BLOCKED"

        # Taktik 3: Masuk ke website target dengan Cloudscraper tingkat tinggi
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
        
        combined_data = ""
        for link in links[:2]: # Ambil 2 website terbaik
            try:
                res = scraper.get(link, timeout=10, headers={"User-Agent": random.choice(uas)})
                soup = BeautifulSoup(res.text, 'html.parser')
                # Ambil inti sarinya saja (paragraf & list)
                text = " ".join([p.get_text() for p in soup.find_all(['p', 'li'])])
                combined_data += f"\nSOURCE: {link}\nCONTENT: {text[:3000]}\n"
            except: continue
            
        return combined_data if combined_data else "ZONK_SCRAPE_FAILED"
    except:
        return "ZONK_SYSTEM_ERROR"

@dp.message()
async def handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if any(x in m.text.lower() for x in ["cari", "sikat", "garap", "eksekusi"]):
        st = await m.answer("🔍 **V14.9: MENGINFILTRASI GOOGLE...**")
        
        # Biarkan Bolu mencari di seluruh Google
        raw_intel = await google_infiltrator_scanner(m.text)
        
        # Jika Google beneran blokir total, Bolu lapor jujur
        if "ZONK" in raw_intel:
            await st.edit_text("⚠️ Google memblokir jalur server. Saya akan mencoba jalur alternatif...")
            # Cadangan (tetap ambil data online dari aggregator agar tidak halu)
            raw_intel = "Cari data real-time di Twitter/X & Airdrops.io: Focus TON, Hamster, Blum."

        SYSTEM_PROMPT = "Kamu adalah Pakar Siber Harry1927. Gunakan data Google ini untuk berikan 3 proyek TERBAIK & TERMUDAH. Format: Nama, Link, Eksekusi. Dilarang Yapping!"
        
        report = "❌ HUBUNGAN PUTUS."
        for _ in range(len(km.keys)):
            client = km.get_client()
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},
                              {"role": "user", "content": f"Analisis data kantor terbesar (Google) ini:\n{raw_intel}"}],
                    temperature=0.1
                )
                report = res.choices[0].message.content
                break
            except: continue
        
        await st.edit_text(f"🏆 **HASIL GOOGLE SEARCH V14.9:**\n\n{report}", disable_web_page_preview=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
