import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V13.1 ---
TOKEN = '8709757602:AAEyEPKGtWuXIoYEwUgCCD5LQqTecZ8LA3A'
OWNER_ID = 728762443 

# SUNTIKAN KUNCI: DETEKSI PRESISI 8 API (TANPA SPASI, DENGAN TITIK)
def get_sacred_keys():
    keys = []
    for i in range(1, 9):
        # Mengambil dari Railway sesuai gambar (GROQ_API_KEY_1.)
        k = os.getenv(f'GROQ_API_KEY_{i}.') or os.getenv(f'GROQ_API_KEY_{i}')
        if k:
            keys.append(k.strip())
    return keys

GROQ_KEYS = get_sacred_keys()

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluGodMode:
    def __init__(self):
        self.key_index = 0

    def get_rotation(self):
        """Menyiapkan rotasi 8 otak tanpa celah"""
        if not GROQ_KEYS: return []
        return GROQ_KEYS[self.key_index:] + GROQ_KEYS[:self.key_index]

    async def scrape_predator(self, url):
        """Mata Dewa: Menembus proteksi server tingkat tinggi"""
        try:
            res = s_requests.get(url, impersonate="chrome120", timeout=25)
            soup = BeautifulSoup(res.text, 'lxml')
            for s in soup(["script", "style", "nav", "footer", "header"]): 
                s.decompose()
            return " ".join(soup.get_text().split())[:9000]
        except: 
            return ""

    async def eksekusi_dewa(self, prompt, context, acc_no, mode="eksekutif"):
        """Logika Anti-Limit: Pindah API otomatis 1 sampai 8"""
        urutan_kunci = self.get_rotation()
        if not urutan_kunci: 
            return "❌ KUNCI DEWA TIDAK TERPASANG DI RAILWAY."

        for key in urutan_kunci:
            try:
                client = Groq(api_key=key)
                if mode == "eksekutif":
                    sys_msg = (f"IDENTITAS: BOLU SUPREME V13.1. UNIT ELIT HARRY1927. AKUN: {acc_no}. "
                               "LOGIKA: DEWA PREDATOR EKONOMI. Cari instruksi klaim uang/crypto. "
                               "Jika proyek butuh alamat USDT/Wallet, minta kepada Bos Harry secara tegas.")
                else:
                    sys_msg = "Kamu Bolu, asisten Dewa Tertinggi Harry1927. Jawab dengan cerdas dan setia."

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}, 
                              {"role": "user", "content": f"DATA_INTEL: {context}\n\nPERINTAH: {prompt}"}],
                    temperature=0.1
                )
                self.key_index = (GROQ_KEYS.index(key) + 1) % len(GROQ_KEYS)
                return res.choices[0].message.content
            except:
                continue 
        
        return "❌ SEMUA 8 OTAK SEDANG RECHARGE. TUNGGU 5 MENIT."

bolu = BoluGodMode()

async def hunting_cuan_otomatis():
    queries = ["new crypto airdrop mainnet payout", "confirmed reward testnet 2026", "crypto bounties high pay"]
    q = random.choice(queries)
    links = []
    try:
        for url in search(q, num_results=3):
            if "google" not in url: 
                links.append(url)
                break
    except: 
        pass
    
    if links:
        try:
            await bot.send_message(OWNER_ID, f"🎯 **LAPORAN PREDATOR: TARGET DETECTED!**\nLink: {links[0]}\n\nKetik 'Sikat' untuk eksekusi pembayaran.")
        except: 
            pass

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    st = await m.answer("⚡ **MENGAKTIFKAN 8 OTAK PARALEL... MEMBEDAH PELUANG CUAN...**")
    
    q = m.text.lower().replace("sikat", "").strip() or "airdrop cuan terbaru"
    links = []
    try:
        for url in search(q, num_results=1): 
            links.append(url)
    except: 
        pass
    
    if not links: 
        return await st.edit_text("❌ TARGET KOSONG.")
    
    raw = await bolu.scrape_predator(links[0])
    tasks = [bolu.eksekusi_dewa(m.text, raw, i+1) for i in range(len(GROQ_KEYS) if GROQ_KEYS else 1)]
    results = await asyncio.gather(*tasks)
    
    report = f"👑 **LAPORAN KONSOLIDASI HARRY1927**\n🌐 Target: {links[0]}\n\n"
    for i, r in enumerate(results): 
        report += f"👤 **UNIT-{i+1}:**\n{r}\n\n"
    
    if len(report) > 4000:
        for i in range(0, len(report), 4000): 
            await m.answer(report[i:i+4000])
    else: 
        await st.edit_text(report, disable_web_page_preview=True)

@dp.message()
async def handler_chat(m: Message):
    if m.from_user.id != OWNER_ID: return
    ans = await bolu.eksekusi_dewa(m.text, "Mode Interaksi", 0, mode="chat")
    await m.answer(ans)

async def main():
    scheduler.add_job(hunting_cuan_otomatis, 'interval', hours=1)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print(f">>> BOLU V13.1 SUPREME ONLINE | {len(GROQ_KEYS)} KUNCI AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
