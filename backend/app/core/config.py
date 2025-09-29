from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("US College Counseling API", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")
    database_url: str = Field("sqlite+aiosqlite:///./data/app.db", env="DATABASE_URL")
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-5", env="OPENAI_MODEL")
    access_token_expire_minutes: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_secret_key: str = Field("change-me", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"], env="CORS_ORIGINS")
    frontend_build_dir: str | None = Field(None, env="FRONTEND_BUILD_DIR")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: Any) -> list[str] | Any:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
