from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from src.database.models import Base

db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
engine = create_async_engine(db_url, echo=True)
session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)



async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
