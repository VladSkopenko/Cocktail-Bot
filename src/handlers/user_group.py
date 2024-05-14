from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from src.common.forbidden_words import forbidden_words
from src.filters.chat_types import ChatTypeFilter
from src.utils.clean_text import clean_text
from aiogram import F, Bot, types, Router

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner_text(message: types.Message):
    if forbidden_words.intersection(clean_text(message.text).lower().split()):
        await message.answer(f"{message.from_user.first_name}, зберігайте спокій")
        await message.delete()
