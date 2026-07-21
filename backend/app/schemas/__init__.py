from typing import Dict, Any, List, Optional, Generic, TypeVar
from datetime import datetime
import enum

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class BaseSchema(BaseModel):
    """Base schema with ORM mode enabled."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


T = TypeVar("T")


class ResponseSchema(BaseSchema, Generic[T]):
    """Standard success response wrapper."""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated results wrapper."""

    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1