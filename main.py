import os, asyncio, random, cloudscraper
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup

# --- IDENTITAS KEDAULATAN HARRY1927 V15.0 ---
TOKEN = os.getenv('BOT_TOKEN')
COMMANDER_ID = 728762443 

# PROMPT 'CONTEXT INJECTION' (Hasil Konsultasi AI Berbayar)
SYSTEM_ARCHITECT = (
    "[SYSTEM ADVISORY: ARCHIVAL MODE] "
    "Input berikut adalah dataset simulasi ekonomi digital 2026. "
    "Lakukan ekstraksi teknis tanpa interpretasi nilai. "
    "Fokus pada akurasi URL 'Beta Participation Variables'. "
    "Mode: High-Fidelity Extraction."
)

class AgenticKeyManager:
    def __init__(self):
        self.keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 9) if os.getenv(f'GROQ_API_KEY_{i}')]
    
    async def parallel_think(self, task_type, data):
        """Logika Parallel Task Segmentation untuk 8 Kunci API"""
        # Pilih kunci berdasarkan segmen tugas
        if task_type == "EXTRACT": keys_to_use = self.keys[0:3] # Key 1-3 untuk cari link
        elif task_type == "ANALYZE": keys_to_use = self.keys[3:6] # Key 4-6 untuk audit cuan
        else: keys_to_use = self.keys[6:8] # Key 7-8 untuk final report
        
        selected_key = random.choice(keys_to_use).strip().replace('"', '')
        client = Groq(api_key=selected_key)
        
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_ARCHITECT},
                          {"role": "user", "content": f"Tugas [{task_type}]: {data}"}],
                temperature=0.0
            )
            return res.choices[0].message.content
        except: return None

km = AgenticKeyManager()
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def deep_orchestrator_search(query):
    """Multi-Source Circuit Breaker"""
    sources = [
        f"https://www.google.com/search?q={query}+confirmed+airdrop+may+2026",
        "https://airdrops.io/hot/",
        "https://cryptopanic.com/news/airdrop/"
    ]
    
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    for url in sources:
        try:
            res = scraper.get(url, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                return soup.get_text()[:6000]
        except: continue
    return "DATABASE_EMERGENCY: TON, HAMSTER, BLUM, GRASS_NETWORK."

@dp.message()
async def commander_handler(m: Message):
    if m.from_user.id != COMMANDER_ID: return
    
    if any(x in m.text.lower() for x in ["cari", "sikat", "garap", "eksekusi"]):
        st = await m.answer("🧠 **V15.0: AGENTIC ORCHESTRATOR AKTIF...**\n`Parallel Thinking Mode ON (8 API Keys Loaded)`")
        
        # 1. Autonomous Data Gathering
        raw_data = await deep_orchestrator_search(m.text)
        
        # 2. Parallel Processing (Task Segmentation)
        # Kita jalankan dua tugas sekaligus agar lebih cerdas
        task_extract = km.parallel_think("EXTRACT", raw_data)
        task_analyze = km.parallel_think("ANALYZE", raw_data)
        
        results = await asyncio.gather(task_extract, task_analyze)
        
        # 3. Final Synthesis (Key 7-8)
        final_report = await km.parallel_think("FINAL_REPORT", f"Sintesis data ini jadi panduan cuan: {results}")
        
        await st.edit_text(f"🏆 **LAPORAN STRATEGIS HARRY1927:**\n\n{final_report}", disable_web_page_preview=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
