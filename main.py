import os, asyncio, logging, random, json
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KONFIGURASI KEDAULATAN HARRY1927 V16.0 ---
TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = int(os.getenv('OWNER_ID') or 728762443)
MEMORY_FILE = "bolu_vault.json"

# SCANNER 8 OTAK (Format Titik & Normal)
def get_sacred_keys():
    keys = []
    for i in range(1, 9):
        k = os.getenv(f'GROQ_API_KEY_{i}.') or os.getenv(f'GROQ_API_KEY_{i}')
        if k and k.startswith('gsk_'):
            keys.append(k.strip().replace('"', '').replace("'", ""))
    if not keys: # Scan total jika tidak ketemu
        for v in os.environ.values():
            if v.startswith('gsk_'): keys.append(v)
    return keys

GROQ_KEYS = get_sacred_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluEternal:
    def __init__(self):
        self.key_index = 0
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        return {}

    def save_to_vault(self, url, intel):
        self.memory[url] = {"intel": intel, "time": str(datetime.now())}
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    async def get_brain(self):
        if not GROQ_KEYS: return None
        key = GROQ_KEYS[self.key_index % len(GROQ_KEYS)]
        self.key_index += 1
        return Groq(api_key=key)

    async def mata_predator(self, url):
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: return ""

    async def berpikir(self, prompt, context="", acc_no=1):
        client = await self.get_brain()
        if not client: return "❌ KUNCI GROQ TIDAK TERDETEKSI."
        try:
            # PERBAIKAN ERROR __INIT__ : Format standar yang pasti jalan
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Kamu BOLU V16.0. Intelejen Harry1927. Unit-{acc_no}. Fokus: PROFIT & DATA NYATA."},
                    {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}
                ],
                temperature=0.2
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ Unit-{acc_no} Re-Sinkronisasi... (Limit/Error)"

bolu = BoluEternal()

async def patroli_otomatis():
    queries = ["new crypto airdrop confirmed incentive", "early node mining access 2026"]
    q = random.choice(queries)
    try:
        for url in search(q, num_results=5):
            if url not in bolu.memory and "google" not in url:
                raw = await bolu.mata_predator(url)
                if len(raw) > 500:
                    bolu.save_to_vault(url, raw)
                    await bot.send_message(OWNER_ID, f"🎯 **TARGET DITEMUKAN!**\nLink: {url}\n\nKetik 'Sikat' untuk membedah.")
                    break
    except: pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    await m.answer("⚡ **MENGAKTIFKAN 8 OTAK PARALEL... MEMBEDAH TARGET...**")
    
    # Ambil target terakhir dari memori
    if not bolu.memory:
        return await m.answer("❌ Belum ada target di memori. Biarkan saya patroli dulu.")
    
    last_url = list(bolu.memory.keys())[-1]
    raw_data = bolu.memory[last_url]['intel']
    
    tasks = [bolu.berpikir(m.text, raw_data, i+1) for i in range(len(GROQ_KEYS))]
    results = await asyncio.gather(*tasks)
    
    report = f"👑 **LAPORAN DIREKTUR HARRY1927**\n🌐 SOURCE: {last_url}\n\n" + "\n\n".join(results)
    if len(report) > 4000:
        for i in range(0, len(report), 4000): await m.answer(report[i:i+4000])
    else: await m.answer(report, disable_web_page_preview=True)

@dp.message()
async def chat_handler(m: Message):
    if m.from_user.id != OWNER_ID: return
    ans = await bolu.berpikir(m.text)
    await m.answer(ans)

async def main():
    scheduler.add_job(patroli_otomatis, 'interval', minutes=30)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V16.0 ETERNAL ONLINE | JALUR AMAN AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
