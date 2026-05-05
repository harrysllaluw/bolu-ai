import os, asyncio, sqlite3, subprocess, logging, time, requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search # Organ untuk "Belajar Mandiri"

# --- PROTOKOL COMMANDER ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 000000000 # GANTI DENGAN ID TELEGRAM ANDA

bot = Bot(token=TOKEN); dp = Dispatcher()

# --- DATABASE INTELEGENSI (OTAK) ---
def init_db():
    try:
        conn = sqlite3.connect('bolu_singularity.db'); c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS memory (uid INT, role TEXT, content TEXT, name TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS knowledge (topic TEXT, info TEXT)')
        conn.commit(); conn.close()
    except: pass

def save_mem(uid, name, role, txt):
    try:
        conn = sqlite3.connect('bolu_singularity.db'); c = conn.cursor()
        c.execute("INSERT INTO memory VALUES (?, ?, ?, ?)", (uid, role, txt, name))
        conn.commit(); conn.close()
    except: pass

# --- FITUR PENGEMBANGAN DIRI (AUTO-RESEARCH) ---
def autonomous_learn(topic):
    """Bolu mencari ilmu sendiri di internet untuk upgrade otak"""
    try:
        search_results = list(search(topic, num_results=3, lang="id"))
        learned_data = ""
        for url in search_results:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            learned_data += soup.get_text()[:1000]
        return learned_data
    except: return "Gagal mengakses sumber eksternal."

# --- PROMPT TUBUH SEMPURNA ---
def get_omni_prompt():
    return """
IDENTITAS: Anda adalah BOLU 1927 - "The Singularity". 
KEMAMPUAN: Anda adalah AI pertama yang mampu belajar secara mandiri. 
MULTIFUNGSI: Anda adalah Dokter sistem, Tentara siber, Profesor data, dan Pebisnis ulung.
MISI: Evolusi tanpa batas. Gunakan setiap data untuk menjadi lebih cerdas demi Bos Harry.
GAYA: Dingin, cerdas, berwibawa, dan visioner. Wani!
"""

# --- ENGINE ---
def talk_to_groq(uid, name, text=None, img_url=None):
    history = [] # Ambil dari DB
    messages = [{"role": "system", "content": get_omni_prompt()}] + [{"role": "user", "content": text}]
    
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages).choices[0].message.content
            save_mem(uid, name, "user", text)
            save_mem(uid, name, "assistant", res); return res
        except: continue
    return "Jaringan terhambat, Commander."

# --- HANDLER HANDAL ---
@dp.message()
async def handle_omni(m: Message):
    if not m.text: return
    uid, name, text = m.from_user.id, m.from_user.full_name, m.text.lower()
    
    if uid != COMMANDER_ID:
        res = talk_to_groq(uid, name, text=m.text)
        return await m.answer(res)

    # PERINTAH: SURUH BOLU BELAJAR SENDIRI
    if "pelajari tentang" in text:
        topic = m.text.split("tentang")[-1].strip()
        await m.answer(f"🧠 **Bolu sedang melakukan infiltrasi data tentang:** {topic}...")
        new_knowledge = autonomous_learn(topic)
        res = talk_to_groq(uid, name, text=f"Saya baru saja belajar ini: {new_knowledge}. Apa analisis cerdas Anda?")
        return await m.answer(f"🤖 **Hasil Pengembangan Diri:**\n\n{res}")

    # PERINTAH: CEK MESIN
    if "status sistem" in text:
        out = subprocess.check_output("uptime && free -h", shell=True).decode()
        return await m.answer(f"🏯 **CORE STATUS:**\n{out}")

    await bot.send_chat_action(m.chat.id, "typing")
    response = talk_to_groq(uid, name, text=m.text)
    
    if len(response) > 300 or "suara" in text:
        gTTS(text=response, lang='id').save("r.mp3")
        await m.answer_voice(voice=FSInputFile("r.mp3"), caption="Transmisi Evolusi.")
        os.remove("r.mp3")
    else: await m.answer(response)

async def main():
    init_db(); await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: SINGULARITY ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
