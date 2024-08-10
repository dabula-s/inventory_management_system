import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import database_exists, create_database

from db.postgresql import sync_connection_url, async_connection_url, get_async_session
from main import app

pytest_plugins = ['pytest_asyncio']


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def create_db():
    if not database_exists(url=sync_connection_url):
        create_database(url=sync_connection_url)
    alembic_config = Config('alembic.ini', ini_section='postgresql')
    command.upgrade(alembic_config, 'head')


@pytest_asyncio.fixture()
async def pg_session():
    async_engine = create_async_engine(async_connection_url)
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            _AsyncSession = async_sessionmaker(bind=connection)
            async with _AsyncSession() as session:
                yield session
            await transaction.rollback()


@pytest.fixture(autouse=True)
def override_app_dependency_get_db(pg_session):
    async def get_db_override():
        yield pg_session

    app.dependency_overrides[get_async_session] = get_db_override
