import openai

from foodify.config import config


class ChatGPTRecipientMaker:
    def get_chatgpt_answer(self, message: dict) -> str:
        api_key = config.openai_api_key
        openai.api_key = api_key
        model = "gpt-3.5-turbo"

        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
        )

        recipe = response.choices[0]["message"]["content"].split("\n")
        return recipe

    def get_recipe(self, recipe_description: str) -> str:
        user_input = [
            {"role": "system", "content": "Ты известный шеф повар."},
            {"role": "user", "content": ""},
        ]
        user_input[1]["content"] = recipe_description
        response = self.get_chatgpt_answer(user_input)
        response = "\n".join(response)
        return response
