from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from api.inventory.item.exceptions import ItemNotFoundException, ItemCreationError, ItemUpdateError, ItemDeleteError
from api.utils.crud_base import CrudBase
from db.postgresql import Item


class ItemCrud(CrudBase):
    async def get_by_id(self, id_) -> Item:
        item = await self.session.scalars(
            select(Item).where(Item.id == id_).options(joinedload(Item.category))
        )
        item = item.first()
        if item is None:
            raise ItemNotFoundException()
        return item

    async def get(self, offset: int, limit: int) -> Sequence[Item]:
        items = await self.session.scalars(
            select(Item).offset(offset).limit(limit).options(joinedload(Item.category))
        )
        return items.all()

    async def create(self, values: dict) -> Item:
        new_item = Item(**values)
        self.session.add(new_item)
        try:
            await self.session.commit()
            await self.session.refresh(new_item, attribute_names=['category'])
        except IntegrityError as exc:
            raise ItemCreationError(detail=str(exc))
        return new_item

    async def update(self, id_: int, values: dict) -> Item:
        item_for_update = await self.get_by_id(id_)
        if item_for_update is None:
            raise ItemNotFoundException()
        try:
            new_item = await self.session.scalars(
                update(Item).where(Item.id == id_).values(**values).returning(Item)
            )
        except IntegrityError as exc:
            raise ItemUpdateError(detail=str(exc))
        return new_item.one()

    async def delete(self, id_: int) -> Item:
        item_for_deletion = await self.get_by_id(id_)
        if item_for_deletion is None:
            raise ItemNotFoundException()
        try:
            deleted_item = await self.session.scalars(delete(Item).where(Item.id == id_).returning(Item))
        except IntegrityError as exc:
            raise ItemDeleteError(detail=str(exc))
        return deleted_item.one()
