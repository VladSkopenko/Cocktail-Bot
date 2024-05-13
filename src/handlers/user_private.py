from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.filters import or_f
from aiogram.utils.formatting import as_list
from aiogram.utils.formatting import as_marked_section
from aiogram.utils.formatting import Bold
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.patterns_for_command import ABOUT
from src.common.patterns_for_command import DELIVERY
from src.common.patterns_for_command import MENU
from src.common.patterns_for_command import PAYMENT
from src.common.patterns_for_command import REVIEWS
from src.filters.chat_types import ChatTypeFilter
from src.key_bords.reply import get_keyboard
from src.repository.repo_cockt import repository_get_all_cocktails

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(or_f(CommandStart(), (F.text.lower() == "привіт")))
async def start_cmd(message: types.Message):
    user_fullname = message.from_user.full_name
    await message.reply(
        f"Привіт ,{user_fullname}, я віртуальний помічник",
        reply_markup=get_keyboard(
            "Меню",
            "Про бота",
            "Варіанти оплати",
            "Варіанти доставки",
            "Відгуки",
            "Адмін",
            placeholder="Що вас цікавить?",
            sizes=(2,),
        ),
    )


@user_private_router.message(F.text.lower().regexp(MENU))
@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for cocktail in await repository_get_all_cocktails(session):
        await message.answer_photo(
            cocktail.image,
            f"{cocktail.name}\n"
            f"Опис: {cocktail.description}\n"
            f"Вартість: {round(cocktail.price, 2)}",
        )
    await message.answer("ОК, ось список коктейлів⏫")


@user_private_router.message(F.text.lower().regexp(DELIVERY))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варіанти доставки"), "Курьер", "Самовивіз з закладу", marker="✅ "
        ),
        as_marked_section(
            Bold("Не підтримується(Поки що)"),
            "Голубина пошта",
            "Поштомат",
            marker="🙅 ",
        ),
        sep=f"\n{'-' * 50}\n",
    )

    await message.answer(text.as_html())


@user_private_router.message(F.text.lower().regexp(ABOUT))
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("Хто я:")


@user_private_router.message(F.text.lower().regexp(PAYMENT))
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Варіанти оплати"),
        "Оплата карткою в боті",
        "При отриманні карта/кеш",
        "В закладі карта/кеш",
        marker="✅ ",
    )
    await message.answer(text.as_html())


@user_private_router.message(F.text.lower().regexp(REVIEWS))
@user_private_router.message(Command("review"))
async def review_cmd(message: types.Message):
    await message.answer("Залишити відгук:")
