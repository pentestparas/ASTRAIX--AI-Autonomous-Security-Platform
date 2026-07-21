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

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Per-request session cache
_request_sessions: dict[int, AsyncSession] = {}


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    import asyncio
    try:
        task_id = id(asyncio.current_task())
    except RuntimeError:
        task_id = id(None)
    
    # Check if we already have a session for this task
    if task_id in _request_sessions:
        yield _request_sessions[task_id]
        return
    
    async with async_session_maker() as session:
        # For SQLite, set journal_mode to DELETE to avoid cross-process visibility issues
        if settings.DATABASE_URL.startswith("sqlite"):
            from sqlalchemy import text
            await session.execute(text("PRAGMA journal_mode=DELETE"))
            await session.execute(text("PRAGMA synchronous=FULL"))
        
        _request_sessions[task_id] = session
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            del _request_sessions[task_id]
            await session.close()


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