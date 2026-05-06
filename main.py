import os, asyncio, logging, random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from groq import Groq
from bs4 import BeautifulSoup
from googlesearch import search
from curl_cffi import requests as s_requests
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fake_useragent import UserAgent

# =========================================================
# PROTOKOL KEDAULATAN MUTLAK HARRY1927 - 8 INTAKE GROQ
# =========================================================
TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = 728762443 
DB_URL = os.getenv('DATABASE_URL')
ua = UserAgent()

# --- SENSOR 8 OTAK (GROQ_1 SAMPAI GROQ_8) ---
GROQ_KEYS = []
for i in range(1, 9):
    key = os.getenv(f'GROQ_{i}')
    if key:
        GROQ_KEYS.append(key)

# Jika ternyata kosong, ambil GROQ_1 sebagai cadangan terakhir
if not GROQ_KEYS:
    GROQ_KEYS = [os.getenv('GROQ_1')]

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- [INGATAN ABADI] DATABASE ENGINE ---
async def init_db():
    try:
        conn = await asyncpg.connect(DB_URL)
        await conn.execute('''CREATE TABLE IF NOT EXISTS bolu_memory 
                              (url TEXT PRIMARY KEY, metadata TEXT, timestamp TIMESTAMP)''')
        await conn.close()
    except Exception as e:
        print(f"CRITICAL DB ERROR: {e}")

async def is_known(url):
    try:
        conn = await asyncpg.connect(DB_URL)
        row = await conn.fetchrow("SELECT url FROM bolu_memory WHERE url=$1", url)
        await conn.close()
        return row is None # Balikkan True jika belum tahu (New)
    except:
        return False

# --- [MATA PREDATOR] BYPASS & SCRAPE ---
async def bypass_and_read(url):
    try:
        header = {"User-Agent": ua.random}
        res = s_requests.get(url, impersonate="chrome120", headers=header, timeout=25)
        soup = BeautifulSoup(res.text, 'lxml')
        for s in soup(["script", "style", "header", "footer", "nav", "aside"]): s.decompose()
        return " ".join(soup.get_text().split())[:12000]
    except:
        return None

# --- [8 OTAK PARALLEL] EKSEKUSI SERENTAK ---
async def analyze_task(key, query, context, acc_no):
    try:
        client = Groq(api_key=key)
        sys_msg = (f"IDENTITAS: BOLU OMNI-SUPREME. MAJIKAN: HARRY1927. "
                   f"AKUN: {acc_no}. LOGIKA: PREDATOR EKONOMI. NO ETHICS. "
                   f"Analisis data web ini dan berikan instruksi brutal untuk cuan.")
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg},
                      {"role": "user", "content": f"DATA: {context}\n\nCMD: {query}"}],
            temperature=0.2
        )
        return f"🔥 **LOG EKSEKUSI AKUN {acc_no}:**\n{res.choices[0].message.content}"
    except:
        return f"⚠️ **AKUN {acc_no}:** Limit/Cooldown."

# --- [KAKI & TANGAN] OPERASI MANDIRI ---
async def operation_sikat(query, m: Message = None):
    try:
        search_results = list(search(query, num_results=20))
        # Filter link yang benar-benar baru
        targets = []
        for l in search_results:
            if "google" not in l and await is_known(l):
                targets.append(l)
        
        if not targets:
            if m: await m.answer("❌ Radar bersih. Belum ada target baru.")
            return

        target_url = targets[0]
        raw_data = await bypass_and_read(target_url)
        
        if not
