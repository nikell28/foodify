from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
)

from foodify.config import config
from foodify.chatgpt_recipient_maker import ChatGPTRecipientMaker


app = ApplicationBuilder().token(config.tg_token).build()


async def get_recipe_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        "Получить рецепт",
        callback_data="/recipe"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Получить рецепт", callback_data="/recipe"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text_message = (
        "Привет! Я бот, который поможет тебе приготовить что-то вкусное."
        "Нажми на кнопку ниже, чтобы получить рецепт."
    )
    await update.message.reply_text(text_message, reply_markup=reply_markup)


async def like_recipe(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [
                await get_recipe_button()
            ]
        ]
    )
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await update.callback_query.message.reply_text(
        "Спасибо за вашу оценку!",
        reply_markup=reply_markup
    )


async def dislike_recipe(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [
                await get_recipe_button()
            ]
        ]
    )
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await update.callback_query.message.reply_text(
        "Мы учтем ваши предпочтения!",
        reply_markup=reply_markup
    )


async def get_recipe(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    await update.callback_query.message.reply_text("Получаю рецепт...")
    chatgpt_recipient_maker = ChatGPTRecipientMaker()
    recipe = chatgpt_recipient_maker.get_recipe(config.promt)

    keyboard = [
        [
            InlineKeyboardButton("👍", callback_data="/like_recipe"),
            InlineKeyboardButton("👎", callback_data="/dislike_recipe"),
        ],
        [
            await get_recipe_button()
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        recipe,
        reply_markup=reply_markup
    )


async def callback_query_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input = update.callback_query.data
    print(input)
    if input == "/like_recipe":
        await like_recipe(update, context)
    elif input == "/dislike_recipe":
        await dislike_recipe(update, context)
    elif input == "/recipe":
        await get_recipe(update, context)


app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback_query_handler))
