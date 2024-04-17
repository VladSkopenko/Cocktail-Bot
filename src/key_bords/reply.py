from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

start_key_boards = ReplyKeyboardMarkup(
    keybord=[
        KeyboardButton(text="Меню"),
        KeyboardButton(text="Про бота"),
        KeyboardButton(text="Оплата"),
        KeyboardButton(text="Доставка"),
        KeyboardButton(text="Меню"),

    ]
)
