from contextlib import asynccontextmanager
from typing import AsyncGenerator
from uuid import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


class Base(DeclarativeBase):
    pass


# Configure engine based on database type
engine_kwargs = {
    "echo": settings.DATABASE_ECHO,
    "future": True,
}

# SQLite-specific settings for development
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False,
    }

# Only use pool settings for PostgreSQL (not SQLite)
if settings.DATABASE_URL.startswith("postgresql"):
    engine_kwargs["pool_size"] = settings.DATABASE_POOL_SIZE
    engine_kwargs["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_timeout"] = 30

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        # For SQLite, set journal_mode to DELETE to avoid cross-process visibility issues
        if settings.DATABASE_URL.startswith("sqlite"):
            from sqlalchemy import text
            await session.execute(text("PRAGMA journal_mode=DELETE"))
            await session.execute(text("PRAGMA synchronous=FULL"))
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    async with engine.begin() as conn:
        # Disable WAL for SQLite to avoid cross-process issues
        if settings.DATABASE_URL.startswith("sqlite"):
            from sqlalchemy import text
            await conn.execute(text("PRAGMA journal_mode=DELETE"))
            await conn.execute(text("PRAGMA synchronous=FULL"))
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()