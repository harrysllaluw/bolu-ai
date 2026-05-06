import os, asyncio, random, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests

# --- KONFIGURASI HARRY1927 V16.1 ---
TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or '8709757602:AAG5rRGSiveQATYho3vGcPVyGOYhxRIBzQo'
OWNER_ID = int(os.getenv('OWNER_ID') or 728762443)

def get_keys():
    """Ambil semua kunci Groq yang ada"""
    return [v.strip().replace('"', '') for k, v in os.environ.items() if "GROQ" in k and v.startswith('gsk_')]

GROQ_KEYS = get_keys()
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def tanya_bolu(teks, context=""):
    if not GROQ_KEYS: return "❌ Kunci Groq tidak ada di Variables!"
    client = Groq(api_key=random.choice(GROQ_KEYS))
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Kamu Bolu V16.1. Robot Harry1927. Jawab singkat & cari cuan."},
                      {"role": "user", "content": f"DATA: {context}\n\nPERINTAH: {teks}"}],
            temperature=0.1
        )
        return res.choices[0].message.content
    except: return "⚠️ Otak lelah, coba lagi 5 detik lagi Bos!"

@dp.message(F.text.func(lambda t: "sikat" in t.lower()))
async def handle_sikat(m: Message):
    if m.from_user.id != OWNER_ID: return
    await m.answer("👊 **TANGAN BERGERAK... MENCARI TARGET...**")
    try:
        for url in search("new crypto airdrop confirmed", num_results=1):
            if "google" not in url:
                await m.answer(f"🎯 **TARGET:** {url}\n\nSedang dianalisis...")
                break
    except: await m.answer("❌ Radar gangguan.")

@dp.message()
async def chat(m: Message):
    if m.from_user.id == OWNER_ID:
        await m.answer(await tanya_bolu(m.text))

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU V16.1 ONLINE <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
