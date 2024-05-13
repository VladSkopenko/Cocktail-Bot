from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.filters import or_f
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.patterns_for_command import ADMIN
from src.filters.chat_types import ChatTypeFilter
from src.filters.chat_types import IsAdmin
from src.key_bords.inline import get_callback_btns
from src.key_bords.reply import get_keyboard
from src.loger.loger import logging
from src.repository.repo_category import repository_get_categories
from src.repository.repo_cockt import repository_add_cocktail
from src.repository.repo_cockt import repository_delete_cocktail_by_id
from src.repository.repo_cockt import repository_get_cocktail
from src.repository.repo_cockt import repository_update_cocktail

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

admin_key_board = get_keyboard(
    "Додати коктейль",
    "Асортимент",
    "Додати/Змінити баннер",
    placeholder="Оберіть дію",
    sizes=(2,),
)


class AddCocktail(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    category = State()

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
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await repository_get_categories(session)
    btns = {category.name: f"category_{category.id}" for category in categories}
    await message.answer(
        "Оберіть категорію", reply_markup=get_callback_btns(btns=btns)
    )


@admin_router.callback_query(F.data.startswith("category_"))
async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split("_")[-1]
    category_id = int(category_id)
    for cocktail in await repository_get_cocktail(session, category_id):
        await callback.message.answer_photo(
            cocktail.image,
            caption=f"<strong>{cocktail.name}\
                    </strong>\n{cocktail.description}\nСтоимость: {round(cocktail.price, 2)}",
            reply_markup=get_callback_btns(
                btns={
                    "Видалити": f"delete_{cocktail.id}",
                    "Змінити": f"change_{cocktail.id}",
                },
                sizes=(2,),
            ),
        )
    await callback.answer()
    await callback.message.answer("ОК, ось список коктейлів в асортименті ⏫")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_cocktail(callback: types.CallbackQuery, session: AsyncSession):
    cocktail_id = int(callback.data.split("_")[-1])
    await repository_delete_cocktail_by_id(session, cocktail_id)
    await callback.answer("Коктейль видалено!⏫")
    await callback.message.answer("Коктейль видалено!⏫")


@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_cocktail_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    cocktail_id = callback.data.split("_")[-1]
    cocktail_id = int(cocktail_id)

    cocktail_for_change = await repository_get_cocktail(session, cocktail_id)

    AddCocktail.cocktail_for_change = cocktail_for_change

    await callback.answer("Коктейль вибрано!⏫")
    await callback.message.answer(
        "Введіть нову назву або '-' щоб пропустити це поле",
        reply_markup=types.ReplyKeyboardRemove(),
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
    if AddCocktail.cocktail_for_change:
        AddCocktail.cocktail_for_change = None
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


@admin_router.message(StateFilter(AddCocktail.name), or_f(F.text, F.text == "-"))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(name=AddCocktail.cocktail_for_change.name)
    else:
        await state.update_data(name=message.text)
    await message.answer("Введіть опис коктейлю")
    await state.set_state(AddCocktail.description)


@admin_router.message(StateFilter(AddCocktail.description), or_f(F.text, F.text == "-"))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(description=AddCocktail.cocktail_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введіть вартість коктейлю")
    await state.set_state(AddCocktail.price)


@admin_router.message(StateFilter(AddCocktail.price), or_f(F.text, F.text == "-"))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(price=AddCocktail.cocktail_for_change.price)
    else:
        await state.update_data(price=message.text)
    await message.answer("Завантажте зображення коктейлю")
    await state.set_state(AddCocktail.image)


@admin_router.message(StateFilter(AddCocktail.image), or_f(F.photo, F.text == "-"))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == "-":
        await state.update_data(image=AddCocktail.cocktail_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddCocktail.cocktail_for_change:
            await repository_update_cocktail(
                session, AddCocktail.cocktail_for_change.id, data
            )
        else:
            await repository_add_cocktail(session, data)
        await message.answer("Операція успішна", reply_markup=admin_key_board)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Помилка: \n{str(e)}\nЗверніться до програміста, він знову хоче грошей",
            reply_markup=admin_key_board,
        )
        logging.error(e)
        await state.clear()

    AddCocktail.cocktail_for_change = None
