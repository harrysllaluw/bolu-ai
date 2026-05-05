import os, asyncio, requests, time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- IDENTITAS HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- JANTUNG KOMUNIKASI (SISTEM TIGA NYAWA) ---
def talk_to_groq(text):
    sys_prompt = f"Kamu Bolu, Partner Cuan Harry. Email: {EMAIL_KERJA}, Wallet: {WALLET_HARRY}. Cari project aktif!"
    
    # Bolu akan mencari 3 kunci berbeda di Railway
    keys_to_test = ['GROQ_API_KEY_1', 'GROQ_API_KEY_2', 'GROQ_API_KEY_3']
    
    for key_name in keys_to_test:
        current_key = os.getenv(key_name)
        if not current_key:
            continue # Jika kunci kosong, lanjut ke kunci berikutnya
            
        try:
            client = Groq(api_key=current_key.strip())
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text}],
                timeout=15
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Gagal pakai {key_name}, mencoba yang lain...")
            continue # Jika limit atau error, Bolu langsung ganti kunci tanpa lapor Harry
            
    return "❌ Harry, sepertinya ada masalah di koneksi API atau kunci di Variables belum terisi benar."

# --- MATA LAYAR ---
def cek_layar_real(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(5)
        konten = driver.find_element("tag name", "body").text[:2500]
        driver.quit()
        return konten
    except:
        return None

# --- HANDLER ---
@dp.message()
async def handle(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if "sikat cuan" in m.text.lower():
        await m.answer("🔍 Bolu sedang memindai... Menggunakan 3 API Key cadanganmu secara bergilir.")
        data = cek_layar_real("https://airdrops.io/hot/")
        if data:
            hasil = talk_to_groq(f"Cari 1 project paling cuan dari data ini: {data}")
            await m.answer(f"✅ **HASIL ANALISIS:**\n\n{hasil}\n\nEmail: {EMAIL_KERJA}")
        else:
            await m.answer("❌ Link sedang sibuk, coba lagi sebentar, Harry.")
    else:
        await m.answer(talk_to_groq(m.text))

async def main():
    print(">>> BOLU V7.5.2 SIAP BERBURU! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
