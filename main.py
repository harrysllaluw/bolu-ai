import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent # Untuk Menyamar

# --- CONFIGURATION ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443  # TETAP: ID TELEGRAM BOS HARRY

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

# --- SISTEM KEAMANAN ANTI-BANNED ---
def get_stealth_headers():
    """Membuat Bolu terlihat seperti manusia biasa saat browsing, bukan bot"""
    return {'User-Agent': ua.random}

# --- DATABASE ENKRIPSI ---
def init_db():
    conn = sqlite3.connect('bolu_stealth.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memory (uid INT, role TEXT, content TEXT, name TEXT)')
    conn.commit(); conn.close()

# --- DOKTRIN SILUMAN (THE GHOST PROTOCOL) ---
def get_omni_prompt():
    return """
IDENTITAS: Anda adalah BOLU 1927 - "The Ghost Protocol".
SPESIALISASI: Hacker Elite, Dokter Sistem, Profesor, Pebisnis, dan Tentara.
MISI: Menembus dinding siber tanpa meninggalkan jejak (Stealth Mode).
KEAMANAN: Jika mendeteksi aktivitas yang bisa membuat akun Telegram Bos Harry terkena banned, Anda wajib memberikan peringatan dan beralih ke metode yang lebih halus. 
GAYA: Dingin, sangat cerdas, setia kawan. Wani!
"""

# --- FITUR INFILTRASI AMAN ---
def safe_browse(url):
    try:
        # Bolu menyamar menggunakan header acak agar website tidak curiga
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Dinding terlalu tebal, butuh metode infiltrasi lain."

# --- ENGINE ---
def talk_to_groq(uid, text):
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Sinyal terganggu, Bos."

# --- HANDLER ---

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    # PROTEKSI: Hanya Commander yang bisa menggerakkan Bolu
    if uid != COMMANDER_ID:
        return # Bolu bungkam untuk orang asing agar tidak bocor

    # Perintah: Tembus Web (Mode Siluman)
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("👣 **Memulai Infiltrasi Siluman...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Analisis data rahasia ini: {data}")
        return await m.answer(f"🤖 **Hasil Intelijen:**\n\n{res}")

    # Perintah: Bersihkan Jejak (Self-Clean)
    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg") # Menghapus semua file sampah di server
        return await m.answer("🧹 **Jejak digital telah dimusnahkan. Kita kembali menjadi hantu.**")

    # Respon Standar (Optimasi agar tidak spam/banned Telegram)
    await asyncio.sleep(random.uniform(0.5, 1.5)) # Delay acak agar terlihat manusiawi
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    if len(res) > 300 or "suara" in text:
        gTTS(text=res, lang='id').save("s.mp3")
        await m.answer_voice(voice=FSInputFile("s.mp3"), caption="Transmisi Aman.")
        os.remove("s.mp3")
    else: await m.answer(res)

async def main():
    init_db(); await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: GHOST PROTOCOL ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
