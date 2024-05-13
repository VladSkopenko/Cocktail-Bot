from aiogram import F
from aiogram import types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.admin.admin_private import admin_router
from src.repository.repo_banner import repository_change_banner_image
from src.repository.repo_banner import repository_get_info_pages


class AddBanner(StatesGroup):
    image = State()


@admin_router.message(StateFilter(None), F.text == "Добавить/Изменить баннер")
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await repository_get_info_pages(session)]
    await message.answer(
        f"Отправьте фото баннера.\nВ описании укажите для какой страницы:\
                         \n{', '.join(pages_names)}"
    )
    await state.set_state(AddBanner.image)


@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await repository_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(
            f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}"
        )
        return
    await repository_change_banner_image(
        session,
        for_page,
        image_id,
    )
    await message.answer("Баннер добавлен/изменен.")
    await state.clear()


@admin_router.message(AddBanner.image)
async def add_banner2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото баннера или отмена")
