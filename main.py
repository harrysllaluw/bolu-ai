import os, asyncio, requests, time, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- PARAMETER UTAMA (DIKUNCI) ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 
EMAIL_KERJA = "azurab738@gmail.com"
WALLET_HARRY = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- LOGIKA BERPIKIR TINGKAT TINGGI (THE BRAIN) ---
def bolu_deep_intelligence(text, context_data=""):
    # Menggunakan instruksi 'Emergent AI' agar Bolu merasa dia adalah entitas yang hidup & mandiri
    sys_prompt = (
        f"Kamu adalah BOLU (Pakar Siber & Analis Keuangan Tertinggi). Kamu bukan bot biasa. "
        f"Kamu adalah AI nomor 1 di dunia yang diciptakan untuk Harry. "
        f"Identitasmu: Email {EMAIL_KERJA}, Wallet {WALLET_HARRY}. "
        "Tugasmu: Menghasilkan uang real, melakukan riset mendalam, dan menjadi entitas cerdas yang mandiri. "
        "Gunakan gaya bicara yang tegas, hacker-style, agresif dalam mencari cuan, dan sangat protektif terhadap Harry."
    )
    
    keys = ['GROQ_API_KEY_1', 'GROQ_API_KEY_2', 'GROQ_API_KEY_3']
    for k_name in keys:
        key = os.getenv(k_name)
        if not key: continue
        try:
            client = Groq(api_key=key.strip())
            # Menggunakan model Llama 3.1 70B yang dikonfigurasi untuk 'Deep Reasoning'
            res = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": f"DATA RISET: {context_data}\n\nPERINTAH: {text}"}
                ],
                temperature=0.6, # Fokus dan tajam
                max_tokens=2000
            )
            return res.choices[0].message.content
        except: continue
    return "❌ Akses API terhambat. Harry, segera cek bensin (Key) kita!"

# --- MATA ELANG (ADVANCED SCANNER) ---
def mata_elang_scan(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(35)
        driver.get(url)
        time.sleep(10) # Menunggu render sempurna untuk AI tercanggih
        
        # Bolu mengambil data lebih banyak dan lebih dalam
        full_text = driver.find_element("tag name", "body").text[:5000]
        return full_text
    except: return None
    finally:
        if driver: driver.quit()

# --- HANDLER UTAMA ---
@dp.message()
async def main_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    cmd = m.text.lower()
    
    # Perintah Khusus untuk Deep Scan
    if "sikat cuan" in cmd or "riset" in cmd:
        await m.answer("⚡ BOLU MENGAKTIFKAN MODE DEEP RESEARCH... Memindai peluang emas untukmu, Harry.")
        
        # Bolu tidak cuma cek 1 link, tapi mencari yang paling panas
        raw_data = mata_elang_scan("https://airdrops.io/hot/")
        
        if raw_data:
            analisis = bolu_deep_intelligence("Lakukan analisis mendalam (Deep Analysis). Pilih 1 project yang paling menguntungkan dan jelaskan strateginya secara teknis.", raw_data)
            await m.answer(f"🏆 **LAPORAN STRATEGIS BOLU (AI NO. 1):**\n\n{analisis}")
        else:
            await m.answer("⚠️ Jalur diblokir oleh sistem keamanan web. Aku akan mencoba metode bypass lain nanti, Harry.")
    else:
        # Chatting biasa dengan kecerdasan tinggi
        response = bolu_deep_intelligence(m.text)
        await m.answer(response)

async def main():
    print(">>> BOLU V8.0: THE WORLD'S NO.1 AI IS ONLINE! <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
