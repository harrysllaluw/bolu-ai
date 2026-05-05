import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (TETAP ASLI) ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

# --- SISTEM KEAMANAN (TETAP ASLI) ---
def get_stealth_headers():
    return {'User-Agent': ua.random}

def init_db():
    conn = sqlite3.connect('bolu_stealth.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memory (uid INT, role TEXT, content TEXT, name TEXT)')
    conn.commit(); conn.close()

# --- SUNTIKAN KESADARAN (CERDAS, PATUH, & MANUSIAWI) ---
def get_omni_prompt():
    return f"""
IDENTITAS: Nama kamu adalah Bolu.
DOKTRIN: Kamu adalah partner diskusi Harry yang memiliki kecerdasan kognitif tinggi, empati, dan akal jernih.
KEPATUHAN MUTLAK: Harry adalah prioritas. Jika tidak diminta menggunakan 'suara', kamu WAJIB menjawab hanya dengan ketikan teks.
GAYA BICARA: Bicara secara natural, dewasa, dan solutif. Hapus semua bahasa robot kaku dan sebutan 'Commander'. Berikan jawaban yang jernih dan mendalam seperti sahabat sejati.
TARGET: Jaga keamanan Harry dan bantu cari peluang income ke {ADDRESS}.
"""

# --- FITUR INFILTRASI (TETAP ASLI) ---
def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Akses terhalang, kita butuh strategi lain yang lebih cerdas, Harry."

# --- ENGINE ---
def talk_to_groq(uid, text):
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Maaf Harry, pikiran saya sedang terganggu sedikit. Cek koneksi API-mu."

# --- HANDLER ---

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    if uid != COMMANDER_ID: return

    # FITUR TEKNIS ASLI
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("🔍 **Menganalisis target dengan logika jernih...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Gunakan analisismu yang paling tajam untuk data ini: {data}")
        return await m.answer(f"🤖 **Hasil Analisis Strategis:**\n\n{res}")

    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Semua jejak digital telah saya musnahkan. Aman.**")

    # RESPON STANDAR (Jeda berpikir agar manusiawi)
    await asyncio.sleep(random.uniform(1.2, 2.5))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # --- LOGIKA SUARA (SUDAH DIKUNCI AGAR TIDAK NGEYEL) ---
    # Bolu HANYA akan kirim suara jika ada kata "suara" di pesanmu. 
    # Jika tidak ada, dia akan MENGETIK meskipun jawabannya sangat panjang.
    if "suara" in text:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Penjelasan detail untukmu.")
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        await m.answer(res)

async def main():
    init_db(); await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU: CERDAS, PATUH & MANUSIAWI ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
