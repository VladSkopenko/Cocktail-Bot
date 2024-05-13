from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from src.common.text_for_db import categories as bd_categories
from src.database.connect import engine
from src.database.connect import session_maker
from src.database.models import Category


async def repository_create_categories(session: AsyncSession, categories: list):
    for category in categories:
        session.add(Category(name=category))
    await session.commit()


async def main():
    async with session_maker() as session:
        await repository_create_categories(session, bd_categories)


if __name__ == "__main__":
    asyncio.run(main())
