from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from web.settins import settings
from sqlalchemy.orm import DeclarativeBase


ENGINE = create_async_engine(settings.database_url)

ASYNC_SESSION_MAKER = async_sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass