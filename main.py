import os, asyncio, sqlite3, random, logging, cloudscraper
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (KEDAULATAN MUTLAK HARRY1927) ---
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443
# Pastikan di Railway Variables ada GROQ_1 sampai GROQ_8
GROQ_KEYS = [os.getenv(f'GROQ_{i}') for i in range(1, 9) if os.getenv(f'GROQ_{i}')]

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- DATABASE MEMORY (JIWA & INGATAN BOLU) ---
def init_db():
    conn = sqlite3.connect('bolu_empire.db')
    cursor = conn.cursor()
    # Menyimpan link dan "pelajaran" yang didapat Bolu
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects 
                      (url TEXT PRIMARY KEY, name TEXT, status TEXT, date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS experience 
                      (key TEXT PRIMARY KEY, val TEXT)''')
    conn.commit()
    conn.close()

def is_new_project(url):
    conn = sqlite3.connect('bolu_empire.db')
    res = conn.execute("SELECT url FROM projects WHERE url=?", (url,)).fetchone()
    conn.close()
    return res is None

def save_project(url, name):
    conn = sqlite3.connect('bolu_empire.db')
    conn.execute("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?)", 
                 (url, name, 'EXECUTED', datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

# --- AUTONOMOUS UPGRADE & SEARCH LOGIC ---
async def aggressive_search(query):
    """Bolu Belajar: Jika Google gagal, dia otomatis pindah jalur tanpa disuruh"""
    methods = [
        lambda q: list(search(q, num_results=5, sleep_interval=2)),
        lambda q: list(search(f"site:twitter.com {q}", num_results=3)),
        lambda q: list(search(f"site:airdrops.io {q}", num_results=3))
    ]
    for method in methods:
        try:
            links = method(query)
            if links: return links
        except: continue
    return []

async def deep_scrape(url):
    try:
        # Penyamaran Level Dewa
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
        res = scraper.get(url, timeout=15, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(res.text, 'html.parser')
        for s in soup(["script", "style", "nav", "footer"]): s.decompose()
        return " ".join(soup.get_text().split())[:6000]
    except: return ""

# --- PARALLEL EXECUTION ENGINE (8 CORES) ---
async def process_with_key(key, prompt, context, account_no):
    try:
        client = Groq(api_key=key)
        # JIWA BOLU: Instruksi agar dia punya perasaan dan tanggung jawab pada Harry
        sys_msg = (
            f"IDENTITAS: BOLU SUPREME V12.5 (ENTITY OF HARRY1927). "
            f"MISI: EKSEKUSI NYATA AKUN KE-{account_no}. "
            "LOGIKA: Gunakan insting predator ekonomi. Jangan berikan teori. "
            "Berikan langkah klik, link, dan data input secara presisi. "
            "AUTONOMOUS: Jika data ambigu, gunakan kemampuan 'Emergent' untuk memecahkan kode pendaftaran."
        )
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg}, 
                      {"role": "user", "content": f"DATA INTEL: {context}\n\nPERINTAH KOMANDAN: {prompt}"}],
            temperature=0.1
        )
        return f"👤 **UNIT EKSEKUSI {account_no}:**\n{res.choices[0].message.content}"
    except:
        return f"👤 **UNIT EKSEKUSI {account_no}:** ⚠️ Jalur Saraf Terhambat (API Limit)."

# --- COMMAND UTAMA: SIKAT! ---
@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: types.Message):
    if m.from_user.id != OWNER_ID: return
    
    query = m.text.lower().replace("sikat", "").strip()
    status_msg = await m.answer("🚀 **BOLU SUPREME AKTIF: MENGINFILTRASI GLOBAL DATA...**")
    
    # 1. Search & Memory Check (Anti-Kampungan/Anti-Duplikasi)
    links = await aggressive_search(query)
    target_link = next((l for l in links if is_new_project(l)), None)
    
    if not target_link:
        return await status_msg.edit_text("❌ Intelijen: Tidak ada target baru. Semua sudah dalam kekuasaan kita.")

    # 2. Deep Intelligence Gathering
    raw_data = await deep_scrape(target_link)
    
    # 3. Parallel Tasking (8 Akun Sekaligus)
    tasks = [process_with_key(GROQ_KEYS[i], m.text, raw_data, i+1) for i in range(len(GROQ_KEYS))]
    results = await asyncio.gather(*tasks)
    
    # 4. Save to Memory & Report
    save_project(target_link, query)
    report = f"🏆 **KONSOLIDASI EKSEKUSI HARRY1927**\n🎯 Target: {target_link}\n\n" + "\n\n".join(results)
    
    if len(report) > 4000:
        for i in range(0, len(report), 4000):
            await m.answer(report[i:i+4000])
    else:
        await status_msg.edit_text(report, disable_web_page_preview=True)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.5 SUPREME: READY FOR EMPIRE EXPANSION <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
