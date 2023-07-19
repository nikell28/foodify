import pydantic

from foodify.models.ingredients import Ingredient


class Recipient(pydantic.BaseModel):
    description: str


class RecipientInput(pydantic.BaseModel):
    favorite_ingredients: list[Ingredient]
    unloved_ingredients: list[Ingredient]
