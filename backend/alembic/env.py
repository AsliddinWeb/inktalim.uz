# Alembic muhit sozlamalari — async migration uchun sozlangan
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Loyiha konfiguratsiyasini import qilish
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database import Base

# Barcha modellarni import qilish (autogenerate uchun kerak)
from app.models import user, course, lesson, module, progress  # noqa: F401

# Alembic Config obyekti
config = context.config

# Logging sozlamasi
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ModellarMetadata — autogenerate uchun
target_metadata = Base.metadata

# .env dan DATABASE_URL ni o'qib, alembic ga berish
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Offline rejimda migration — DB ga ulanmasdan SQL script yaratadi."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # UUID tipini to'g'ri render qilish
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Sinxron ulanish orqali migrationlarni ishga tushirish."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Async engine orqali migrationlarni bajarish."""
    # Async engine yaratish (asyncpg driver ishlatiladi)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Async ulanishni sinxron kontekstga o'tkazish
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Online rejimda async migration ishga tushirish."""
    asyncio.run(run_async_migrations())


# Offline yoki online rejimni tanlash
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
