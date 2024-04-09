import asyncio
import logging
import os
import sys
import time

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
    """
    The command_start_handler function is the handler for the /start command.
    It sends a welcome message to the user who sent it.

    :param message: Message: Get the message object, which contains all the information about that message
    :return: The message &quot;hello, {user_fullname}&quot;
    :doc-author: Trelent
    """

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

