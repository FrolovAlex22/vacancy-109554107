import dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseModel):
    KEY: str

class PostgresqlSettings(BaseModel):
    URL: str

class MainSettings(BaseModel):
    HOST: str
    PORT: int

class Settings(BaseSettings):
    AUTH: AuthSettings
    DB: PostgresqlSettings
    MAIN: MainSettings
    app_title: str = "task_manager_fastapi"


    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(".env"),
        env_nested_delimiter="_",
    )


settings = Settings()