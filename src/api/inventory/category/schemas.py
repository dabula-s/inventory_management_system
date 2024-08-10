from __future__ import annotations

from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, model_validator


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class Category(CategoryBase):
    id: Optional[int] = None


class CategoryWithItems(Category):
    items: Optional[list[Item]] = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# to avoid circular imports with Item
from api.inventory.item.schemas import Item

CategoryWithItems.model_rebuild()


class CreateCategoryRequestSchema(CategoryBase):
    ...


class CreateCategoryResponseSchema(Category):
    ...


class GetCategoriesRequestSchema(BaseModel):
    offset: int = Field(0, ge=0, description='Offset for pagination purposes')
    limit: int = Field(10, gt=0, description='Limit of categories per page')


class GetCategoriesResponseSchema(BaseModel):
    categories: list[Category]


class GetCategoryByIdRequestSchema(BaseModel):
    category_id: int = Query(..., description='Id of the category')


class GetCategoryByIdResponseSchema(Category):
    ...


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, values):
        nullable_fields = ('description',)
        if not (any(values.get(field) is not None for field in values if field not in nullable_fields)
                or any(values.get(field) is not None for field in values if field in nullable_fields)):
            raise ValueError('At least one field must be provided')
        return values


class UpdateCategoryRequestSchema(BaseModel):
    category_id: int = Query(..., description='Id of the category')
    values: CategoryUpdate


class UpdateCategoryResponseSchema(Category):
    ...


class DeleteCategoryRequestSchema(BaseModel):
    category_id: int = Query(..., description='Id of the category')


class DeleteCategoryResponseSchema(Category):
    ...
