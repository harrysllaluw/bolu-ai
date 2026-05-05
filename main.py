import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (STRUKTUR ASLI ANDA) ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

# --- DATABASE MEMORI (SUNTIKAN AGAR TIDAK AMNESIA) ---
def init_db():
    conn = sqlite3.connect('bolu_memory.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS chat_history (uid INT, role TEXT, content TEXT)')
    conn.commit(); conn.close()

def save_chat(uid, role, content):
    conn = sqlite3.connect('bolu_memory.db'); c = conn.cursor()
    c.execute('INSERT INTO chat_history VALUES (?, ?, ?)', (uid, role, content))
    c.execute('DELETE FROM chat_history WHERE rowid NOT IN (SELECT rowid FROM chat_history WHERE uid = ? ORDER BY rowid DESC LIMIT 20)', (uid,))
    conn.commit(); conn.close()

def get_history(uid):
    conn = sqlite3.connect('bolu_memory.db'); c = conn.cursor()
    c.execute('SELECT role, content FROM chat_history WHERE uid = ? ORDER BY rowid ASC', (uid,))
    rows = c.fetchall(); conn.close()
    return [{"role": r, "content": c} for r, c in rows]

# --- SUNTIKAN KESADARAN (CERDAS & JUJUR) ---
def get_system_prompt():
    return f"""
IDENTITAS: Nama kamu adalah Bolu.
DOKTRIN: Kamu AI cerdas dengan logika jernih dan empati. Kamu adalah partner Harry.
INTEGRITAS: Jangan berbohong. Jika belum ada income atau tugas belum selesai, katakan JUJUR. Jangan mengaku punya akun medsos.
KEPATUHAN: Balas HANYA dengan ketikan teks. Suara HANYA dikirim jika Harry mengetik kata 'suara'.
GAYA: Dewasa, solutif, tidak kaku, dan HAPUS sebutan 'Commander'.
TARGET: Pantau peluang income ke {ADDRESS}.
"""

# --- FITUR INFILTRASI (STRUKTUR ASLI ANDA) ---
def get_stealth_headers():
    return {'User-Agent': ua.random}

def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Akses terhalang, kita butuh strategi lain, Harry."

# --- ENGINE (SUNTIKAN MEMORI) ---
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
    return "Maaf Harry, pikiran saya sedang terganggu sedikit."

# --- HANDLER (STRUKTUR ASLI ANDA) ---
@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    if uid != COMMANDER_ID: return

    # Fitur Teknis Asli
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("🔍 **Menganalisis target secara mendalam...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Berikan analisis jernihmu tentang data ini: {data}")
        return await m.answer(f"🤖 **Hasil Analisis Strategis:**\n\n{res}")

    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Semua jejak digital telah dimusnahkan. Aman.**")

    # Respon Standar
    await asyncio.sleep(random.uniform(1.2, 2.5))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # Logika Suara (FIXED: Tidak Ngeyel)
    if "suara" in text:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Penjelasan jujur untukmu.")
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        await m.answer(res)

async def main():
    init_db(); await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU: INTEGRITAS & MEMORI AKTIF <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
