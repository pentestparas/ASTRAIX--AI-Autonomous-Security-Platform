from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, JSON, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.domain.models.base import UUIDMixin, TimestampMixin


class Finding(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "findings"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id: Mapped[str] = mapped_column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    plugin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    cvss_score: Mapped[float | None] = mapped_column()
    remediation: Mapped[str | None] = mapped_column(Text)
    reference: Mapped[str | None] = mapped_column(Text)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False, index=True)

    # Relationships
    assessment: Mapped["Assessment"] = relationship(back_populates="findings", lazy="selectin")
    asset: Mapped["Asset"] = relationship(lazy="selectin")
    project: Mapped["Project"] = relationship(lazy="selectin")

    __table_args__ = (
        Index("ix_findings_asset_severity", "asset_id", "severity"),
        Index("ix_findings_assessment_fingerprint", "assessment_id", "fingerprint"),
        Index("ix_findings_org_project_status", "organization_id", "project_id", "status"),
        Index("ix_findings_org_severity_status", "organization_id", "severity", "status"),
    )