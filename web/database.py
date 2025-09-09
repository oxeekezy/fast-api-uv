from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from web.settins import settings
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(f"postgres+asyncpg://{settings.POSTGRES_HOST}:{settings.POSTGRES_HOST}")

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass