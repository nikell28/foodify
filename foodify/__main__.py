import logging

from foodify.chatbot import app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Foodify Bot")
    app.run_polling()
