# Ma'lumotlar bazasi ulanishi — async SQLAlchemy engine
# asyncpg driveri ishlatiladi (yuqori unumdorlik uchun)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Async engine yaratish — connection pool sozlamalari bilan
engine = create_async_engine(
    settings.DATABASE_URL,
    # Development da SQL so'rovlarini konsolga chiqarish
    echo=settings.ENVIRONMENT == "development",
    # Connection pool sozlamalari
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Ulanish tirik ekanligini tekshirish
    pool_recycle=3600,   # 1 soatdan keyin ulanishni yangilash
)

# Async sessiya fabrikasi
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Commit dan keyin ob'ektlar yuklanmasin
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Barcha SQLAlchemy modellari uchun asosiy sinf."""
    pass


async def get_db() -> AsyncSession:
    """
    FastAPI Dependency Injection uchun DB sessiyasi.

    Ishlatish:
        async def endpoint(db: AsyncSession = Depends(get_db)):
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            # Xatolik bo'lsa rollback qilish
            await session.rollback()
            raise
        finally:
            await session.close()
