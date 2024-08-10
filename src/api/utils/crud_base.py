from abc import ABC
from typing import TypeVar, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class CrudBase(ABC):
    """
    Base class for CRUD operations
    """
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, values: dict) -> T:
        raise NotImplementedError

    async def get_by_id(self, id_: int) -> T:
        raise NotImplementedError

    async def get(self, offset: int, limit: int) -> Sequence[T]:
        raise NotImplementedError

    async def delete(self, id_: int) -> T:
        raise NotImplementedError

    async def update(self, id_: int, values: dict) -> T:
        raise NotImplementedError
