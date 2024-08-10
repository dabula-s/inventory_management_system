from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.postgresql.base import BaseModel


class Item(BaseModel):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Numeric, nullable=False, default=0)

    category = relationship('Category', back_populates='items')


class Category(BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    items = relationship('Item', collection_class=list, back_populates='category')


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
#
#
# class Role(BaseModel):
#     __tablename__ = 'role'
