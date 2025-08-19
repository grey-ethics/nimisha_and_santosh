"""
app/core/config.py

Centralized application configuration using pydantic-settings (Pydantic v2).
Reads .env. All time-based values are minutes/days where noted.

Notes:
- E164_DEFAULT_COUNTRY: used by phone normalization ("IN" by default).
- ACCESS/REFRESH expirations are configurable.
- DEBUG enables more verbose logging.
"""
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Core
    DEBUG: bool = False
    APP_NAME: str = "KidneyTx Pharma Backend"
    APP_VERSION: str = "0.1.0"

    # Database
    DATABASE_URL: str = Field(..., description="postgresql+psycopg2://user:pass@host:port/dbname")

    # JWT / Auth
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    # Phone normalization
    E164_DEFAULT_COUNTRY: str = "IN"

    # Admin bootstrap
    ADMIN_PHONE: str | None = None
    ADMIN_PASSWORD: str | None = None
    ADMIN_FULL_NAME: str | None = None

    # Defaults to speed up demos
    DEFAULT_REGION_NAME: str | None = "Default Region"
    DEFAULT_BRANCH_NAME: str | None = "Default Branch"


settings = Settings()
