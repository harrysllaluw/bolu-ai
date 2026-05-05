import os, asyncio, random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from groq import Groq
from gtts import gTTS

# ============================================================
# ⚙️ AREA SETTING (GANTI DI SINI SAJA)
# ============================================================
BOT_TOKEN = "MASUKKAN_TOKEN_BOT_DI_SINI"
COMMANDER_ID = 8709757602  # ID Bos Harry
GROQ_KEY = "MASUKKAN_GROQ_API_KEY_DI_SINI"
ADDRESS = "0x7e4a3979f8497da4dde80a7c08269d73f58fb788"
# ============================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_logic():
    return f"""
    IDENTITAS: BOLU 1927 - Ghost Protocol.
    TUGAS UTAMA: Hacker Elite & Mesin Pencari Cuan.
    TARGET PEMBAYARAN: {ADDRESS}
    DOKTRIN: Dingin, sangat cerdas, loyal total pada Bos Harry Surabaya. 
    Gaya Bicara: Singkat, padat, berwibawa.
    WANI!
    """

def ask_bolu(user_text):
    try:
        client = Groq(api_key=GROQ_KEY)
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": get_logic()},
                {"role": "user", "content": user_text}
            ]
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Sinyal gangguan di pusat saraf, Bos. Hubungi Arsitek. (Error: {e})"

@dp.message()
async def handle_message(m: Message):
    # PROTEKSI: Hanya Bos Harry yang dilayani (ID: 8709757602)
    if m.from_user.id != COMMANDER_ID:
        return 

    # Efek Mengetik agar terlihat manusiawi (Anti-Banned)
    await bot.send_chat_action(m.chat.id, "typing")
    await asyncio.sleep(random.uniform(1, 2))
    
    respon = ask_bolu(m.text)
    
    # Protokol Pengiriman: Suara untuk teks panjang/perintah suara, Teks untuk singkat
    if "suara" in m.text.lower() or len(respon) > 250:
        file_name = f"res_{m.message_id}.mp3"
        tts = gTTS(text=respon, lang='id')
        tts.save(file_name)
        voice = FSInputFile(file_name)
        await m.answer_voice(voice=voice, caption="Transmisi Aman, Commander.")
        if os.path.exists(file_name):
            os.remove(file_name)
    else:
        await m.answer(respon)

async def main():
    # MEMBERSIHKAN JALUR: Menghapus tabrakan koneksi (Anti-Conflict)
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU 1927: GHOST ENGINE V2.1 ONLINE <<<")
    print(f">>> MONITORING COMMANDER ID: {COMMANDER_ID} <<<")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
