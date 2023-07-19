import uuid
from foodify.models.base import BaseModel, OrmBaseModel


class Ingredient(BaseModel):
    name: str


class IngredientCreate(OrmBaseModel):
    name: str


class _FavoriteUnlovedIngredientCreate(OrmBaseModel):
    ingredient_id: uuid.UUID
    user_id: uuid.UUID


class FavoriteIngredientCreate(_FavoriteUnlovedIngredientCreate):
    ...


class UnlovedIngredientCreate(_FavoriteUnlovedIngredientCreate):
    ...
