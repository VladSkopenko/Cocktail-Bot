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
