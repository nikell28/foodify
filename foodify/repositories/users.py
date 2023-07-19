import uuid

from foodify.repositories.base import BaseRepository
from foodify.repositories.ingredients import IngredientsRepository
from foodify.db.users import Users
from foodify.models.user import User as UserModel


class UsersRepository(BaseRepository):
    table = Users
    model_cls = UserModel

    async def _fill_favorite_and_unloved_ingredients(
        self, user: UserModel
    ) -> UserModel:
        ingredient_repository = IngredientsRepository(self.session_maker)
        user.favorite_ingredients = (
            await ingredient_repository.get_favorite_ingredients(user_id=user.id)
        )
        user.unloved_ingredients = await ingredient_repository.get_unloved_ingredients(
            user_id=user.id
        )
        return user

    async def get_by_tg_id(self, tg_id) -> UserModel | None:
        row = await self._get_by("tg_id", tg_id)
        if not row:
            return None
        user = self.model_cls.from_orm(row)
        user = await self._fill_favorite_and_unloved_ingredients(user)
        return user

    async def get_all(self) -> list[UserModel]:  # type: ignore
        rows = await self._get_all()
        users = [self.model_cls.from_orm(row) for row in rows]
        users = [
            await self._fill_favorite_and_unloved_ingredients(user) for user in users
        ]
        return users

    async def get_by_id(self, user_id) -> UserModel | None:
        row = await self._get_by("id", user_id)
        if not row:
            return None
        user = self.model_cls.from_orm(row)
        user = await self._fill_favorite_and_unloved_ingredients(user)
        return user

    async def add_favorite_ingredient(
        self, user_id: uuid.UUID, ingredient_id: uuid.UUID
    ) -> None:
        ingredients_repository = IngredientsRepository(self.session_maker)
        await ingredients_repository.add_favorite_ingredient(
            user_id=user_id, ingredient_id=ingredient_id
        )

    async def add_unloved_ingredient(
        self, user_id: uuid.UUID, ingredient_id: uuid.UUID
    ) -> None:
        ingredients_repository = IngredientsRepository(self.session_maker)
        await ingredients_repository.add_unloved_ingredient(
            user_id=user_id, ingredient_id=ingredient_id
        )
