import re
import socket
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import os

BOT_TOKEN = os.getenv("9224806523:AAHC-oQFFhjVTVqFJRn4_DgNuAeJ5ALdxq8") 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def ip_to_hex(ip_str: str) -> str:
    parts = [int(part) for part in ip_str.split('.')]
    return "0x" + "".join(f"{part:02x}" for part in parts)

def get_hex_ip_link(url: str) -> str | None:
    if not re.match(r'^https?://', url):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        path = parsed.path if parsed.path else "/"
        query = f"?{parsed.query}" if parsed.query else ""
        if not hostname: return None
        ip = socket.gethostbyname(hostname)
        hex_ip = ip_to_hex(ip)
        return f"http://{hex_ip}{path}{query}"
    except Exception:
        return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Пришли мне ссылку, и я сделаю из неё HEX-IP линк.")

@dp.message(F.text)
async def handle(message: Message):
    text = message.text.strip()
    if "." not in text:
        await message.answer("⚠️ Это не похоже на ссылку.")
        return
    result = get_hex_ip_link(text)
    if not result:
        await message.answer("❌ Не смог определить IP.")
        return
    await message.answer(f"✅ Готово:\n`{result}`", parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
