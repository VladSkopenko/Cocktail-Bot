from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.database.models import Cocktail


async def repository_add_cocktail(session: AsyncSession, data: dict):
    cocktail = Cocktail(
        name=data["name"],
        description=data["description"],
        image=data["image"],
        price=float(data["price"]),
    )
    session.add(cocktail)
    await session.commit()


async def repository_get_all_cocktails(session: AsyncSession):
    query = select(Cocktail)
    result = await session.execute(query)
    return result.scalars().all()


async def repository_get_cocktail(
    session: AsyncSession, cocktail_id: int
):
    query = select(Cocktail).where(Cocktail.id == cocktail_id)
    result = await session.execute(query)
    return result.scalar()


async def repository_delete_cocktail_by_id(session: AsyncSession, cocktail_id: int):
    query = delete(Cocktail).where(Cocktail.id == cocktail_id)
    await session.execute(query)
    await session.commit()


async def repository_update_product(session: AsyncSession, cocktail_id: int, data):
    query = update(Cocktail).where(Cocktail.id == cocktail_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()
