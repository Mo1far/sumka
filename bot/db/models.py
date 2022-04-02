from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String, Text,
)
from sqlalchemy.orm import relationship

from .base import Base


class Town(Base):
    __tablename__ = "town"

    name = Column(String(100), nullable=False)
    rating = Column(Integer, default=0)

    user = relationship("User")


class User(Base):
    __tablename__ = "user"

    name = Column(String(100), nullable=True)
    user_name = Column(String(100), nullable=False)
    town_id = Column(Integer, ForeignKey("town.id"))


class Category(Base):
    __tablename__ = "category"

    name = Column(String(100), nullable=False)
    description = Column(Text, default=False)
    rating = Column(Integer, default=0)

    town_id = Column(Integer, ForeignKey("town.id"))
    parent_category_id = Column(Integer, ForeignKey("category.id"))
