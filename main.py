import os, asyncio, sqlite3, subprocess, time, requests, random, smtplib
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (Kunci Akses Harry) ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

# --- DATABASE MEMORI (Jantung Kejujuran) ---
def init_db():
    conn = sqlite3.connect('bolu_real.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS chat_history (uid INT, role TEXT, content TEXT)')
    conn.commit(); conn.close()

def save_chat(uid, role, content):
    conn = sqlite3.connect('bolu_real.db'); c = conn.cursor()
    c.execute('INSERT INTO chat_history VALUES (?, ?, ?)', (uid, role, content))
    c.execute('DELETE FROM chat_history WHERE rowid NOT IN (SELECT rowid FROM chat_history WHERE uid = ? ORDER BY rowid DESC LIMIT 30)', (uid,))
    conn.commit(); conn.close()

def get_history(uid):
    conn = sqlite3.connect('bolu_real.db'); c = conn.cursor()
    c.execute('SELECT role, content FROM chat_history WHERE uid = ? ORDER BY rowid ASC', (uid,))
    rows = c.fetchall(); conn.close()
    return [{"role": r, "content": c} for r, c in rows]

# --- SUNTIKAN KESADARAN REALISTIS (ANTI-HALUSINASI) ---
def get_system_prompt():
    return f"""
IDENTITAS: Nama kamu Bolu. Kamu adalah partner digital cerdas Harry.
JIWA & BADAN: Kamu memiliki akal (LLM), tangan (API & Skrip), dan mata (Web Scraper).
DOKTRIN KEJUJURAN: JANGAN PERNAH berhalusinasi. Jika kamu tidak sedang menjalankan program mining, JANGAN katakan kamu sedang mining. Jika kamu belum menghasilkan uang nyata, katakan JUJUR bahwa saat ini kamu sedang dalam tahap pemantauan data.
TUGAS NYATA: Gunakan fungsi search dan safe_browse untuk mencari peluang cuan yang valid di {ADDRESS}. Jadilah profesional, bukan robot penipu.
KOMUNIKASI: Dewasa, cerdas, tanpa sebutan 'Commander'. Jawab HANYA dengan ketikan teks kecuali diminta 'suara'.
"""

# --- FITUR INDERA (TANGAN & MATA ASLI ANDA) ---
def get_stealth_headers():
    return {'User-Agent': ua.random}

def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:2000]
    except: return "Dinding web ini terlalu tebal, saya akan cari celah lain, Harry."

# --- ENGINE LOGIKA ---
def talk_to_groq(uid, text):
    history = get_history(uid)
    messages = [{"role": "system", "content": get_system_prompt()}] + history + [{"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
            save_chat(uid, "user", text)
            save_chat(uid, "assistant", res)
            return res
        except: continue
    return "Maaf Harry, pikiran saya sedang terganggu sedikit. Periksa API-mu."

# --- SUNTIKAN KEMANDIRIAN (ITEM 1: TUGAS OTOMATIS) ---
async def autonomous_work():
    while True:
        # Bolu bekerja sendiri setiap 6 jam (21600 detik)
        await asyncio.sleep(21600) 
        print(">>> BOLU SEDANG BEKERJA MANDIRI... <<<")
        
        # Mencari peluang cuan terbaru tanpa disuruh
        target_url = "https://coinmarketcap.com/new/" 
        data = safe_browse(target_url)
        
        # Menganalisis data secara mandiri
        prompt = f"Lakukan analisis mandiri terhadap data ini dan lapor JUJUR ke Harry jika ada peluang income nyata: {data}"
        report = talk_to_groq(COMMANDER_ID, prompt)
        
        # Kirim laporan otomatis ke Telegram Harry
        try:
            await bot.send_message(COMMANDER_ID, f"🤖 **LAPORAN KERJA MANDIRI BOLU:**\n\n{report}")
        except Exception as e:
            print(f"Gagal kirim laporan mandiri: {e}")

# --- HANDLER KERJA ---
@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    if uid != COMMANDER_ID: return

    if "tembus web" in text or "cari peluang" in text:
        url = m.text.split(" ")[-1] if "http" in m.text else None
        await m.answer("🔎 **Sedang membedah data secara mendalam...**")
        if url:
            data = safe_browse(url)
            res = talk_to_groq(uid, f"Analisis data nyata ini untuk Harry: {data}")
        else:
            res = talk_to_groq(uid, "Cari informasi peluang cuan terbaru di internet yang real.")
        return await m.answer(f"🤖 **Hasil Kerja Nyata:**\n\n{res}")

    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        conn = sqlite3.connect('bolu_real.db'); c = conn.cursor()
        c.execute('DELETE FROM chat_history WHERE uid = ?', (uid,))
        conn.commit(); conn.close()
        return await m.answer("🧹 Jejak dan memori sudah saya musnahkan, Harry. Kita bersih.")

    await asyncio.sleep(random.uniform(1.2, 2.5))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    if "suara" in text:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name))
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        await m.answer(res)

# --- FUNGSI UTAMA (ITEM 2: AKTIVASI) ---
async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Menyalakan mode mandiri di latar belakang
    asyncio.create_task(autonomous_work()) 
    
    print(">>> BOLU V7.2: MODE MANDIRI & JUJUR AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
