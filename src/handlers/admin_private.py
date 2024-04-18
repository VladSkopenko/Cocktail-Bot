from aiogram import F, Router, types
from aiogram.filters import Command
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


@admin_router.message(F.text == "Додати коктейль")
async def add_product(message: types.Message):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )


@admin_router.message(Command("відміна"))
@admin_router.message(F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message) -> None:
    await message.answer("Галя відміна", reply_markup=admin_key_board)


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message) -> None:
    await message.answer(f"Ок, вы повернулись до попереденього кроку")


@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer("Введіть опис коктейлю")


@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer("Введіть вартість коктейлю")


@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer("Завантажте зображення коктейлю")


@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer("Коктейль додано", reply_markup=admin_key_board)
