from aiogram import F, Router, types
from aiogram.filters import Command

from src.filters.chat_types import ChatTypeFilter, IsAdmin
from src.key_bords.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


admin_key_board = get_keyboard(
    "Додати коктейль",
    "Видалити коктейль",
    "Змінити коктейль",
    placeholder="Оберіть дію",
    sizes=(1, 1, 1),
)

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=admin_key_board)

