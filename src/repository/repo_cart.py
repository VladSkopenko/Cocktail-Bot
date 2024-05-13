from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database.models import Cart


async def repository_add_to_cart(session: AsyncSession, user_id: int, cocktail_id: int):
    query = (
        select(Cart)
        .where(Cart.user_id == user_id, Cart.cocktail_id == cocktail_id)
        .options(joinedload(Cart.cocktail))
    )
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(user_id=user_id, cocktail_id=cocktail_id, quantity=1))
        await session.commit()


async def repository_get_user_carts(session: AsyncSession, user_id):
    query = (
        select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.cocktail))
    )
    result = await session.execute(query)
    return result.scalars().all()


async def repository_delete_from_cart(
    session: AsyncSession, user_id: int, cocktail_id: int
):
    query = delete(Cart).where(Cart.user_id == user_id, Cart.cocktail_id == cocktail_id)
    await session.execute(query)
    await session.commit()


async def repository_reduce_product_in_cart(
    session: AsyncSession, user_id: int, cocktail_id: int
):
    query = (
        select(Cart)
        .where(Cart.user_id == user_id, Cart.cocktail_id == cocktail_id)
        .options(joinedload(Cart.cocktail))
    )
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await repository_delete_from_cart(session, user_id, cocktail_id)
        await session.commit()
        return False
