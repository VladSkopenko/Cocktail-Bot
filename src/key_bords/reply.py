from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

start_key_boards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="Доставка"),
        ],

        {
            KeyboardButton(text="Про бота"),
            KeyboardButton(text="Оплата"),
            KeyboardButton(text='Залишити відгук'),
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить ?'
)

delete_key_boards = ReplyKeyboardRemove()
