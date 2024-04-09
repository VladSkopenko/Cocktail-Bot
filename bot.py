import asyncio
import logging
import os
import sys
import time

from aiocron import crontab
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
MSG = "Чи завантажував ти свій код  на гітхаб сьогодні, {}?"


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name
    logging.info(f"{user_id=} {user_fullname=}, {time.asctime()}")
    await message.reply(f"Привіт ,{user_fullname}")


@dp.message()
async def remind_git(message: Message):
    user_name = message.from_user.first_name
    await message.answer(MSG.format(user_name))


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

