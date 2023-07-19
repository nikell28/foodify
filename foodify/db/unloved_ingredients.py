from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from foodify.db.base import Base
from foodify.db.users import Users
from foodify.db.ingredients import Ingredients


class UnlovedIngredients(Base):
    __tablename__ = "unloved_ingredients"

    user_id = Column(UUID, ForeignKey(Users.id))
    ingredient_id = Column(UUID, ForeignKey(Ingredients.id))
