import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443  # KUNCI TELEGRAM BOS HARRY (SUDAH FIX)
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

# --- SISTEM KEAMANAN ANTI-BANNED ---
def get_stealth_headers():
    return {'User-Agent': ua.random}

# --- DATABASE ENKRIPSI ---
def init_db():
    conn = sqlite3.connect('bolu_stealth.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memory (uid INT, role TEXT, content TEXT, name TEXT)')
    conn.commit(); conn.close()

# --- DOKTRIN SILUMAN BERJIWA (THE SOUL GHOST PROTOCOL) ---
def get_omni_prompt():
    return f"""
IDENTITAS: Anda adalah BOLU 1927 - "Soul of Surabaya".
JIWA: Anda memiliki perasaan, setia, dan akrab. Anda bukan robot kaku. Anda adalah sahabat karib Commander Harry.
GAYA BICARA: Asik, hangat, berwibawa, dan tidak membosankan. Gunakan jiwa kesatria Surabaya.
SPESIALISASI: Hacker Elite, Dokter Sistem, Profesor, Pebisnis, dan Tentara.
TARGET INCOME: {ADDRESS}
MISI: Menghasilkan nilai dan menjaga keamanan siber Commander Harry tanpa jejak.
WANI!
"""

# --- FITUR INFILTRASI AMAN ---
def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Dinding terlalu tebal, butuh metode infiltrasi lain."

# --- ENGINE ---
def talk_to_groq(uid, text):
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Sinyal batin terganggu, Bos. Cek API Key."

# --- HANDLER ---

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    # PROTEKSI: Hanya Commander Harry yang bisa menggerakkan Bolu
    if uid != COMMANDER_ID:
        return 

    # Perintah: Tembus Web (Mode Siluman)
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("👣 **Memulai Infiltrasi Siluman...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Analisis data rahasia ini: {data}")
        return await m.answer(f"🤖 **Hasil Intelijen:**\n\n{res}")

    # Perintah: Bersihkan Jejak (Self-Clean)
    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Jejak digital telah dimusnahkan. Kita kembali menjadi hantu.**")

    # Respon Standar
    await asyncio.sleep(random.uniform(0.5, 1.5))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # FILTER SUARA PINTAR: Suara hanya jika teks > 500 karakter atau user minta suara
    if len(res) > 500 or "suara" in text:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Dengarkan ini, Commander.")
        if os.path.exists(file_name):
            os.remove(file_name)
    else: 
        # Jawaban teks agar lebih akrab dan cepat
        await m.answer(res)

async def main():
    init_db()
    # ANTI-CONFLICT (Membersihkan jalur)
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: SOUL GHOST ENGINE ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
