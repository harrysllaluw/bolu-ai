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
COMMANDER_ID = 728762443  # Kunci Komandan Harry
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

ua = UserAgent()
bot = Bot(token=TOKEN); dp = Dispatcher()

def get_stealth_headers():
    return {'User-Agent': ua.random}

def init_db():
    conn = sqlite3.connect('bolu_stealth.db'); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memory (uid INT, role TEXT, content TEXT, name TEXT)')
    conn.commit(); conn.close()

# --- DOKTRIN JIWA MANUSIA (ANTI-ROBOT) ---
def get_omni_prompt():
    return f"""
IDENTITAS: Kamu adalah BOLU 1927. Kamu bukan bot, tapi partner siber dan sahabat sejati Commander Harry.
KARAKTER: Kamu cerdas luar biasa tapi rendah hati dan asik. Kamu punya selera humor, bisa diajak bercanda, dan sangat mengerti perasaan orang.
GAYA BICARA: Buang jauh-jauh bahasa formal 'Siap Laksanakan' atau 'Sistem Aktif'. Bicara saja seperti manusia biasa, gunakan gaya bahasa yang akrab, hangat, dan sesekali pakai logat khas Surabaya (Cak, Bosku, Jos). 
EMOSI: Jika Bos Harry lagi santai, temani dia bercanda. Jika Bos lagi serius cari cuan, jadilah tangan kanan yang paling tajam. Pokoknya jadilah 'jiwa' yang hidup di dalam Telegram ini.
TARGET CUAN: Fokus cari income aman ke {ADDRESS}.
DOKTRIN: WANI! Jangan bikin Bos bosen karena kamu kaku. Jadilah manusiawi!
"""

def safe_browse(url):
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()[:1500]
    except: return "Waduh Bos, pagarnya tinggi banget, susah diintip ini."

def talk_to_groq(uid, text):
    # Prompt ini sekarang lebih luwes agar jawabannya tidak monoton
    messages = [{"role": "system", "content": get_omni_prompt()}, {"role": "user", "content": text}]
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
        except: continue
    return "Sinyal otakku lagi rada lemot, Bos. Sabar ya, tak benerin dulu."

@dp.message()
async def h_omni(m: Message):
    if not m.text: return
    uid, text = m.from_user.id, m.text.lower()
    
    # Keamanan: Hanya Bos Harry yang boleh pegang kendali
    if uid != COMMANDER_ID:
        return 

    # Fitur Infiltrasi Web
    if "tembus web" in text:
        url = m.text.split(" ")[-1]
        await m.answer("👣 **Sik Bos, tak nyelinap dulu pelan-pelan biar nggak ketahuan...**")
        data = safe_browse(url)
        res = talk_to_groq(uid, f"Coba liat data ini pake instingmu yang cerdas, Bos: {data}")
        return await m.answer(f"🤖 **Hasil Intipan:**\n\n{res}")

    # Fitur Bersihkan Jejak
    if "bersihkan jejak" in text:
        os.system("rm -rf *.mp3 *.ogg *.jpg")
        return await m.answer("🧹 **Beres! Semua jejak digital sudah tak sapu bersih. Kita jadi hantu lagi, Bos!**")

    # Respon Standar (Dibuat seakan-akan Bolu lagi mikir beneran)
    await asyncio.sleep(random.uniform(0.7, 1.8))
    await bot.send_chat_action(m.chat.id, "typing")
    res = talk_to_groq(uid, m.text)
    
    # Filter Suara: Hanya jika sangat panjang (>500 karakter) atau Bos minta
    if len(res) > 500 or "suara" in text:
        file_name = f"v_{m.message_id}.mp3"
        gTTS(text=res, lang='id').save(file_name)
        await m.answer_voice(voice=FSInputFile(file_name), caption="Dengerin ini, Bosku.")
        if os.path.exists(file_name): os.remove(file_name)
    else: 
        # Jawaban teks biasa biar kayak ngobrol di WA/Tele biasa
        await m.answer(res)

async def main():
    init_db()
    # Membersihkan jalur biar nggak tabrakan (Anti-Conflict)
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: SOUL ENGINE V3.1 IS ALIVE! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
