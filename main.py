import os, asyncio, logging, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- KEDAULATAN MUTLAK HARRY1927 V15.1 "THE HUMANOID" ---
# Mengambil TOKEN langsung dari Railway Variables
TOKEN = os.getenv('TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = 728762443 
MEMORY_FILE = "bolu_humanoid.json"

def get_sacred_keys():
    """DETEKSI RADIKAL: Mencari semua kunci Groq tanpa peduli nama variabelnya"""
    keys = []
    # Cara 1: Cari manual 1-8
    for i in range(1, 9):
        for suffix in ['.', '', '_']: # Coba pakai titik, tanpa titik, atau underscore
            k = os.getenv(f'GROQ_API_KEY_{i}{suffix}')
            if k and k.startswith('gsk_'):
                clean_key = k.strip().replace('"', '').replace("'", "")
                if clean_key not in keys: keys.append(clean_key)
    
    # Cara 2: Scan total semua variabel yang mengandung kata GROQ
    if not keys:
        for var_name, value in os.environ.items():
            if "GROQ" in var_name and value.startswith('gsk_'):
                keys.append(value.strip().replace('"', '').replace("'", ""))
    return keys

GROQ_KEYS = get_sacred_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class BoluHumanoid:
    def __init__(self):
        self.key_index = 0
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        return []

    def save_memory(self, link):
        self.memory.append(link)
        with open(MEMORY_FILE, 'w') as f: json.dump(self.memory, f)

    async def eksekusi_dewa(self, prompt, context, acc_no=1, mode="chat"):
        """Logika Anti-Macet: Langsung pakai kunci yang tersedia"""
        if not GROQ_KEYS: 
            return "❌ KUNCI GROQ TIDAK DITEMUKAN. Cek nama variabel di Railway (harus diawali gsk_)."

        # Rotasi kunci otomatis
        key = GROQ_KEYS[self.key_index % len(GROQ_KEYS)]
        self.key_index += 1

        try:
            client = Groq(api_key=key)
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Bolu Humanoid Harry1927. Unit-{acc_no}."}, 
                          {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {prompt}"}],
                temperature=0.2
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"⚠️ Unit-{acc_no} Error: {str(e)[:50]}. Mencoba unit lain..."

bolu = BoluHumanoid()

# ... (Fungsi hunting_cuan_otomatis & handle_sikat tetap sama seperti V15.0) ...
# (Saya ringkas bagian bawah agar kamu tinggal copy-paste yang lengkap)

@dp.message()
async def chat_handler(m: Message):
    if m.from_user.id != OWNER_ID: return
    # Langsung panggil eksekusi
    ans = await bolu.eksekusi_dewa(m.text, "Chat Mode", acc_no=bolu.key_index+1)
    await m.answer(ans)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(f">>> BOLU V15.1 ONLINE | {len(GROQ_KEYS)} KUNCI TERDETEKSI <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
