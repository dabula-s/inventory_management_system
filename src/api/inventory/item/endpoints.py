from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from starlette import status

from api.inventory.item.crud import ItemCrud
from api.inventory.item.schemas import (
    GetItemsRequestSchema, GetItemsResponseSchema,
    GetItemByIdRequestSchema, GetItemByIdResponseSchema,
    CreateItemRequestSchema, CreateItemResponseSchema,
    UpdateItemRequestSchema, UpdateItemResponseSchema,
    DeleteItemRequestSchema, DeleteItemResponseSchema,
)
from api.users.auth import current_active_user
from db.postgresql import get_async_session

logger = getLogger(__name__)
router = APIRouter(
    prefix="/items",
    tags=["item"],
    dependencies=[Depends(current_active_user)],
)


@router.get(
    "/",
    response_model=GetItemsResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_items(
    params: Annotated[GetItemsRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    items = await ItemCrud(db_session).get(**params.model_dump())
    return {'items': items}


@router.get(
    "/{item_id}",
    response_model=GetItemByIdResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_item_by_id(
    params: Annotated[GetItemByIdRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    item = await ItemCrud(db_session).get_by_id(id_=params.item_id)
    return item


@router.post(
    "/",
    response_model=CreateItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    params: Annotated[CreateItemRequestSchema, Body()],
    db_session=Depends(get_async_session),
):
    new_item = await ItemCrud(session=db_session).create(values=params.model_dump())
    return new_item


@router.put(
    "/{item_id}",
    response_model=UpdateItemResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    params: Annotated[UpdateItemRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    updated_item = await ItemCrud(session=db_session).update(
        id_=params.item_id,
        values=params.values.model_dump(exclude_unset=True, exclude_defaults=True)
    )
    return updated_item


@router.delete(
    "/{item_id}",
    response_model=DeleteItemResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def delete_item(
    params: Annotated[DeleteItemRequestSchema, Depends()],
    db_session=Depends(get_async_session),
):
    deleted_item = await ItemCrud(session=db_session).delete(id_=params.item_id)
    return deleted_item
