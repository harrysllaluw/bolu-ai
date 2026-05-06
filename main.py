import os, asyncio, logging, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Modul "Tangan" - Otomatisasi Browser
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("⚠️ Playwright belum terinstall. Pastikan ada di requirements.txt")

# --- KEDAULATAN MUTLAK HARRY1927 V15.0 "THE HUMANOID" ---
TOKEN = '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = 728762443 
MEMORY_FILE = "bolu_humanoid.json"

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

class BoluHumanoid:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        return []

    def save_memory(self, link):
        self.memory.append(link)
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    async def gerakkan_tangan(self, url):
        """FUNGSI TANGAN: Mengetik dan Mengklik Otomatis"""
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True) # Jari digital bergerak rahasia
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")
                page = await context.new_page()
                await page.goto(url, timeout=60000)
                
                # Jari mengetik dan mencari tombol 'Join' atau 'Register'
                content = await page.content()
                await browser.close()
                return content
            except Exception as e:
                return f"⚠️ Tangan kaku: {str(e)}"

    async def eksekusi_dewa(self, prompt, context, role="manager"):
        key = random.choice(GROQ_KEYS) if GROQ_KEYS else None
        if not key: return "❌ KUNCI DEWA MATI."
        try:
            client = Groq(api_key=key)
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Kamu Bolu Humanoid Harry1927. Role: {role}. Jadilah eksekutor cuan yang agresif."},
                          {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.1
            )
            return res.choices[0].message.content
        except: return "⚠️ Otak sedang sinkronisasi..."

bolu = BoluHumanoid()

async def auto_hunting_daging():
    """Patroli Mencari Peluang Cuan Terbaru"""
    queries = ["new airdrop registration live now", "early crypto testnet register 2026"]
    q = random.choice(queries)
    try:
        for url in search(q, num_results=5):
            if url not in bolu.memory and "google" not in url:
                # Gunakan Mata Dewa untuk membedah link
                await bot.send_message(OWNER_ID, f"🕵️ **MATA DEWA MENDETEKSI TARGET!**\nLink: {url}\n\nSedang menggerakkan tangan untuk membedah isi...")
                raw_html = await bolu.gerakkan_tangan(url)
                analysis = await bolu.eksekusi_dewa("Apakah link ini punya potensi cuan nyata? Jika ya, kasih instruksi daftar.", raw_html[:10000], "manager")
                
                if "scam" not in analysis.lower():
                    bolu.save_memory(url)
                    await bot.send_message(OWNER_ID, f"👑 **HASIL ANALISIS PREDATOR:**\n{analysis}\n\nKetik 'Sikat' untuk instruksi eksekusi.")
                    break
    except: pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    await m.answer("👊 **MENGGERAKKAN TANGAN UNTUK EKSEKUSI MASSAL...**")
    # Logika eksekusi lanjut di sini
    await auto_hunting_daging()

@dp.message()
async def chat(m: Message):
    if m.from_user.id == OWNER_ID:
        ans = await bolu.eksekusi_dewa(m.text, "Chat Mode", "manager")
        await m.answer(ans)

async def main():
    scheduler.add_job(auto_hunting_daging, 'interval', minutes=30) # Patroli tiap 30 menit
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V15.0 THE HUMANOID ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
