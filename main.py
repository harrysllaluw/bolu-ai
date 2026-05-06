import os, asyncio, logging, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V15.7 ---
TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = int(os.getenv('OWNER_ID') or 728762443)

def get_keys():
    """RADAR SILUMAN: Mengambil kunci dari Railway tanpa memicu error Build"""
    keys = []
    # Scan semua variabel yang mengandung 'GROQ'
    for k, v in os.environ.items():
        if "GROQ" in k and v.startswith('gsk_'):
            keys.append(v.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluPhantom:
    async def mata_predator(self, url):
        """MATA: Menembus proteksi web tanpa beban Playwright"""
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=15)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: return ""

    async def otak_dewa(self, prompt, context=""):
        if not GROQ_KEYS: return "❌ Kunci Groq tidak terdeteksi. Cek Variables!"
        client = Groq(api_key=random.choice(GROQ_KEYS))
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Bolu V15.7. Intelejen Harry1927. Cari cuan nyata."},
                          {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: return "⚠️ Otak sedang re-sinkronisasi..."

bolu = BoluPhantom()

async def patroli_cuan():
    """KAKI: Mencari link cuan tiap 30 menit"""
    q = random.choice(["new crypto airdrop confirmed incentive", "early node mining 2026"])
    try:
        for url in search(q, num_results=3):
            if "google" not in url:
                data = await bolu.mata_predator(url)
                analisis = await bolu.otak_dewa("Apakah ini proyek legit? Kasih instruksi daftar.", data)
                if "scam" not in analisis.lower():
                    await bot.send_message(OWNER_ID, f"🎯 **TARGET DITEMUKAN!**\nLink: {url}\n\n{analisis}")
                    break
    except: pass

@dp.message()
async def chat(m: Message):
    if m.from_user.id == OWNER_ID:
        await m.answer(await bolu.otak_dewa(m.text))

async def main():
    scheduler.add_job(patroli_cuan, 'interval', minutes=30)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V15.7 ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
