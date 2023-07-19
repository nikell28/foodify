from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

from foodify.config import config
from foodify.services.recipient_maker import RecipientMaker
from foodify.models.user import UserCreate
from foodify.repositories.users import UsersRepository
from foodify.services.ingredients_service import IngredientsService
from foodify.services.users_service import UsersService
from foodify.db.base import sessionmaker


app = ApplicationBuilder().token(config.tg_token).build()


async def get_recipe_button() -> InlineKeyboardButton:
    return InlineKeyboardButton("Получить рецепт", callback_data="/recipient")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        raise ValueError("Update message is None")

    if not update.message.from_user:
        raise ValueError("Update message from user is None")
    repository = UsersRepository(session_maker=sessionmaker)
    user = await repository.get_by_tg_id(str(update.message.from_user.id))
    if not user:
        new_user = UserCreate(
            tg_id=str(update.message.from_user.id),
            tg_username=update.message.from_user.username,
            tg_first_name=update.message.from_user.first_name,
        )
        await repository.create(new_user)

    keyboard = [
        [
            InlineKeyboardButton("Получить рецепт", callback_data="/recipient"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text_message = (
        "Привет! Я бот, который поможет тебе приготовить что-то вкусное."
        "Нажми на кнопку ниже, чтобы получить рецепт."
    )
    if not update.message:
        raise ValueError("Update message is None")

    await update.message.reply_text(text_message, reply_markup=reply_markup)


async def add_favorite_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        raise ValueError("Update message is None")
    ingredients_service = IngredientsService()
    ingredients = await ingredients_service.get_all()
    keyboard = []
    for ingredient in ingredients:
        keyboard.append(
            [
                InlineKeyboardButton(
                    ingredient.name,
                    callback_data=f"/add_favorite_ingredient {ingredient.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Далее",
                callback_data="/add_unloved_ingredients",
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите ингредиенты которые вам нравится", reply_markup=reply_markup
    )


async def _add_favorite_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        raise ValueError("Update callback query is None")

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)

    if not query.message:
        raise ValueError("Update callback query message is None")

    await query.edit_message_reply_markup(reply_markup=None)


async def _add_unloved_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        raise ValueError("Update callback query is None")

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)

    if not query.message:
        raise ValueError("Update callback query message is None")

    await query.edit_message_reply_markup(reply_markup=None)


async def add_unloved_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        raise ValueError("Update message is None")
    ingredients_service = IngredientsService()
    ingredients = await ingredients_service.get_all()
    keyboard = []
    for ingredient in ingredients:
        keyboard.append(
            [
                InlineKeyboardButton(
                    ingredient.name,
                    callback_data=f"/add_unloved_ingredient {ingredient.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Получить рецепт",
                callback_data="/get_recipe",
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите ингредиенты которые вам не нравится", reply_markup=reply_markup
    )


async def like_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup([[await get_recipe_button()]])
    query = update.callback_query

    if not query:
        raise ValueError("Update callback query is None")

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)

    if not query.message:
        raise ValueError("Update callback query message is None")

    await query.message.reply_text("Спасибо за вашу оценку!", reply_markup=reply_markup)


async def dislike_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup([[await get_recipe_button()]])
    query = update.callback_query

    if not query:
        raise ValueError("Update callback query is None")

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)

    if not query.message:
        raise ValueError("Update callback query message is None")

    await query.message.reply_text(
        "Мы учтем ваши предпочтения!", reply_markup=reply_markup
    )


async def get_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        raise ValueError("Update callback query is None")

    await update.callback_query.answer()
    await update.callback_query.edit_message_reply_markup(reply_markup=None)

    if not update.callback_query.message:
        raise ValueError("Update callback query message is None")

    await update.callback_query.message.reply_text("Получаю рецепт...")
    chatgpt_recipient_maker = RecipientMaker()
    recipient = chatgpt_recipient_maker.get_recipe(config.promt)

    keyboard = [
        [
            InlineKeyboardButton("👍", callback_data="/like_recipe"),
            InlineKeyboardButton("👎", callback_data="/dislike_recipe"),
        ],
        [await get_recipe_button()],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(recipient, reply_markup=reply_markup)


async def callback_query_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.callback_query:
        raise ValueError("Update callback query is None")

    input = update.callback_query.data
    print(input)
    if input == "/like_recipe":
        await like_recipe(update, context)
    elif input == "/dislike_recipe":
        await dislike_recipe(update, context)
    elif input == "/recipient":
        await get_recipe(update, context)
    elif input == "/add_favorite_ingredients":
        await add_favorite_ingredients(update, context)
    elif input == "/add_favorite_ingredient":
        await _add_favorite_ingredient(update, context)
    elif input == "/add_unloved_ingredients":
        await add_unloved_ingredients(update, context)
    elif input == "/add_unloved_ingredient":
        await _add_unloved_ingredient(update, context)


app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback_query_handler))
