from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from src.key_bords.inline import get_products_buttons
from src.key_bords.inline import get_user_cart
from src.key_bords.inline import get_user_catalog_buttons
from src.key_bords.inline import get_user_main_buttons
from src.repository.banner import repository_get_banner
from src.repository.cart import repository_add_to_cart
from src.repository.cart import repository_delete_from_cart
from src.repository.cart import repository_get_user_carts
from src.repository.cart import repository_reduce_product_in_cart
from src.repository.category import repository_get_categories
from src.repository.cocktail import repository_get_all_cocktails
from src.utils.paginator import Paginator


async def main_menu(session, level, menu_name):
    banner = await repository_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    key_boards = get_user_main_buttons(level=level)

    return image, key_boards


async def catalog(session, level, menu_name):
    banner = await repository_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    categories = await repository_get_categories(session)
    key_boards = get_user_catalog_buttons(level=level, categories=categories)

    return image, key_boards


def pages(paginator: Paginator):
    buttons = dict()
    if paginator.has_previous():
        buttons["◀ Пред."] = "previous"

    if paginator.has_next():
        buttons["След. ▶"] = "next"

    return buttons


async def cocktails(session, level, category, page):
    cocktails_list = await repository_get_all_cocktails(session, category_id=category)

    paginator = Paginator(cocktails_list, page=page)
    cocktail = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=cocktail.image,
        caption=f"<strong>{cocktail.name}\
                </strong>\n{cocktail.description}\nВартість: {round(cocktail.price, 2)}\n\
                <strong>Коктейль {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_buttons = pages(paginator)

    buttons = get_products_buttons(
        level=level,
        category=category,
        page=page,
        pagination_buttons=pagination_buttons,
        cocktail_id=cocktail.id,
    )

    return image, buttons


async def carts(session, level, menu_name, page, user_id, cocktail_id):
    if menu_name == "delete":
        await repository_delete_from_cart(session, user_id, cocktail_id)
        if page > 1:
            page -= 1
    elif menu_name == "decrement":
        is_cart = await repository_reduce_product_in_cart(session, user_id, cocktail_id)
        if page > 1 and not is_cart:
            page -= 1
    elif menu_name == "increment":
        await repository_add_to_cart(session, user_id, cocktail_id)

    carts_list = await repository_get_user_carts(session, user_id)

    if not carts_list:
        banner = await repository_get_banner(session, "cart")
        image = InputMediaPhoto(
            media=banner.image, caption=f"<strong>{banner.description}</strong>"
        )

        key_boards = get_user_cart(
            level=level,
            page=None,
            pagination_buttons=None,
            cocktail_id=None,
        )

    else:
        paginator = Paginator(carts_list, page=page)

        cart = paginator.get_page()[0]

        cart_price = round(cart.quantity * cart.cocktail.price, 2)
        total_price = round(
            sum(cart.quantity * cart.cocktail.price for cart in carts_list), 2
        )
        image = InputMediaPhoto(
            media=cart.cocktail.image,
            caption=f"<strong>{cart.cocktail.name}</strong>\n{cart.cocktail.price}$ x {cart.quantity} = {cart_price}$\
                    \nТовар {paginator.page} из {paginator.pages} в корзині.\nЗагальна вартість замовлення: {total_price}",
        )

        pagination_buttons = pages(paginator)

        key_boards = get_user_cart(
            level=level,
            page=page,
            pagination_buttons=pagination_buttons,
            cocktail_id=cart.cocktail.id,
        )

    return image, key_boards


async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    page: int | None = None,
    cocktail_id: int | None = None,
    user_id: int | None = None,
):
    if level == 0:
        return await main_menu(session, level, menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)
    elif level == 2:
        return await cocktails(session, level, category, page)
    elif level == 3:
        return await carts(session, level, menu_name, page, user_id, cocktail_id)
