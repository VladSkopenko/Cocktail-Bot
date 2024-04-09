import time
import logging
import os
import asyncio
import sys
import schedule

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")

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


async def send_reminder():
    schedule.every().day.at("12:00").do(remind_git)
    schedule.every().day.at("21:00").do(remind_git)
    schedule.every().day.at("04:39").do(remind_git)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
