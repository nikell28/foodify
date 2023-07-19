import uuid

from foodify.models.recipient import Recipient
from foodify.repositories.users import UsersRepository
from foodify.models.recipient import RecipientInput
from foodify.services.recipient_maker import RecipientMaker
from foodify.db.base import sessionmaker


class FoodyService:
    def __init__(self):
        self.user_repository = UsersRepository(session_maker=sessionmaker)
        self.recipe_maker = RecipientMaker()

    async def get_recipient(
        self, user_id: uuid.UUID | None = None, tg_user_id: str | None = None
    ) -> Recipient:
        user_repository = UsersRepository(session_maker=sessionmaker)
        if user_id:
            user = await user_repository.get_by_id(user_id)
        elif tg_user_id:
            user = await user_repository.get_by_tg_id(tg_user_id)
        else:
            raise ValueError("No user_id or tg_user_id provided")
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        recipient_input = RecipientInput(
            favorite_ingredients=user.favorite_ingredients,  # type: ignore
            unloved_ingredients=user.unloved_ingredients,  # type: ignore
        )
        recipient = await self.recipe_maker.make_recipe(recipient_input)
        return recipient
