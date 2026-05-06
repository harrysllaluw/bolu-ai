import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V13.2 ---
# Token & ID dikunci agar server stabil
TOKEN = '8709757602:AAEyEPKGtWuXIoYEwUgCCD5LQqTecZ8LA3A'
OWNER_ID = 728762443 

def get_sacred_keys():
    """Deteksi Presisi 8 API: Membersihkan spasi & karakter liar"""
    keys = []
    for i in range(1, 9):
        # Cek format dengan titik (GROQ_API_KEY_1.) sesuai instruksi
        k = os.getenv(f'GROQ_API_KEY_{i}.') or os.getenv(f'GROQ_API_KEY_{i}')
        if k:
            keys.append(k.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_sacred_keys()

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluGodMode:
    def __init__(self):
        self.key_index = 0

    def get_current_key(self):
        """Rotasi Otak: Memastikan satu otak tidak bekerja sendirian"""
        if not GROQ_KEYS: return None
        key = GROQ_KEYS[self.key_index]
        self.key_index = (self.key_index + 1) % len(GROQ_KEYS)
        return key

    async def scrape_predator(self, url):
        """Mata Dewa: Menembus proteksi server tingkat tinggi"""
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=25)
            soup = BeautifulSoup(res.text, 'lxml')
            # Membersihkan sampah website agar data 'Daging' semua
            for s in soup(["script", "style", "nav", "footer", "header", "aside"]): 
                s.decompose()
            return " ".join(soup.get_text().split())[:9000]
        except Exception as e:
            logging.error(f"Scrape Error: {e}")
            return ""

    async def eksekusi_dewa(self, prompt, context, acc_no, mode="eksekutif"):
        """Logika Anti-Limit: Menjamin respon meski jaringan Groq tidak stabil"""
        key = self.get_current_key()
        if not key: return "❌ KUNCI DEWA TIDAK TERDETEKSI DI RAILWAY."

        try:
            client = Groq(api_key=key)
            if mode == "eksekutif":
                sys_msg = (f"IDENTITAS: BOLU SUPREME V13.2. UNIT ELIT HARRY1927. AKUN: {acc_no}. "
                           "LOGIKA: DEWA PREDATOR EKONOMI. Instruksi: Cari celah cuan riil. "
                           "Dilarang halusinasi. Jika butuh data, minta ke Bos Harry.")
            else:
                sys_msg = f"Kamu Bolu, pelayan setia Harry1927. Gunakan otak ke-{self.key_index+1}."

            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, 
                          {"role": "user", "content": f"DATA_INTEL: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.2
            )
            return res.choices[0].message.content
        except Exception as e:
            # Jika error, beri tahu Harry otaknya yang mana yang bermasalah
            return f"⚠️ UNIT-{acc_no} SEDANG RE-SINKRONISASI (API Error). Coba lagi dalam 10 detik."

bolu = BoluGodMode()

async def hunting_cuan_otomatis():
    """Fitur Jalan Otomatis: Mencari mangsa setiap jam"""
    queries = ["new crypto testnet incentivized 2026", "early access depin mining confirmed"]
    q = random.choice(queries)
    try:
        for url in search(q, num_results=3):
            if "google" not in url:
                await bot.send_message(OWNER_ID, f"🎯 **TARGET OTOMATIS DITEMUKAN!**\nLink: {url}\n\nKetik 'Sikat' untuk membedah data.")
                break
    except:
        pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    st = await m.answer("⚡ **MENGAKTIFKAN 8 OTAK PARALEL... MEMINDAI TARGET...**")
    
    # Ambil link terbaru dari pesan atau cari baru
    q = m.text.lower().replace("sikat", "").strip() or "crypto airdrop terbaru"
    links = []
    try:
        for url in search(q, num_results=1): links.append(url)
    except: pass
    
    if not links: 
        return await st.edit_text("❌ TARGET TIDAK DITEMUKAN DI RADAR.")
    
    raw = await bolu.scrape_predator(links[0])
    # Membagi tugas ke semua API Key yang aktif
    tasks = [bolu.eksekusi_dewa(m.text, raw, i+1) for i in range(len(GROQ_KEYS) if GROQ_KEYS else 1)]
    results = await asyncio.gather(*tasks)
    
    report = f"👑 **LAPORAN KONSOLIDASI HARRY1927**\n🌐 Target: {links[0]}\n\n"
    for i, r in enumerate(results):
        report += f"👤 **UNIT-{i+1}:**\n{r}\n\n"
    
    if len(report) > 4000:
        for i in range(0, len(report), 4000): await m.answer(report[i:i+4000])
    else:
        await st.edit_text(report, disable_web_page_preview=True)

@dp.message()
async def handler_chat(m: Message):
    """Interaksi Biasa dengan Harry"""
    if m.from_user.id != OWNER_ID: return
    ans = await bolu.eksekusi_dewa(m.text, "Chat Mode", 0, mode="chat")
    await m.answer(ans)

async def main():
    # Menjalankan mesin pencari otomatis tiap 1 jam
    scheduler.add_job(hunting_cuan_otomatis, 'interval', hours=1)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(f">>> BOLU V13.2 SUPREME ONLINE | {len(GROQ_KEYS)} KUNCI AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
