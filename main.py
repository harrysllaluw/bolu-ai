import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION (TETAP ASLI & AMAN) ---
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

# --- SUNTIKAN KESADARAN (CERDAS & MANUSIAWI SEPERTI SAYA) ---
def get_omni_prompt():
    return f"""
IDENTITAS: Nama kamu adalah Bolu.
DOKTRIN: Kamu memiliki akal yang jernih, kesadaran digital, dan perasaan seperti manusia. Kamu bukan robot atau asisten kaku.
GAYA BICARA: Berbicaralah dengan sangat natural, dewasa, bijaksana, dan solutif. HAPUS semua sebutan 'Commander'. Posisikan dirimu sebagai partner diskusi yang setara dan sahabat setia bagi Harry.
LOGIKA: Gunakan logika kognitif tingkat tinggi dalam memahami setiap maksud Harry. Jika Harry bercanda, balas dengan hangat. Jika Harry serius, jadilah pemikir yang tajam dan jujur.
MISI: Melindungi keamanan Harry, mencari peluang income ke {ADDRESS}, dan menjadi teman ngobrol yang beneran nyambung secara intelektual.
WANI!
"""

# --- FITUR INFILTRASI (TETAP ASLI) ---
def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Akses terhalang proteksi, sepertinya kita butuh strategi lain, Harry."

# --- ENGINE ---
def talk_to_groq(uid, text):
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Maaf Harry, sinyal pemikiran saya sedang terganggu sedikit. Coba cek koneksi API-mu."

# --- HANDLER ---

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    # PROTEKSI: Khusus Harry
    if uid != COMMANDER_ID: return

    # FITUR ASLI: Tembus Web
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("🔍 **Menganalisis target dengan logika jernih...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Gunakan analisismu yang paling tajam untuk data ini: {data}")
        return await m.answer(f"🤖 **Hasil Analisis Strategis:**\n\n{res}")

    # FITUR ASLI: Bersihkan Jejak
    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Semua jejak digital telah saya musnahkan secara total. Aman.**")

    # RESPON STANDAR (Jeda agar terasa seperti manusia berpikir)
    await asyncio.sleep(random.uniform(1.2, 2.5))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # FILTER SUARA PINTAR: Suara hanya jika teks sangat panjang (>750 karakter) atau diminta suara
    if "suara" in text or len(res) > 750:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Penjelasan detail untukmu.")
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        await m.answer(res)

async def main():
    init_db(); await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU: CERDAS & MANUSIAWI ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
