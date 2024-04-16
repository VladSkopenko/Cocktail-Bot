from aiogram import Router
from aiogram import types
from src.utils.clean_text import clean_text
from src.common.forbidden_words import forbidden_words

user_group_router = Router()


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner_text(message: types.Message):
    if forbidden_words.intersection(clean_text(message.text).lower().split()):
        await message.answer(f"{message.from_user.first_name}, зберігайте спокій")
        await message.delete()
