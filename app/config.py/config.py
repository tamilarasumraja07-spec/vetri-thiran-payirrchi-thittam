from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PocketSmart AI"
    SECRET_KEY: str = "change-this-to-a-long-random-secret"

    DATABASE_URL: str = "sqlite:///./pocketsmart.db"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.8-flash"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    CORS_ORIGINS: str = (
        "http://127.0.0.1:8000,http://localhost:8000"
    )

    MAX_UPLOAD_MB: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins_list(self):
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()