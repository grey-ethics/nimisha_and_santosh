"""
app/models/region.py

Region entity: RM belongs to exactly one region. Branch belongs to a region.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    branches = relationship("Branch", back_populates="region")
