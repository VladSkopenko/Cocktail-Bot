from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

start_key_boards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="Доставка"),
        ],
        {
            KeyboardButton(text="Про бота"),
            KeyboardButton(text="Оплата"),
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить ?'
)
