import os
import asyncio
import sqlite3
import subprocess
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq

# --- KONFIGURASI ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- SISTEM INGATAN ---
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

# --- MESIN UTAMA ---
def talk_to_groq(uid, text=None, img_url=None):
    history = get_mem(uid)
    model = "llama-3.1-8b-instant"
    user_content = [{"type": "text", "text": text if text else "Analisis ini."}]
    
    if img_url:
        model = "llama-3.2-11b-vision-preview"
        user_content.append({"type": "image_url", "image_url": {"url": img_url}})

    messages = [{"role": "system", "content": "Anda BOLU 1927, AI Autonomous canggih. Anda asisten Bos Harry yang cerdas, mandiri, dan sigap."}]
    messages += history + [{"role": "user", "content": user_content}]
    
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
    return "Energi kritis! Bensin habis."

# --- HANDLER PESAN ---
@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    img_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
    await bot.send_chat_action(message.chat.id, "typing")
    response = talk_to_groq(message.from_user.id, text=message.caption, img_url=img_url)
    await message.reply(f"👁️ **Analisis Mata Bolu:**\n\n{response}")

@dp.message()
async def handle_text(message: Message):
    if not message.text: return
    
    # PERBAIKAN DI SINI: Bolu membersihkan teks sebelum mengecek
    pesan_bersih = message.text.strip().lower()
    
    # Fitur Kaki (Autonomous) - Sekarang lebih peka
    if "status sistem" in pesan_bersih:
        try:
            stats = subprocess.check_output("uptime && free -h", shell=True).decode()
            await message.answer(f"🤖 **Laporan Mandiri Bolu:**\nSistem Aman.\n\nKondisi Mesin:\n{stats}")
        except:
            await message.answer("🤖 Sistem sedang sibuk mengevaluasi, tapi saya tetap aktif!")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    response = talk_to_groq(message.from_user.id, text=message.text)
    await message.answer(response)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 AKTIF (VERSI ANTI-REWEL) <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
