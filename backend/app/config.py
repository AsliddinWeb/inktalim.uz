# Ilova konfiguratsiyasi — pydantic BaseSettings asosida
# .env fayldan avtomatik o'qiydi

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Barcha muhit o'zgaruvchilari shu yerda jamlangan."""

    # PostgreSQL ulanish sozlamalari
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "inktalim"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"

    # Async SQLAlchemy uchun to'liq URL
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/inktalim"

    # JWT sozlamalari
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Ilova muhiti
    ENVIRONMENT: str = "development"

    # Frontend CORS manziллari (vergul bilan ajratilgan)
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Media (yuklangan fayllar) papkasi — Docker volume bilan mos kelishi kerak
    MEDIA_DIR: str = "media"

    # Pydantic v2 sozlamasi — .env fayldan o'qish
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Settings obyektini bir marta yaratib, keshlab qaytaradi."""
    return Settings()


# Global sozlamalar obyekti — import qilib ishlatish uchun
settings = get_settings()
