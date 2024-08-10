import pytest_asyncio

from db.postgresql import Item, Category


@pytest_asyncio.fixture
async def item_factory_single(pg_session):
    item = Item(id=1, name='test', description='test', category_id=None, quantity=1, price=1)
    pg_session.add(item)
    await pg_session.commit()
    await pg_session.refresh(item)
    return item


@pytest_asyncio.fixture
async def category_factory_single(pg_session):
    category = Category(id=1, name='test', description='test')
    pg_session.add(category)
    await pg_session.commit()
    await pg_session.refresh(category)
    return category
