from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, JSON, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.domain.models.base import UUIDMixin, TimestampMixin


class Assessment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "assessments"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id: Mapped[UUID] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    findings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error: Mapped[str | None] = mapped_column(Text)

    # Relationships
    asset: Mapped["Asset"] = relationship(lazy="joined", viewonly=True)
    project: Mapped["Project"] = relationship(back_populates="assessments", lazy="selectin")
    findings: Mapped[list["Finding"]] = relationship(back_populates="assessment", lazy="selectin")

    __table_args__ = (
        Index("ix_assessments_org_project_status", "organization_id", "project_id", "status"),
        Index("ix_assessments_org_asset", "organization_id", "asset_id"),
    )