import uuid

from foodify.repositories.base import BaseRepository
from foodify.db.ingredients import Ingredients
from foodify.db.favorite_ingredients import FavoriteIngredients
from foodify.db.unloved_ingredients import UnlovedIngredients
from foodify.models.ingredient import (
    Ingredient,
    FavoriteIngredientCreate,
    UnlovedIngredientCreate,
)


class _FavoriteIngredientsRepository(BaseRepository):
    table = FavoriteIngredients
    model_cls = Ingredient

    async def get_favorite_ingredients(self, user_id: uuid.UUID) -> list[Ingredient]:
        rows = await self._get_by_filter_with_wildcard(
            Ingredients, self.table.user_id.name, user_id
        )
        return [self.model_cls(**row) for row in rows]


class _UnlovedIngredientsRepository(BaseRepository):
    table = UnlovedIngredients
    model_cls = Ingredient

    async def get_unloved_ingredients(self, user_id: uuid.UUID) -> list[Ingredient]:
        rows = await self._get_by_filter_with_wildcard(
            Ingredients, self.table.user_id.name, user_id
        )
        return [self.model_cls(**row) for row in rows]


class IngredientsRepository(BaseRepository):
    table = Ingredients
    model_cls = Ingredient

    async def get_by_name(self, name: str) -> Ingredient | None:
        return await self.get_by(self.table.name.name, name)  # type: ignore

    async def get_favorite_ingredients(self, user_id: uuid.UUID) -> list[Ingredient]:
        return await _FavoriteIngredientsRepository(
            session_maker=self.session_maker
        ).get_favorite_ingredients(user_id)

    async def get_unloved_ingredients(self, user_id: uuid.UUID) -> list[Ingredient]:
        return await _UnlovedIngredientsRepository(
            session_maker=self.session_maker
        ).get_unloved_ingredients(user_id)

    async def add_favorite_ingredient(
        self, user_id: uuid.UUID, ingredient_id: uuid.UUID
    ) -> None:
        await _FavoriteIngredientsRepository(session_maker=self.session_maker).create(
            FavoriteIngredientCreate(
                user_id=user_id, ingredient_id=ingredient_id
            )  # type: ignore
        )

    async def add_unloved_ingredient(
        self, user_id: uuid.UUID, ingredient_id: uuid.UUID
    ) -> None:
        await _UnlovedIngredientsRepository(session_maker=self.session_maker).create(
            UnlovedIngredientCreate(
                user_id=user_id, ingredient_id=ingredient_id
            )  # type: ignore
        )
