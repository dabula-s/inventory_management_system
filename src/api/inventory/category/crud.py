from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from api.inventory.category.exceptions import CategoryNotFoundException, CategoryCreationError, CategoryUpdateError, \
    CategoryDeleteError
from api.utils.crud_base import CrudBase
from db.postgresql import Category


class CategoryCrud(CrudBase):
    async def get_by_id(self, id_: int) -> Category:
        category = await self.session.scalars(select(Category).where(Category.id == id_))
        category = category.first()
        if category is None:
            raise CategoryNotFoundException()
        return category

    async def get(self, offset: int, limit: int) -> Sequence[Category]:
        categories = await self.session.scalars(select(Category).offset(offset).limit(limit))
        return categories.all()

    async def create(self, values: dict) -> Category:
        new_category = Category(**values)
        self.session.add(new_category)
        try:
            await self.session.commit()
            await self.session.refresh(new_category)
        except IntegrityError as exc:
            raise CategoryCreationError(detail=str(exc))
        return new_category

    async def update(self, id_: int, values: dict) -> Category:
        category_for_update = await self.get_by_id(id_)
        if category_for_update is None:
            raise CategoryNotFoundException()
        try:
            new_category = await self.session.scalars(
                update(Category).where(Category.id == id_).values(**values).returning(Category)
            )
        except IntegrityError as exc:
            raise CategoryUpdateError(detail=str(exc))
        return new_category.one()

    async def delete(self, id_: int) -> Category:
        category_for_deletion = await self.get_by_id(id_)
        if category_for_deletion is None:
            raise CategoryNotFoundException()
        try:
            deleted_category = await self.session.scalars(
                delete(Category).where(Category.id == id_).returning(Category)
            )
        except IntegrityError as exc:
            raise CategoryDeleteError(detail=str(exc))
        return deleted_category.one()
