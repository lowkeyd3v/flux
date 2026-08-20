"""
Centralized application configuration.

All environment-dependent values (database URL, CORS origins, API keys
for future services, etc.) should be read here, not scattered across
the codebase. See backend/.env.example for the full list of variables.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App metadata ---
    APP_NAME: str = "FLUX API"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api"

    # --- Database ---
    DATABASE_URL: str = (
        "postgresql+psycopg2://flux_user:flux_password@localhost:5432/flux_db"
    )

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Future service placeholders (used by service interfaces) ---
    LLM_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor so we don't re-parse the environment on every call."""
    return Settings()
