import pytest
from sqlalchemy import select

from api.inventory.item.schemas import (
    ItemUpdate, UpdateItemRequestSchema,
    GetItemByIdRequestSchema, GetItemsRequestSchema, CreateItemRequestSchema, DeleteItemRequestSchema,
)
from db.postgresql import Item


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (GetItemByIdRequestSchema(item_id=1), 200),
        (GetItemByIdRequestSchema.model_construct({'item_id'}, item_id='test'), 422),
        (GetItemByIdRequestSchema(item_id=2), 404),
    ]
)
async def test_get_item_by_id(
    client,
    pg_session,
    item_factory_single,
    category_factory_single,
    request_,
    expected_status_code,
):
    response = await client.get(f'/items/{request_.item_id}')
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        json = response.json()
        assert json['id'] == request_.item_id


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (GetItemsRequestSchema(), 200),
        (GetItemsRequestSchema(limit=1, offset=0), 200),
        (GetItemsRequestSchema(limit=100, offset=5), 200),
        (GetItemsRequestSchema.model_construct({'limit'}, limit='test'), 422),
    ]
)
async def test_get_items(
    client,
    pg_session,
    item_factory_single,
    request_,
    expected_status_code,
):
    response = await client.get(f'/items/', params=request_.model_dump(exclude_unset=True))
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        json = response.json()
        assert 'items' in json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (UpdateItemRequestSchema(item_id=1, values=ItemUpdate(description='another')), 200),
        (UpdateItemRequestSchema(item_id=1, values=ItemUpdate(category_id=1)), 200),
        (UpdateItemRequestSchema(item_id=1, values=ItemUpdate(category_id=2)), 422),
        (UpdateItemRequestSchema(item_id=2, values=ItemUpdate(category_id=2)), 404),
    ]
)
async def test_update_item(
    pg_session,
    client,
    item_factory_single,
    category_factory_single,
    request_,
    expected_status_code,
):
    body = request_.values.model_dump(exclude_unset=True, exclude_defaults=True)
    response = await client.put(f'/items/{request_.item_id}', json=body)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        await pg_session.refresh(item_factory_single)
        for field, value in body.items():
            assert getattr(item_factory_single, field) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (CreateItemRequestSchema(name='test_', description='test', quantity=1, price=1), 201),
        (CreateItemRequestSchema(name='test_', quantity=1, price=1), 201),
        (CreateItemRequestSchema(name='test', category_id=1, quantity=1, price=1), 422),
        (CreateItemRequestSchema(name='test', category_id=2, quantity=1, price=1), 422),
        (CreateItemRequestSchema.model_construct({'test'}, test='test'), 422),
        (CreateItemRequestSchema.model_construct({'name'}, name=None), 422),
    ]
)
async def test_create_item(
    pg_session,
    client,
    item_factory_single,
    category_factory_single,
    request_,
    expected_status_code,
):
    body = request_.model_dump()
    response = await client.post(f'/items/', json=body)
    assert response.status_code == expected_status_code
    if expected_status_code == 201:
        new_item = await pg_session.scalars(select(Item).where(Item.name == body['name']))
        new_item = new_item.first()
        for field, value in body.items():
            assert getattr(new_item, field) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (DeleteItemRequestSchema(item_id=1), 200),
        (DeleteItemRequestSchema(item_id=2), 404),
        (DeleteItemRequestSchema.model_construct({'item_id'}, item_id=None), 422),
    ]
)
async def test_delete_item(
    pg_session,
    client,
    item_factory_single,
    request_,
    expected_status_code,
):
    response = await client.delete(f'/items/{request_.item_id}')
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        item = await pg_session.scalars(select(Item).where(Item.id == request_.item_id))
        item = item.first()
        assert item is None
