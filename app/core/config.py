from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/automation"

    class Config:
        env_file = ".env"


settings = Settings()
