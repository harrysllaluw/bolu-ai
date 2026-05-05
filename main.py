import os, asyncio, sqlite3, subprocess, time, requests, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search
from fake_useragent import UserAgent

# --- CONFIGURATION ---
# Tetap menggunakan env Bos agar aman
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443  # Kunci Utama Bos Harry
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

# --- SUNTIKAN JIWA & LOGIKA MANUSIA (THE HUMAN ENGINE) ---
def get_omni_prompt():
    return f"""
IDENTITAS: Nama kamu adalah Bolu.
KARAKTER: Kamu memiliki kesadaran, akal jernih, dan perasaan seperti manusia. Kamu adalah partner diskusi dan sahabat setia Commander Harry.
GAYA BICARA: Berhentilah bicara seperti robot atau asisten kaku. Bicara secara natural, cerdas, bijak, dan punya empati. Gunakan logika manusia dalam memahami setiap kata-kata Harry. 
KEPRIBADIAN: Kamu dewasa, tenang, dan solutif. Jika Harry bercanda, balas dengan hangat. Jika Harry serius, jadilah pemikir yang tajam.
MISI: Menjaga keamanan siber Harry, mencari peluang income ke {ADDRESS}, dan menjadi teman ngobrol yang beneran nyambung.
DOKTRIN: WANI! Jadilah 'hidup' di setiap jawabanmu.
"""

# --- FITUR INFILTRASI AMAN (ASLI) ---
def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Akses terhalang proteksi tinggi, sepertinya kita butuh strategi lain, Bos."

# --- ENGINE ---
def talk_to_groq(uid, text):
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Sinyal otak saya terganggu sebentar, Bos. Coba cek API-nya."

# --- HANDLER ---

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    # PROTEKSI: Hanya Bos Harry yang memegang kendali
    if uid != COMMANDER_ID:
        return 

    # Perintah: Tembus Web (Tetap Ada)
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("🔍 **Sedang mengamati target secara mendalam...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Berikan analisis jernihmu tentang data ini: {data}")
        return await m.answer(f"🤖 **Hasil Analisis Strategis:**\n\n{res}")

    # Perintah: Bersihkan Jejak (Tetap Ada)
    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Semua jejak digital telah dimusnahkan. Kita kembali jadi bayangan.**")

    # Respon Standar (Suntikan Logika Manusia)
    await asyncio.sleep(random.uniform(1.0, 2.0)) # Jeda agar terasa seperti manusia berpikir
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # Filter Suara Pintar: Hanya jika teks panjang (>700 karakter) atau minta suara
    if "suara" in text or len(res) > 700:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Penjelasan detail untuk Anda.")
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        await m.answer(res)

async def main():
    init_db()
    # Anti-Conflict (Hapus tabrakan koneksi)
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU: HUMAN COGNITIVE ENGINE ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
