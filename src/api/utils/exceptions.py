from fastapi import HTTPException


class BaseInventoryException(HTTPException):
    ...
