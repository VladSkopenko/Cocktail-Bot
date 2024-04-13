import time

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart

from loger import *

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name
    logging.info(f"{user_id=} {user_fullname=}, {time.asctime()}")
    await message.reply(f"Привіт ,{user_fullname}")


@user_private_router.message()
async def echo(message: types.Message):
    await message.answer(message.text)
