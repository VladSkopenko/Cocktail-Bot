import asyncio
import os

from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv
from src.handlers.user_private import user_private_router

load_dotenv()

ALLOWED_UPDATES = ["message", "edited_message"]
TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
