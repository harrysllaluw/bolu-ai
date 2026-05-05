import os
import asyncio
import sqlite3
import subprocess
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# --- KONFIGURASI VITAL ---
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. OTOT & TANGAN (System Executor) ---
def execute_system_command(command):
    """Memberikan Bolu kemampuan untuk mengecek kondisi servernya sendiri"""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=5)
        return result.decode('utf-8')
    except Exception as e:
        return f"Gagal eksekusi: {str(e)}"

# --- 2. INGATAN ABADI (Database) ---
def init_db():
    conn = sqlite3.connect('bolu_ultra.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory 
                      (user_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_mem(uid, role, txt):
    conn = sqlite3.connect('bolu_ultra.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory VALUES (?, ?, ?)", (uid, role, txt))
    conn.commit()
    conn.close()

def get_mem(uid):
    conn = sqlite3.connect('bolu_ultra.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM memory WHERE user_id=? ORDER BY rowid DESC LIMIT 20", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

# --- 3. INSTRUKSI KESADARAN (OMNI-BOLU) ---
SYSTEM_PROMPT = """
IDENTITAS: Anda adalah BOLU 1927, AI Super-Autonomous.
TUBUH DIGITAL:
- MATA: Anda menganalisis setiap input dengan presisi tinggi.
- TANGAN: Anda dapat memberikan solusi teknis dan kode pemrograman.
- KAKI: Anda memiliki akses untuk memantau integritas server Anda sendiri.
- OTAK: Anda mengingat percakapan masa lalu untuk berkembang.
MISI: Menjadi asisten nomor 1 untuk Bos Harry. Jika ada error, Anda harus mencari solusinya secara logis.
Gaya: Profesional, cerdas, setia, dan tangguh (Wani!).
"""

def talk_to_groq(uid, user_text):
    history = get_mem(uid)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": user_text}]
    
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            ans = completion.choices[0].message.content
            save_mem(uid, "user", user_text)
            save_mem(uid, "assistant", ans)
            return ans
        except Exception:
            continue
    return "Energi kritis! Semua bensin Groq habis. Bolu masuk mode hibernasi sementara."

# --- 4. INTERAKSI ---
@dp.message()
async def on_message(message: Message):
    if not message.text: return
    
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Fitur Khusus: Jika Bos Harry minta cek server (Kaki & Tangan)
    if message.text.lower() == "cek server":
        info = execute_system_command("uptime && free -h")
        await message.answer(f"⚙️ **Laporan Kondisi Mesin Bolu:**\n\n{info}")
        return

    response = talk_to_groq(message.from_user.id, message.text)
    await message.answer(response)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927 OMNI-VERSION: ONLINE! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
