from sqlalchemy import Column, String

from foodify.db.base import Base


class Ingredients(Base):
    __tablename__ = "ingredients"

    name = Column(String, unique=True, nullable=False)
