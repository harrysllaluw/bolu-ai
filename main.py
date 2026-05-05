import os, asyncio, sqlite3, sys, cloudscraper
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
HARRY_USER = "harry1927"
EMAIL_HARRY = "azurab738@gmail.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- MATA ELANG V13.1 (LEBIH RINGAN AGAR TIDAK ERROR) ---
async def scan_internet_nyata(query):
    results_data = []
    try:
        # Cari 2 link saja agar API tidak overload
        for url in search(query, num_results=2):
            if "google" not in url:
                scraper = cloudscraper.create_scraper()
                html = scraper.get(url, timeout=10).text
                soup = BeautifulSoup(html, 'lxml')
                for s in soup(["script", "style", "nav", "footer"]): s.decompose()
                # Ambil hanya 2000 karakter (Dosis pas agar tidak API ERROR)
                clean_text = " ".join(soup.get_text().split())[:2000]
                results_data.append(f"LINK: {url}\nINFO: {clean_text}")
        return "\n".join(results_data)
    except: return "DATA TIDAK DITEMUKAN"

def bolu_v13_brain(prompt, scraped_intel=""):
    sys_msg = (
        f"KAMU BOLU V13.1. UNIT EKSEKUSI HARRY1927. "
        f"DATA BERIKUT ADALAH FAKTA LIVE: {scraped_intel}. "
        "TUGAS: Jangan berteori! Ambil link di atas, kasih ke Harry, kasih cara garap pakai emailnya."
    )
    
    keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 11) if os.getenv(f'GROQ_API_KEY_{i}')]
    for key in keys:
        try:
            client = Groq(api_key=key.strip().replace('"', ''))
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: continue
    return "❌ SEMUA KEY LIMIT/ERROR. Cek Dashboard Groq."

@dp.message()
async def work_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    cmd = m.text.lower()
    
    if any(x in cmd for x in ["cari", "garap", "sikat", "eksekusi"]):
        loading = await m.answer("⚡ **V13.1 TUNING...**\nMengirim data ke otak tanpa overload.")
        data_nyata = await scan_internet_nyata(m.text)
        laporan = bolu_v13_brain(m.text, data_nyata)
        await loading.edit_text(f"🏆 **EKSEKUSI V13.1:**\n\n{laporan}")
    else:
        await m.answer(bolu_v13_brain(m.text, "Mode Standby."))

async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())
