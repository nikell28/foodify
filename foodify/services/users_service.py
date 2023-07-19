from foodify.repositories.users import UsersRepository
from foodify.models.user import User


class UsersService:
    def __init__(self):
        self.__users_repository = UsersRepository()

    async def get_by_tg_id(self, tg_id: str) -> User | None:
        return await self.__users_repository.get_by_tg_id(tg_id)

    async def get_all(self) -> list[User]:
        return await self.__users_repository.get_all()

    async def create(self, user: User) -> User:
        return await self.__users_repository.create(user)
