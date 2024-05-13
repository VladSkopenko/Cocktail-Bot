from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ['Gin', 'Rum', "Tequila", "Whiskey", "Vodka", "Brandy", "Other"]

description_for_info_pages = {
    "main": "Добро пожаловать!",
    "about": "Online-bar-bot.\nЧас роботи: 10:00 - 22:00.",
    "payment": as_marked_section(
        Bold("Варіанти оплати:"),
        "Карткою в боті",
        "При отриманні карта/кеш",
        "В закладі",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варіанти доставки/заказа:"),
            "Курьер",
            "Самовивіз",
            marker="✅ ",
        ),
        as_marked_section(Bold("Нельзя:"), "Пошта", "Голубка", marker="❌ "),
        sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Категории:',
    'cart': 'В кошику нічого немає!'
}
