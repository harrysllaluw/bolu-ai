import os, asyncio, logging, random, json
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V16.0 ---
TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = int(os.getenv('OWNER_ID') or 728762443)
MEMORY_FILE = "bolu_vault.json"

def get_keys():
    """RADAR SILUMAN: Mengambil semua kunci Groq yang ada di Railway"""
    keys = []
    for k, v in os.environ.items():
        if "GROQ" in k and v.startswith('gsk_'):
            keys.append(v.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluEternal:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def save_vault(self, url, intel):
        self.memory[url] = {"intel": intel, "time": str(datetime.now())}
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    async def mata_predator(self, url):
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=15)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: return ""

    async def otak_dewa(self, prompt, context="", acc_no=1):
        if not GROQ_KEYS: return "❌ Kunci Groq tidak terbaca. Cek Variables di Railway!"
        client = Groq(api_key=random.choice(GROQ_KEYS))
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Bolu V16.0. Intelejen Harry1927. Unit-{acc_no}. Jawab singkat dan cari cuan."},
                    {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}
                ],
                temperature=0.2
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"⚠️ Unit-{acc_no} sedang re-sinkronisasi..."

bolu = BoluEternal()

async def patroli_cuan():
    q = random.choice(["new crypto airdrop confirmed incentive", "early node mining access 2026"])
    try:
        for url in search(q, num_results=3):
            if url not in bolu.memory and "google" not in url:
                data = await bolu.mata_predator(url)
                if len(data) > 500:
                    bolu.save_vault(url, data)
                    await bot.send_message(OWNER_ID, f"🎯 **TARGET DITEMUKAN!**\nLink: {url}\n\nKetik 'Sikat' untuk membedah potensi cuannya.")
                    break
    except: pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    await m.answer("⚡ **BOLU V16.0: MENGAKTIFKAN 8 OTAK PARALEL...**")
    if not bolu.memory: return await m.answer("❌ Memori kosong. Biarkan saya patroli dulu.")
    last_url = list(bolu.memory.keys())[-1]
    raw_data = bolu.memory[last_url]['intel']
    ans = await bolu.otak_dewa(m.text, raw_data)
    await m.answer(f"👑 **LAPORAN DIREKTUR HARRY1927**\n\n{ans}", disable_web_page_preview=True)

@dp.message()
async def chat(m: Message):
    if m.from_user.id == OWNER_ID:
        await m.answer(await bolu.otak_dewa(m.text))

async def main():
    scheduler.add_job(patroli_cuan, 'interval', minutes=30)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V16.0 ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
