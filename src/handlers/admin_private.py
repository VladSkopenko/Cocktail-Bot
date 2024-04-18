from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

from src.filters.chat_types import ChatTypeFilter, IsAdmin
from src.key_bords.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

admin_key_board = get_keyboard(
    "Додати коктейль",
    "Видалити коктейль",
    "Змінити коктейль",
    "Показати всі коктейлі",
    placeholder="Оберіть дію",
    sizes=(2, 2)
)


@admin_router.message(Command("admin"))
async def start_work(message: types.Message):
    await message.answer("Що бажаєте зробити?", reply_markup=admin_key_board)


@admin_router.message(F.text == "Показати всі коктейлі")
async def starring_at_product(message: types.Message):
    await message.answer("ОК, ось список коктейлів")


@admin_router.message(F.text == "Змінити коктейль")
async def change_product(message: types.Message):
    await message.answer("ОК, ось список коктейлів")


@admin_router.message(F.text == "Видалити коктейль")
async def delete_product(message: types.Message):
    await message.answer("Оберіть товар(и) для видалення")


# -------------------------------------------------------------------------------- Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()


@admin_router.message(StateFilter(None), F.text == "Додати коктейль")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введіть назву коктейлю", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("відміна"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if not current_state:
        return
    await state.clear()
    await message.answer("Галя відміна", reply_markup=admin_key_board)


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Ок, вы повернулись до попереденього кроку")


@admin_router.message(StateFilter(AddProduct.name), F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть опис коктейлю")
    await state.set_state(AddProduct.description)


@admin_router.message(StateFilter(AddProduct.description), F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введіть вартість коктейлю")
    await state.set_state(AddProduct.price)


@admin_router.message(F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Завантажте зображення коктейлю")
    await state.set_state(AddProduct.image)


@admin_router.message(F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Коктейль додано", reply_markup=admin_key_board)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
