from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, JSON, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.domain.models.base import UUIDMixin, TimestampMixin


class Asset(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "assets"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    identifier: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    criticality: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    last_scanned: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="assets", lazy="selectin")
    assessments: Mapped[list["Assessment"]] = relationship(back_populates="asset", lazy="selectin")

    __table_args__ = (
        Index("ix_assets_identifier_type", "identifier", "type", unique=True),
        Index("ix_assets_org_project_type", "organization_id", "project_id", "type"),
    )