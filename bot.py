import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
API_TOKEN = "8411809747:AAH4j3Pdc0reP2D00uX7L72Y8xZle_GZhPg"



bot = Bot(token=API_TOKEN)
dp = Dispatcher()

MINI_APP_URL = "https://magical-taiyaki-08d177.netlify.app"

import requests
from aiogram.filters import Command

API_URL = " https://tricky-cameras-add.loca.lt"  # ИЛИ loca.lt

@dp.message(Command("add"))
async def add_task(message: Message):
    text = message.text.replace("/add", "").strip()

    if not text:
        await message.answer("Напиши: /add задача")
        return

    try:
        requests.post(f"{API_URL}/api/add", json={
            "user_id": message.from_user.id,
            "title": text
        })

        await message.answer(f"✅ Добавлено: {text}")

    except Exception as e:
        await message.answer("❌ Ошибка при добавлении")
        print(e)

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id

    url = f"{MINI_APP_URL}?user_id={user_id}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Открыть трекер",
            web_app=WebAppInfo(url=url)
        )]
    ])

    await message.answer("Открой приложение 👇", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
