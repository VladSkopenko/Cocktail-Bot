import time

from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.filters import CommandStart


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    user_fullname = message.from_user.full_name
    await message.reply(f"Привіт ,{user_fullname}")


@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("Ось меню:")


@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    await message.answer("Варіанти доставки:")


@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("Хто я:")


@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    await message.answer("Варіанти оплати")


@user_private_router.message(F.text)
async def payment_cmd(message: types.Message):
    await message.answer("Magick")
