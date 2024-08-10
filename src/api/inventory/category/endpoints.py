from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.exc import IntegrityError
from starlette import status

from api.inventory.category.crud import CategoryCrud
from api.inventory.category.exceptions import CategoryCreationError
from api.inventory.category.schemas import (
    GetCategoriesRequestSchema, GetCategoriesResponseSchema,
    GetCategoryByIdRequestSchema, GetCategoryByIdResponseSchema,
    CreateCategoryRequestSchema, CreateCategoryResponseSchema,
    UpdateCategoryRequestSchema, UpdateCategoryResponseSchema,
    DeleteCategoryRequestSchema, DeleteCategoryResponseSchema,
)
from api.users.auth import current_active_superuser
from db.postgresql import get_async_session

logger = getLogger(__name__)
router = APIRouter(
    prefix="/categories",
    tags=["category"],
    dependencies=[Depends(current_active_superuser)],
)


@router.get(
    "/",
    response_model=GetCategoriesResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    params: Annotated[GetCategoriesRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    categories = await CategoryCrud(db_session).get(**params.model_dump())
    return {'categories': categories}


@router.get(
    "/{category_id}",
    response_model=GetCategoryByIdResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    params: Annotated[GetCategoryByIdRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    item = await CategoryCrud(db_session).get_by_id(id_=params.category_id)
    return item


@router.post(
    "/",
    response_model=CreateCategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    params: Annotated[CreateCategoryRequestSchema, Body()],
    db_session=Depends(get_async_session),
):
    try:
        new_item = await CategoryCrud(session=db_session).create(values=params.model_dump())
    except IntegrityError as exc:
        raise CategoryCreationError(detail=str(exc))
    return new_item


@router.put(
    "/{category_id}",
    response_model=UpdateCategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    params: Annotated[UpdateCategoryRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    new_item = await CategoryCrud(session=db_session).update(
        id_=params.category_id,
        values=params.values.model_dump(exclude_unset=True, exclude_defaults=True),
    )
    return new_item


@router.delete(
    "/{category_id}",
    response_model=DeleteCategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def delete_category(
    params: Annotated[DeleteCategoryRequestSchema, Depends()], db_session=Depends(get_async_session)
):
    deleted_category = await CategoryCrud(session=db_session).delete(id_=params.category_id)
    return deleted_category
