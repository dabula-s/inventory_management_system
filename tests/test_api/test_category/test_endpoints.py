import pytest
from sqlalchemy import select

from api.inventory.category.schemas import (
    CategoryUpdate, UpdateCategoryRequestSchema,
    GetCategoryByIdRequestSchema, GetCategoriesRequestSchema, CreateCategoryRequestSchema, DeleteCategoryRequestSchema,
)
from db.postgresql import Category


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (GetCategoryByIdRequestSchema(category_id=1), 200),
        (GetCategoryByIdRequestSchema.model_construct({'item_id'}, category_id='test'), 422),
        (GetCategoryByIdRequestSchema(category_id=2), 404),
    ]
)
async def test_get_category_by_id(
    client,
    pg_session,
    category_factory_single,
    request_,
    expected_status_code,
):
    response = await client.get(f'/categories/{request_.category_id}')
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        json = response.json()
        assert json['id'] == request_.category_id


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (GetCategoriesRequestSchema(), 200),
        (GetCategoriesRequestSchema(limit=1, offset=0), 200),
        (GetCategoriesRequestSchema(limit=100, offset=5), 200),
        (GetCategoriesRequestSchema.model_construct({'limit'}, limit='test'), 422),
    ]
)
async def test_get_categories(
    client,
    pg_session,
    request_,
    expected_status_code,
):
    response = await client.get(f'/categories/', params=request_.model_dump(exclude_unset=True))
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        json = response.json()
        assert 'categories' in json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (UpdateCategoryRequestSchema(category_id=1, values=CategoryUpdate(description='another')), 200),
        (UpdateCategoryRequestSchema(category_id=1, values=CategoryUpdate(name='another')), 200),
        (UpdateCategoryRequestSchema(category_id=1, values=CategoryUpdate(category_id=2)), 422),
        (UpdateCategoryRequestSchema(category_id=2, values=CategoryUpdate(name='another')), 404),
    ]
)
async def test_update_category(
    pg_session,
    client,
    category_factory_single,
    request_,
    expected_status_code,
):
    body = request_.values.model_dump(exclude_unset=True, exclude_defaults=True)
    response = await client.put(f'/categories/{request_.category_id}', json=body)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        await pg_session.refresh(category_factory_single)
        for field, value in body.items():
            assert getattr(category_factory_single, field) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (CreateCategoryRequestSchema(name='test_', description='test'), 201),
        (CreateCategoryRequestSchema(name='test_'), 201),
        (CreateCategoryRequestSchema(name='test'), 422),
        (CreateCategoryRequestSchema.model_construct({'test'}, test='test'), 422),
        (CreateCategoryRequestSchema.model_construct({'name'}, name=None), 422),
    ]
)
async def test_create_category(
    pg_session,
    client,
    category_factory_single,
    request_,
    expected_status_code,
):
    body = request_.model_dump()
    response = await client.post(f'/categories/', json=body)
    assert response.status_code == expected_status_code
    if expected_status_code == 201:
        new_item = await pg_session.scalars(select(Category).where(Category.name == body['name']))
        new_item = new_item.first()
        for field, value in body.items():
            assert getattr(new_item, field) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['request_', 'expected_status_code'],
    [
        (DeleteCategoryRequestSchema(category_id=1), 200),
        (DeleteCategoryRequestSchema(category_id=2), 404),
        (DeleteCategoryRequestSchema.model_construct({'category_id'}, category_id='null'), 422),
    ]
)
async def test_delete_category(
    pg_session,
    client,
    category_factory_single,
    request_,
    expected_status_code,
):
    response = await client.delete(f'/categories/{request_.category_id}')
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        category = await pg_session.scalars(select(Category).where(Category.id == request_.category_id))
        category = category.first()
        assert category is None