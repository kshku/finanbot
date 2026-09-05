from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{root}/.env",
        extra='ignore',
        env_prefix='FINANBOT_',
    )

    model_provider: str
    model_name: str

settings = Settings()
