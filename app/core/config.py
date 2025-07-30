from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = "sqlite://db.sqlite3"

    API_KEY: str = "mysecret123"

    WEB_APP_TITLE: str = "Chat Message Processor API"
    WEB_APP_DESCRIPTION: str = "REST API for receiving, validating and storing chat messages."
    WEB_APP_VERSION: str = "1.0.0"

    DEBUGGER: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
