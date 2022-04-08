from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base, CreatedMixin, UpdatedMixin


class Town(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "town"

    name = Column(String(100), nullable=False)
    rating = Column(Integer, server_default="0")

    user = relationship("User")


class User(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "user"

    name = Column(String(100), nullable=True)
    user_name = Column(String(100), nullable=True)
    town_id = Column(Integer, ForeignKey("town.id"))


class Category(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "category"

    name = Column(String(100), nullable=False)
    description = Column(Text(), default=False)
    rating = Column(Integer, server_default="0")

    town_id = Column(Integer, ForeignKey("town.id"))
    parent_category_id = Column(Integer, ForeignKey("category.id"))


class MessageLog(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "message_log"

    text = Column(Text())
    user_id = Column(BigInteger)
    user_town_id = Column(Integer)
