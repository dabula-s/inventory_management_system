from contextlib import contextmanager, asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from db.postgresql import async_engine


async def get_async_session():
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            _AsyncSession = async_sessionmaker(bind=connection)
            async with _AsyncSession() as session:
                try:
                    yield session
                    await session.commit()
                except:  # noqa:E722
                    await transaction.rollback()
                    raise


async_session_manager = asynccontextmanager(get_async_session)
