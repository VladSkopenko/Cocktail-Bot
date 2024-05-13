from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from src.database.models import Base
from src.common.text_for_db import categories, description_for_info_pages
from src.repository.repo_banner import repository_add_banner_description
from src.repository.repo_category import repository_create_categories

db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
engine = create_async_engine(db_url, echo=True)
session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await repository_create_categories(session, categories)
        await repository_add_banner_description(session, description_for_info_pages)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

