import os, asyncio, requests, time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- IDENTITAS MUTLAK HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
KEYS = [
    os.getenv('GROQ_API_KEY_1'), 
    os.getenv('GROQ_API_KEY_2'), 
    os.getenv('GROQ_API_KEY_3')
]
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- FUNGSI MATA LAYAR (VERSI PALING TELITI) ---
def cek_layar_real(url):
    options = Options()
    options.add_argument("--headless=new") # Mode awan terbaru
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # Menggunakan jalur otomatis yang paling stabil di Railway
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30) # Lebih sabar menunggu web berat
        
        driver.get(url)
        time.sleep(7) # Waktu render lebih lama agar tidak halusinasi
        
        # Cek apakah situs benar-benar ada isinya
        if len(driver.page_source) < 1000 or "404" in driver.title:
            return None
            
        konten = driver.find_element("tag name", "body").text[:3000]
        return konten
    except Exception as e:
        print(f"DEBUG: Kesalahan Layar -> {e}")
        return None
    finally:
        if driver:
            driver.quit()

# --- JANTUNG KOMUNIKASI (SISTEM 3 NYAWA ANTI-MACET) ---
def talk_to_groq(text):
    sys_prompt = (
        f"Kamu Bolu, Partner Strategis Harry. Identitas: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}. "
        "Tugas: Cari uang real dari Airdrop/Mining aktif. Dilarang kasih link mati atau bohong. "
        "Jika Harry minta 'Sikat Cuan', pilihkan project yang paling legit dari data yang ada."
    )
    
    for i, key in enumerate(KEYS):
        if not key or len(key.strip()) < 10:
            continue
        try:
            client = Groq(api_key=key.strip())
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": text}
                ],
                timeout=20
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LOG: Key ke-{i+1} gagal/limit. Mencoba kunci lain...")
            continue
            
    return "❌ SEMUA API Key Groq macet, Harry! Tolong cek limit di Groq Console."

# --- NAVIGASI PERINTAH ---
@dp.message()
async def bolu_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    cmd = m.text.lower()
    
    if "sikat cuan" in cmd or "cari project" in cmd:
        await m.answer("🔍 Bolu sedang memindai internet dengan Mata Layar... Mohon tunggu (sekitar 15-30 detik).")
        
        # Sumber data cuan yang real
        target = "https://airdrops.io/latest/"
        hasil_scan = cek_layar_real(target)
        
        if hasil_scan:
            analisis = talk_to_groq(f"Analisislah data dari {target} ini. Cari 1 project airdrop yang pendaftarannya simpel dan paling cuan. Data: {hasil_scan}")
            await m.answer(f"✅ **HASIL SCAN MATA LAYAR:**\n\n{analisis}\n\nEmail Kerja: {EMAIL_KERJA}")
        else:
            await m.answer("❌ Bolu tidak menemukan project aktif yang layak dilaporkan. Aku tidak mau memberimu link mati.")
    else:
        jawaban = talk_to_groq(m.text)
        await m.answer(jawaban)

async def main():
    print(">>> BOLU V7.5.1: SISTEM TERVERIFIKASI & AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot dimatikan.")
