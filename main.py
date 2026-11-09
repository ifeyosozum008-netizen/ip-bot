import re
import httpx
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

# Твой токен
BOT_TOKEN = "9169232508:AAEncl4GE7sa0wDBdnd0-nPpl8bB_32bvAE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def shorten_url(url: str) -> str:
    """Сокращает ссылку через бесплатный сервис is.gd"""
    try:
        async with httpx.AsyncClient() as client:
            # Отправляем запрос на сокращение
            response = await client.get(f"https://is.gd/create.php?format=simple&url={url}")
            if response.status_code == 200:
                return response.text
    except Exception as e:
        print(f"Ошибка сокращения: {e}")
    return url # Если не вышло, вернет оригинал

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Пришли мне ссылку (например, на Авито), и я сделаю из неё рабочую короткую ссылку.")

@dp.message(F.text)
async def handle(message: Message):
    text = message.text.strip()
    if "." not in text:
        await message.answer("⚠️ Это не похоже на ссылку. Пришли URL.")
        return
        
    if not text.startswith("http"):
        text = "https://" + text

    await message.answer("⏳ Генерирую ссылку, подожди пару секунд...")
    
    # Делаем короткую ссылку
    short_link = await shorten_url(text)
    
    await message.answer(f"✅ Твоя ссылка готова:\n{short_link}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
