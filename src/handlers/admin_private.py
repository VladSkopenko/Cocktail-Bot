from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.patterns_for_command import ADMIN
from src.filters.chat_types import ChatTypeFilter
from src.filters.chat_types import IsAdmin
from src.key_bords.inline import get_callback_btns
from src.key_bords.reply import get_keyboard
from src.loger.loger import logging
from src.repository.crud import repository_add_cocktail
from src.repository.crud import repository_delete_cocktail_by_id
from src.repository.crud import repository_get_all_cocktails
from src.repository.crud import repository_get_cocktail_by_key

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

admin_key_board = get_keyboard(
    "Додати коктейль",
    "Асортимент",
    "Назад",
    "Скидання",
    placeholder="Оберіть дію",
    sizes=(2,),
)

class AddCocktail(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    cocktail_for_change = None

    texts = {
        "AddCocktail:name": "Введіть назву знову",
        "AddCocktail:description": "Введіть опис знову",
        "AddCocktail:price": "Введіть ціну знову",
        "AddCocktail:image": "Завантажте нове фото",
    }


@admin_router.message(F.text.lower().regexp(ADMIN))
@admin_router.message(Command("admin"))
async def start_work(message: types.Message):
    await message.answer("Що бажаєте зробити?", reply_markup=admin_key_board)


@admin_router.message(F.text == "Асортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for cocktail in await repository_get_all_cocktails(session):
        await message.answer_photo(
            cocktail.image,
            f"{cocktail.name}\n"
            f"Опис: {cocktail.description}\n"
            f"Вартість: {round(cocktail.price, 2)}",
            reply_markup=get_callback_btns(
                btns={
                    "Видалити": f"delete_{cocktail.id}",
                    "Редагувати": f"edit_{cocktail.id}",
                }
            ),
        )
    await message.answer("ОК, ось список коктейлів в асортименті")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_cocktail(callback: types.CallbackQuery, session: AsyncSession):
    cocktail_id = int(callback.data.split("_")[-1])
    await repository_delete_cocktail_by_id(session, cocktail_id)
    await callback.answer("Коктейль видалено!")
    await callback.message.answer("Коктейль видалено!")


@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    cocktail_id = callback.data.split("_")[-1]

    cocktail_for_change = await repository_get_cocktail_by_key(session, int(cocktail_id), mode="by_id")

    AddCocktail.product_for_change = cocktail_for_change

    await callback.answer()
    await callback.message.answer(
        "Введіть назву коктейля", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddCocktail.name)





# -------------------------------------------------------------------------------- Код ниже для машины состояний (FSM)


@admin_router.message(StateFilter(None), F.text == "Додати коктейль" or "add")
async def add_cocktail(message: types.Message, state: FSMContext):
    await message.answer(
        "Введіть назву коктейлю", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddCocktail.name)


@admin_router.message(StateFilter("*"), Command("скидання"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "скидання")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if not current_state:
        return
    await state.clear()
    await message.answer("Все скинуто", reply_markup=admin_key_board)


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddCocktail.name:
        await message.answer(
            "Це перший крок, напишіть назву товара або оберіть відміну"
        )
        return
    previous = None

    for step in AddCocktail.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок ви повернулись до попереднього кроку \n{AddCocktail.texts[previous.state]}"
            )
            return
        previous = step


@admin_router.message(StateFilter(AddCocktail.name), F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть опис коктейлю")
    await state.set_state(AddCocktail.description)


@admin_router.message(StateFilter(AddCocktail.description), F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введіть вартість коктейлю")
    await state.set_state(AddCocktail.price)


@admin_router.message(StateFilter(AddCocktail.price), F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Завантажте зображення коктейлю")
    await state.set_state(AddCocktail.image)


@admin_router.message(StateFilter(AddCocktail.image), F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Коктейль додано", reply_markup=admin_key_board)
    try:
        data = await state.get_data()
        await repository_add_cocktail(session, data)
        await state.clear()
    except Exception as e:
        await message.answer(
            "Коктейль не додано, зверніться до программіста він знову хоче грошей"
        )
        await state.clear()
        logging.error(f"Ошибка при добавлении коктейля: {e}")
