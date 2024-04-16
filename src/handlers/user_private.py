from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.filters import or_f

from src.common.patterns_for_command import DELIVERY
from src.common.patterns_for_command import PAYMENT
from src.common.patterns_for_command import ABOUT
from src.common.patterns_for_command import MENU

user_private_router = Router()


@user_private_router.message(or_f(CommandStart(), (F.text.lower() == "привіт")))
async def start_cmd(message: types.Message):
    user_fullname = message.from_user.full_name
    await message.reply(f"Привіт ,{user_fullname}, я віртуальний помічник")


@user_private_router.message(or_f(Command(MENU), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")


@user_private_router.message(F.text.lower().regexp(DELIVERY))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    await message.answer("Варіанти доставки:")


@user_private_router.message(F.text.lower().regexp(ABOUT))
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("Хто я:")


@user_private_router.message(F.text.lower().regexp(PAYMENT))
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    await message.answer("Варіанти оплати")


@user_private_router.message(F.text)
async def payment_cmd(message: types.Message):
    await message.answer("Magick")
