"""
app/models/regional_manager_profile.py

Regional Manager Profile: links user -> region.
"""
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RegionalManagerProfile(Base):
    __tablename__ = "regional_manager_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    region_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="RESTRICT"), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(2000))

    user = relationship("User", back_populates="regional_manager_profile")
    region = relationship("Region")
