from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
