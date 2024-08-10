from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD

async_connection_url = ('postgresql+asyncpg://'
                        f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                        f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
async_engine = create_async_engine(async_connection_url)

sync_connection_url = ('postgresql://'
                       f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
sync_engine = create_engine(sync_connection_url)


class BaseModel(DeclarativeBase):
    ...


metadata = BaseModel.metadata
