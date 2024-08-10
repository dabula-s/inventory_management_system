from __future__ import annotations

from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, computed_field, model_validator


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: int
    price: float


class Item(ItemBase):
    id: Optional[int] = None


class ItemWithCategory(Item):
    category_id: Optional[int] = Field(None, exclude=True)
    category: Optional['Category'] = Field(None, exclude=True)

    @computed_field
    def category_name(self) -> Optional[str]:
        try:
            return self.category.name
        except AttributeError:
            return None

    model_config = ConfigDict(
        from_attributes=True,
    )


from api.inventory.category.schemas import Category

ItemWithCategory.model_rebuild()


class CreateItemRequestSchema(ItemBase):
    ...


class CreateItemResponseSchema(ItemWithCategory):
    ...


class GetItemsRequestSchema(BaseModel):
    offset: int = Field(0, ge=0, description='Offset for pagination purposes')
    limit: int = Field(10, gt=0, description='Limit of items per page')


class GetItemsResponseSchema(BaseModel):
    items: list[ItemWithCategory]


class GetItemByIdRequestSchema(BaseModel):
    item_id: int = Query(..., description='Id of the item')


class GetItemByIdResponseSchema(ItemWithCategory):
    ...


class ItemUpdate(ItemBase):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, values):
        nullable_fields = ('description', 'category_id')
        if not (any(values.get(field) is not None for field in values if field not in nullable_fields)
                or any(values.get(field) is not None for field in values if field in nullable_fields)):
            raise ValueError('At least one field must be provided')
        return values


class UpdateItemRequestSchema(BaseModel):
    item_id: int = Query(..., description='Id of the item')
    values: ItemUpdate


class UpdateItemResponseSchema(ItemWithCategory):
    ...


class DeleteItemRequestSchema(BaseModel):
    item_id: int = Query(..., description='Id of the item')


class DeleteItemResponseSchema(Item):
    ...
