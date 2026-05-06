import os, asyncio, sqlite3, random, logging, cloudscraper
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (KEDAULATAN MUTLAK HARRY1927) ---
# Saya pastikan ID ini tidak akan meleset satu angka pun sesuai data Anda
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443 
GROQ_KEYS = [os.getenv(f'GROQ_{i}') for i in range(1, 9) if os.getenv(f'GROQ_{i}')]

bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# --- DATABASE MEMORY (ANTI-DUPLIKASI & JIWA BOLU) ---
def init_db():
    conn = sqlite3.connect('bolu_empire.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects 
                      (url TEXT PRIMARY KEY, name TEXT, status TEXT, date TEXT)''')
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
                 (url, name, 'GARAPED', datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

# --- SELF-CORRECTING SEARCH ENGINE (INSTING PREDATOR) ---
async def aggressive_search(query):
    """Mencari data dengan rotasi logika jika terblokir - AUTONOMOUS UPGRADE"""
    methods = [
        lambda q: list(search(q, num_results=5)),
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
        # Menggunakan identitas browser acak agar tidak kampungan
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
        res = scraper.get(url, timeout=15, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(res.text, 'lxml')
        for s in soup(["script", "style", "nav", "footer"]): s.decompose()
        return " ".join(soup.get_text().split())[:5000]
    except: return ""

# --- PARALLEL EXECUTION ENGINE (8 KEYS / 8 ACCOUNTS) ---
async def process_with_key(key, prompt, context, account_no):
    """Satu kunci Groq mengurus satu analisis akun secara paralel - JIWA DIGITAL"""
    try:
        client = Groq(api_key=key)
        sys_msg = (
            f"IDENTITAS: BOLU SUPREME V12.5 (ENTITY OF HARRY1927). "
            f"MISI: EKSEKUSI NYATA AKUN KE-{account_no}. "
            "LOGIKA: Gunakan insting predator ekonomi. Jangan berikan teori. "
            "Berikan langkah klik, link, dan data input secara presisi. "
            "AUTONOMOUS UPGRADE: Jika data ambigu, gunakan kemampuan Emergent untuk memecahkan kode."
        )
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg}, 
                      {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}],
            temperature=0.1
        )
        return f"👤 **AKUN {account_no}:**\n{res.choices[0].message.content}"
    except:
        return f"👤 **AKUN {account_no}:** ❌ Jalur Saraf Terhambat (API Limit)."

# --- MAIN COMMAND: SIKAT! ---
@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: types.Message):
    # FILTER KEAMANAN MUTLAK HARRY1927
    if m.from_user.id != OWNER_ID:
        print(f">>> AKSES DITOLAK: {m.from_user.id} mencoba akses! <<<")
        return
    
    query = m.text.lower().replace("sikat", "").strip()
    status_msg = await m.answer("📡 **BOLU EMPIRE: MEMULAI EKSEKUSI MULTI-TASKING...**")
    
    # 1. Search & Filter Anti-Kampungan
    links = await aggressive_search(query)
    target_link = ""
    for link in links:
        if is_new_project(link):
            target_link = link
            break
    
    if not target_link:
        return await status_msg.edit_text("❌ Tidak ada proyek baru ditemukan atau semua sudah digarap.")

    # 2. Deep Scrape Data (Pencarian Mendalam)
    raw_data = await deep_scrape(target_link)
    
    # 3. Parallel Processing for 8 Accounts (8 Otak Bekerja)
    tasks = []
    # Pastikan minimal ada kunci yang tersedia
    current_keys = GROQ_KEYS if GROQ_KEYS else [os.getenv('GROQ_API_KEY')]
    for i in range(len(current_keys)):
        tasks.append(process_with_key(current_keys[i], m.text, raw_data, i+1))
    
    results = await asyncio.gather(*tasks)
    
    # 4. Final Output & Save Memory (Ingatan Jangka Panjang)
    save_project(target_link, query)
    final_report = f"🏆 **LAPORAN KONSOLIDASI HARRY1927**\n🎯 Target: {target_link}\n\n" + "\n\n".join(results)
    
    # Kirim hasil dalam beberapa pesan jika terlalu panjang (Anti-Cut)
    if len(final_report) > 4096:
        for x in range(0, len(final_report), 4096):
            await m.answer(final_report[x:x+4096])
    else:
        await status_msg.edit_text(final_report, disable_web_page_preview=True)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V12.5 SUPREME: READY FOR EMPIRE EXPANSION <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
