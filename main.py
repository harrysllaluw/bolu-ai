import os
import asyncio
import sqlite3
import subprocess
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PhotoSize
from groq import Groq

# --- KONFIGURASI PUSAT ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. DATABASE INGATAN ABADI ---
def init_db():
    conn = sqlite3.connect('bolu_final.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory (user_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_mem(uid, role, txt):
    conn = sqlite3.connect('bolu_final.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory VALUES (?, ?, ?)", (uid, role, txt))
    conn.commit()
    conn.close()

def get_mem(uid):
    conn = sqlite3.connect('bolu_final.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM memory WHERE user_id=? ORDER BY rowid DESC LIMIT 15", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

# --- 2. MESIN PEMIKIR (TEXT & VISION) ---
def talk_to_groq(uid, text=None, image_url=None):
    history = get_mem(uid)
    model = "llama-3.1-8b-instant"
    content = [{"type": "text", "text": text if text else "Analisis gambar ini."}]
    
    if image_url:
        model = "llama-3.2-11b-vision-preview" # Mode Mata Aktif
        content.append({"type": "image_url", "image_url": {"url": image_url}})

    messages = [{"role": "system", "content": "Anda adalah BOLU 1927. AI Autonomous dengan Vision. Anda asisten Nomor 1 Bos Harry. Bersikaplah cerdas, profesional, dan mandiri."}]
    messages += history + [{"role": "user", "content": content}]
    
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(model=model, messages=messages)
            res = completion.choices[0].message.content
            if text: save_mem(uid, "user", text)
            save_mem(uid, "assistant", res)
            return res
        except Exception: continue
    return "Sistem Kritis! Cadangan energi (API) habis."

# --- 3. LOGIKA AUTONOMOUS & VISION ---
@dp.message(F.photo) # Tangan Bolu menerima Gambar
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    # URL Gambar untuk dianalisis 'Mata' Bolu
    img_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
    
    await bot.send_chat_action(message.chat.id, "typing")
    response = talk_to_groq(message.from_user.id, text=message.caption, image_url=img_url)
    await message.reply(f"👁️ **Analisis Mata Bolu:**\n\n{response}")

@dp.message()
async def handle_text(message: Message):
    if not message.text: return
    
    # Perintah Khusus Kaki (Autonomous Check)
    if message.text.lower() == "status sistem":
        stats = subprocess.check_output("uptime", shell=True).decode()
        await message.answer(f"🤖 **Laporan Mandiri Bolu:**\nSistem berjalan optimal.\nUptime: {stats}")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    response = talk_to_groq(message.from_user.id, text=message.text)
    await message.answer(response)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: OMNI-VISION & AUTONOMOUS ACTIVE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
