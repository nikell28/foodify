from foodify.models.base import BaseModel, OrmBaseModel
from foodify.models.ingredients import Ingredient


class User(BaseModel):
    tg_id: str
    tg_username: str | None = None
    tg_first_name: str
    favorite_ingredients: list[Ingredient] = []
    unloved_ingredients: list[Ingredient] = []


class UserCreate(OrmBaseModel):
    tg_id: str
    tg_username: str | None = None
    tg_first_name: str
