from api.utils.exceptions import BaseInventoryException


class ItemNotFoundException(BaseInventoryException):
    def __init__(self):
        super().__init__(status_code=404, detail='Item not found')


class ItemCreationError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class ItemUpdateError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class ItemDeleteError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)
