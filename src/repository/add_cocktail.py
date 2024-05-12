from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

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


async def repository_get_cocktail_by_id(
    session: AsyncSession, cocktail_key: int, mode: str = "by_id"
):
    if mode == "by_id":
        query = select(Cocktail).where(Cocktail.id == cocktail_key)
    elif mode == "by_name":
        query = select(Cocktail).where(Cocktail.name == cocktail_key)
    else:
        raise ValueError(
            "Непідтримуваний режим. Режим повинен бути 'by_id' або 'by_name."
        )
    result = await session.execute(query)
    return result.scalar_one_or_none()
