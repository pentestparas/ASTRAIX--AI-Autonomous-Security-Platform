from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from app.database.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDMixin:
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            primary_key=True,
            default=uuid4,
            nullable=False,
            unique=True,
            index=True,
        )


class BaseModel(UUIDMixin, TimestampMixin, Base):
    __abstract__ = True