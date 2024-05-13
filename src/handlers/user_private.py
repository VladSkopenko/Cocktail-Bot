from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.chat_types import ChatTypeFilter
from src.handlers.menu_processing import get_menu_content
from src.key_bords.inline import MenuCallBack
from src.repository.repo_cart import repository_add_to_cart
from src.repository.repo_user import repository_add_user

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")

    await message.answer_photo(
        media.media, caption=media.caption, reply_markup=reply_markup
    )


async def add_to_cart(
    callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession
):
    user = callback.from_user
    await repository_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await repository_add_to_cart(
        session, user_id=user.id, cocktail_id=callback_data.cocktail_id
    )
    await callback.answer("Коктейль додано в корзину.")


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession
):

    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        cocktail_id=callback_data.cocktail_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


