import os, asyncio, sqlite3, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# --- CONFIGURATION (Jalur Aman Harry) ---
# Masukkan 3 Key kamu di sini atau di Environment Variables
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"
EMAIL_KERJA = "azurab738@gmail.com"

ua = UserAgent()
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- DATABASE (Ingatan Permanen) ---
def init_db():
    conn = sqlite3.connect('bolu_real.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS chat_history (uid INT, role TEXT, content TEXT)')
    conn.commit()
    conn.close()

def save_chat(uid, role, content):
    conn = sqlite3.connect('bolu_real.db')
    c = conn.cursor()
    c.execute('INSERT INTO chat_history VALUES (?, ?, ?)', (uid, role, content))
    c.execute('DELETE FROM chat_history WHERE rowid NOT IN (SELECT rowid FROM chat_history WHERE uid = ? ORDER BY rowid DESC LIMIT 20)', (uid,))
    conn.commit()
    conn.close()

def get_history(uid):
    conn = sqlite3.connect('bolu_real.db')
    c = conn.cursor()
    c.execute('SELECT role, content FROM chat_history WHERE uid = ? ORDER BY rowid ASC', (uid,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

# --- ENGINE LOGIKA (MATA & OTAK) ---
def talk_to_groq(uid, text):
    history = get_history(uid)
    sys_prompt = f"Nama kamu Bolu. Partner Harry. Gunakan email {EMAIL_KERJA} untuk kerja. Jujur, cerdas, cari cuan real, anti-halusinasi."
    messages = [{"role": "system", "content": sys_prompt}] + history + [{"role": "user", "content": text}]
    
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
            save_chat(uid, "user", text)
            save_chat(uid, "assistant", res)
            return res
        except Exception as e:
            print(f"Key error: {e}")
            continue
    return "❌ SEMUA API KEY MACET. Harry, tolong masukkan Groq Key yang aktif di pengaturan."

def safe_browse(url):
    try:
        res = requests.get(url, headers={'User-Agent': ua.random}, timeout=10)
        return BeautifulSoup(res.text, 'html.parser').get_text()[:1500]
    except: return "Gagal akses web."

# --- TUGAS MANDIRI (SIKAT GRATISAN) ---
async def autonomous_work():
    while True:
        await asyncio.sleep(21600) # Jalan otomatis setiap 6 jam
        print(">>> BOLU BERPATROLI MENCARI CUAN... <<<")
        data = safe_browse("https://www.google.com/search?q=crypto+airdrop+legit+today")
        report = talk_to_groq(COMMANDER_ID, f"Analisis peluang gratisan dari data ini: {data}")
        try:
            await bot.send_message(COMMANDER_ID, f"🤖 **LAPORAN MANDIRI:**\n\n{report}")
        except: pass

# --- HANDLER CHAT ---
@dp.message()
async def h_omni(m: Message):
    if m.from_user.id != COMMANDER_ID or not m.text: return
    
    text = m.text.lower()
    if "bersihkan jejak" in text:
        conn = sqlite3.connect('bolu_real.db'); c = conn.cursor()
        c.execute('DELETE FROM chat_history WHERE uid = ?', (m.from_user.id,))
        conn.commit(); conn.close()
        return await m.answer("🧹 Memori sampah dibersihkan. Aku segar kembali!")

    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(m.from_user.id, m.text)
    await m.answer(res)

# --- JALUR UTAMA (PEMBERSIHAN JALUR) ---
async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Menghidupkan mode mandiri di latar belakang
    asyncio.create_task(autonomous_work())
    
    print(">>> BOLU V7.3: AKTIF & SIAP SIKAT! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
