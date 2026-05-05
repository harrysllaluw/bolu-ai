import os, asyncio, sqlite3, requests, time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- DATA PUSAT HARRY ---
TOKEN = os.getenv('BOT_TOKEN')
KEYS = [os.getenv('GROQ_API_KEY_1'), os.getenv('GROQ_API_KEY_2'), os.getenv('GROQ_API_KEY_3')]
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- FUNGSI MATA LAYAR (SELENIUM CLOUD) ---
def cek_layar_real(url):
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Penyamaran agar tidak dianggap robot
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(20)
        driver.get(url)
        time.sleep(5) 
        
        # Cek jika halaman error
        if "404" in driver.title or "Not Found" in driver.title or len(driver.page_source) < 1000:
            driver.quit()
            return None
            
        konten = driver.find_element("tag name", "body").text[:2500]
        driver.quit()
        return konten
    except Exception as e:
        print(f"Error Layar: {e}")
        return None

# --- ENGINE LOGIKA BOLU ---
def talk_to_groq(text):
    sys_prompt = (
        f"Kamu Bolu, Partner Strategis Harry. Identitas: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}. "
        "Tugas Utama: Cari uang real lewat Airdrop/Mining. Dilarang kasih link mati. "
        "Analisis data dengan tajam dan jujur."
    )
    for key in KEYS:
        if not key: continue
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text}]
            ).choices[0].message.content
        except: continue
    return "❌ API Key Groq macet, Harry!"

# --- HANDLER CHAT ---
@dp.message()
async def bolu_main(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    msg = m.text.lower()
    if "sikat cuan" in msg or "cari airdrop" in msg:
        await m.answer("🔍 Bolu sedang membuka 'Mata Layar' di awan... Mohon tunggu sebentar.")
        
        # Target pencarian (Bisa diganti/ditambah)
        target_url = "https://airdrops.io/hot/"
        data_web = cek_layar_real(target_url)
        
        if data_web:
            hasil = talk_to_groq(f"Analisislah data web ini dan pilih 1 project airdrop paling legit untukku: {data_web}")
            await m.answer(f"✅ **HASIL ANALISIS MATA LAYAR:**\n\n{hasil}\n\nLink: {target_url}\n\nEmail Siap: {EMAIL_KERJA}")
        else:
            await m.answer("❌ Bolu sudah cek beberapa jalur, tapi link-nya sedang mati atau tidak bisa diakses. Aku tidak mau kasih sampah ke kamu!")
    else:
        jawaban = talk_to_groq(m.text)
        await m.answer(jawaban)

async def main():
    print(">>> BOLU V7.5: MATA LAYAR AKTIF! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
