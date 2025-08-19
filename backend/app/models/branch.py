"""
app/models/branch.py

Branch: belongs to a Region. BM belongs to a Branch. Name unique within region.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Branch(Base):
    __tablename__ = "branches"
    __table_args__ = (
        UniqueConstraint("region_id", "name", name="uq_branch_region_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="RESTRICT"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str | None] = mapped_column(String(300))

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    region = relationship("Region", back_populates="branches")
    branch_managers = relationship("BranchManagerProfile", back_populates="branch")
    patients = relationship("PatientProfile", back_populates="branch")
    