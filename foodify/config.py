import pydantic


class Config(pydantic.BaseSettings):
    openai_api_key: str
    tg_token: str
    promt: str
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()
