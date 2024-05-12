from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
engine = create_async_engine(db_url, echo=True)
session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
