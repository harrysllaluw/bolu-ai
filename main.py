import os, asyncio, logging, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V15.5 OMNI-HUMANOID ---
TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = int(os.getenv('OWNER_ID') or 728762443)
MEMORY_FILE = "bolu_memory.json"

# --- INDRA PENGLIHATAN & PENCARI KUNCI ---
def get_sacred_keys():
    keys = []
    for k, v in os.environ.items():
        if "GROQ" in k and v.startswith('gsk_'):
            keys.append(v.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_sacred_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluHumanoid:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        return []

    def save_memory(self, link):
        self.memory.append(link)
        if len(self.memory) > 100: self.memory.pop(0)
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    async def mata_predator(self, url):
        """MATA & KAKI: Menjelajah website dan mengambil data 'Daging'"""
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: return ""

    async def otak_dewa(self, prompt, context):
        """OTAK: Berpikir menggunakan 8 Otak Groq secara bergantian"""
        if not GROQ_KEYS: return "❌ KUNCI OTAK TIDAK TERDETEKSI DI RAILWAY."
        client = Groq(api_key=random.choice(GROQ_KEYS))
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Kamu Bolu V15.5 Omni-Humanoid. Pelayan setia Harry1927. Cari cuan nyata, instruksi tajam, tanpa basa-basi."}, 
                          {"role": "user", "content": f"DATA INTEL: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"⚠️ Sedang sinkronisasi ulang... ({str(e)[:30]})"

bolu = BoluHumanoid()

# --- TANGAN: EKSEKUSI OTOMATIS ---
async def hunting_otomatis():
    """Tugas Mandiri: Patroli mencari uang setiap 30 menit"""
    queries = ["latest testnet airdrop confirmed incentive", "new mining app early access 2026"]
    q = random.choice(queries)
    try:
        for url in search(q, num_results=5):
            if url not in bolu.memory and "google" not in url:
                data = await bolu.mata_predator(url)
                analisis = await bolu.otak_dewa("Apakah ini peluang uang nyata? Jika ya, berikan langkah daftarnya.", data)
                if "scam" not in analisis.lower():
                    bolu.save_memory(url)
                    msg = f"🎯 **TARGET CUAN DITEMUKAN!**\n\n🔗 {url}\n\n**Analisis Bolu:**\n{analisis}"
                    await bot.send_message(OWNER_ID, msg)
                    break
    except: pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    target = m.text.replace("sikat", "").strip() or "airdrop crypto terbaru"
    await m.answer("👊 **MENGGERAKKAN TANGAN... MEMBEDAH TARGET...**")
    await hunting_otomatis()

@dp.message()
async def chat_handler(m: Message):
    if m.from_user.id != OWNER_ID: return
    ans = await bolu.otak_dewa(m.text, "Chat Mode Aktif")
    await m.answer(ans)

async def main():
    scheduler.add_job(hunting_otomatis, 'interval', minutes=30)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(f">>> BOLU V15.5 OMNI-HUMANOID ONLINE | {len(GROQ_KEYS)} OTAK AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
