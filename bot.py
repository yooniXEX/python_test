import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command, CommandStart

TOKEN = "8381336402:AAFM9PbF6fqKVfBz_nkOzff4iOo7EPHahjE"
API_URL = "https://your-app.up.railway.app"
MINI_APP_URL = "https://magical-taiyaki-08d177.netlify.app"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    url = f"{MINI_APP_URL}?user_id={message.from_user.id}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Открыть задачи",
            web_app=WebAppInfo(url=url)
        )]
    ])

    await message.answer("Открой приложение 👇", reply_markup=kb)

@dp.message(Command("add"))
async def add_task(message: Message):
    text = message.text.replace("/add", "").strip()

    if not text:
        await message.answer("Напиши: /add задача")
        return

    requests.post(f"{API_URL}/api/add", json={
        "user_id": message.from_user.id,
        "title": text
    })

    await message.answer("✅ Добавлено")

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
