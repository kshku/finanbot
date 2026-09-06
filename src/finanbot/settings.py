from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{root}/.env",
        extra='ignore',
        env_prefix='FINANBOT_',
    )

    # model
    model_provider: str
    model_name: str

    # neo4j
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

settings = Settings()
