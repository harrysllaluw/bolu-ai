import os, asyncio, logging, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V14.0 "SUPER UNLIMITED" ---
TOKEN = '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = 728762443 
MEMORY_FILE = "bolu_memory.json"

def get_sacred_keys():
    keys = []
    for i in range(1, 9):
        k = os.getenv(f'GROQ_API_KEY_{i}.') or os.getenv(f'GROQ_API_KEY_{i}')
        if k: keys.append(k.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_sacred_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluSupreme:
    def __init__(self):
        self.key_index = 0
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        return []

    def save_memory(self, link):
        self.memory.append(link)
        if len(self.memory) > 100: self.memory.pop(0) # Simpan 100 link terakhir
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    def get_role_key(self, role_type):
        """Multi-Agent: Membagi tugas ke API berbeda"""
        if not GROQ_KEYS: return None
        # Otak 1-3: Riset, 4-6: Analisis, 7-8: Eksekusi
        if role_type == "scout": idx = random.randint(0, 2)
        elif role_type == "analyst": idx = random.randint(3, 5)
        else: idx = random.randint(6, 7)
        return GROQ_KEYS[idx % len(GROQ_KEYS)]

    async def scrape_predator(self, url):
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=20)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer"]): s.decompose()
            return " ".join(soup.get_text().split())[:8000]
        except: return ""

    async def ask_bolu(self, prompt, context, role="analyst"):
        key = self.get_role_key(role)
        if not key: return "❌ API KEY ERROR."
        try:
            client = Groq(api_key=key)
            # Logika Multi-Agent Terintegrasi
            roles = {
                "scout": "Kamu adalah PENCARI CUAN. Fokus temukan tanggal TGE dan link pendaftaran.",
                "analyst": "Kamu adalah ANALIS RISIKO. Cek apakah ini SCAM atau REAL berdasarkan investor.",
                "manager": "Kamu adalah ASISTEN PRIBADI HARRY1927. Buat laporan singkat, padat, dan instruksi jelas."
            }
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": roles.get(role, "Asisten Harry1927")}, 
                          {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: return "⚠️ Otak sedang sinkronisasi..."

bolu = BoluSupreme()

async def auto_hunter():
    # Pencarian lebih agresif tapi cerdas
    queries = ["latest incentivized testnet airdrop confirmed", "new depin mining early access 2026"]
    q = random.choice(queries)
    try:
        for url in search(q, num_results=5):
            if url not in bolu.memory and "google" not in url:
                raw_data = await bolu.scrape_predator(url)
                # Analisis dulu sebelum kirim ke Harry (Filter Sampah)
                analysis = await bolu.ask_bolu("Apakah ini proyek legit? Jawab singkat saja.", raw_data, "analyst")
                if "scam" not in analysis.lower():
                    bolu.save_memory(url)
                    await bot.send_message(OWNER_ID, f"🚀 **DAGING DETECTED!**\nTarget: {url}\n\n**Hasil Analisis:**\n{analysis}\n\nKetik 'Sikat' untuk eksekusi.")
                    break
    except: pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    st = await m.answer("🧠 **8 OTAK SUPREME BEKERJA...**")
    target = m.text.replace("sikat", "").strip() or "airdrop terbaru"
    
    # Gunakan Multi-Agent untuk laporan
    raw = await bolu.scrape_predator(target)
    report = await bolu.ask_bolu("Berikan panduan pendaftaran paling simpel dan cepat.", raw, "manager")
    await st.edit_text(f"👑 **PANDUAN EKSEKUSI HARRY1927**\n\n{report}", disable_web_page_preview=True)

@dp.message()
async def chat(m: Message):
    if m.from_user.id == OWNER_ID:
        ans = await bolu.ask_bolu(m.text, "Chat Mode", "manager")
        await m.answer(ans)

async def main():
    scheduler.add_job(auto_hunter, 'interval', minutes=45) # Lebih sering patroli
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V14.0 SUPER UNLIMITED ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
