from api.utils.exceptions import BaseInventoryException


class CategoryNotFoundException(BaseInventoryException):
    def __init__(self):
        super().__init__(status_code=404, detail='Category not found')


class CategoryCreationError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class CategoryUpdateError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class CategoryDeleteError(BaseInventoryException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)
