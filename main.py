import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from groq import Groq

# Ambil Variabel dari Railway
TOKEN = os.getenv('BOT_TOKEN')
GROQ_KUNCI = os.getenv('GROQ_API_KEY')

# Inisialisasi Groq & Bot
client = Groq(api_key=GROQ_KUNCI)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_chat(message: Message):
    if not message.text: return
    try:
        # Pake Llama 3 (Otak Groq paling encer)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Bolu lagi pening, Bos. Cek Groq Key di Railway!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> BOLU GROQ SUDAH MELEK! <<<")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
