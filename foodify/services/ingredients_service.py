import uuid

from foodify.models.ingredient import Ingredient
from foodify.repositories.ingredients import IngredientsRepository


class IngredientsService:
    def __init__(self):
        self.__ingredients_repository = IngredientsRepository()

    async def get_all(self) -> list[Ingredient]:
        return await self.__ingredients_repository.get_all()

    async def get_by_id(self, ingredient_id: uuid.UUID) -> Ingredient | None:
        return await self.__ingredients_repository.get_by_id(ingredient_id)

    async def get_by_name(self, name: str) -> Ingredient | None:
        return await self.__ingredients_repository.get_by_name(name)
